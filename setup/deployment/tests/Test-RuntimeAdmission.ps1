param([Parameter(Mandatory=$true)][string]$RuntimeArchive,[Parameter(Mandatory=$true)][string]$Destination)
# Inert inventory-only fixtures. No startup module or payload is created.
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
. (Join-Path $source 'Start-Deployment.ps1')
$root=[IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $root) { throw 'fresh_runtime_test_destination_required' }
$package=Join-Path $root 'package'
$target=Join-Path $root 'installation'
[IO.Directory]::CreateDirectory($package) | Out-Null
foreach ($name in @('Start-Deployment.ps1','Bootstrap.ps1','Verify.ps1','Recover.ps1')) {
    Copy-Item -LiteralPath (Join-Path $source $name) -Destination (Join-Path $package $name)
}
Copy-Item -LiteralPath $RuntimeArchive -Destination (Join-Path $package 'python.zip')
$manifest=@{schema_version=1;package_id='inert-runtime-inventory';files=@();dependencies=@(
    @{name='CPython';filename='python.zip';sha256=(Get-Digest (Join-Path $package 'python.zip'))})}
foreach ($file in Get-ChildItem -LiteralPath $package -File) {
    $manifest.files+=@{path=$file.Name;size_bytes=$file.Length;sha256=(Get-Digest $file.FullName)}
}
[IO.File]::WriteAllText((Join-Path $package 'manifest.json'),($manifest | ConvertTo-Json -Depth 10))
[IO.File]::WriteAllText((Join-Path $package 'manifest.sha256'),(Get-Digest (Join-Path $package 'manifest.json')))
$manifest=Read-DeploymentPackage $package
$runtime=Join-Path $target 'tooling/python'
[IO.Directory]::CreateDirectory((Join-Path $target 'tooling')) | Out-Null
Expand-VerifiedZip (Join-Path $package 'python.zip') $runtime
[IO.Directory]::CreateDirectory((Join-Path $target '.deployment')) | Out-Null
Write-NewJson (Join-Path $target '.deployment/owner.json') @{package_id=$manifest.package_id;manifest_sha256=(Get-Digest (Join-Path $package 'manifest.json'));target=$target}
# Exact trusted archive bytes are admitted without starting an interpreter.
$python=Get-DeploymentPython $package $target $manifest 'verify'
if ($python -ne (Join-Path $runtime 'python.exe')) { throw 'exact_runtime_not_admitted' }
$sentinel=Join-Path $root 'unrelated.txt'
[IO.File]::WriteAllText($sentinel,'unchanged')
$extra=Join-Path $runtime 'Lib/extra-inventory.txt'
[IO.File]::WriteAllText($extra,'inert additional runtime file')
$extraHash=Get-Digest $extra
$outcomes=@();$failures=@()
$shell=Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
$extraRefused=$false
try { $null=Get-DeploymentPython $package $target $manifest 'verify';$failures+='extra_file_admitted' }
catch { if ($_.Exception.Message -ne 'runtime_inventory_mismatch') { throw };$extraRefused=$true }
# Public refusal is checked only after inventory itself refuses, so RED never starts Python.
foreach ($command in @('Bootstrap','Verify','Recover') | Where-Object { $extraRefused }) {
    $output=& $shell -NoProfile -File (Join-Path $package ($command+'.ps1')) -Destination $target 2> (Join-Path $root ($command+'.stderr.txt'))
    $exit=$LASTEXITCODE
    $value=($output -join [Environment]::NewLine) | ConvertFrom-Json
    $outcomes+=@{command=$command;exit=$exit;code=$value.code}
    if ($exit -ne 4 -or $value.code -ne 'runtime_inventory_mismatch') { $failures+='extra_file_not_refused_before_interpreter:'+ $command }
    if ((Get-Digest $extra) -ne $extraHash) { throw 'inert_extra_not_preserved' }
}
# Remove only this test's known inert extra; exact inventory must again admit.
Remove-Item -LiteralPath $extra
if ((Get-DeploymentPython $package $target $manifest 'verify') -ne $python) { throw 'exact_runtime_not_readmitted' }
# Empty unexpected directories also conflict; no blanket cache exemption.
$extraDirectory=Join-Path $runtime 'unknown-empty-cache'
[IO.Directory]::CreateDirectory($extraDirectory) | Out-Null
try { $null=Get-DeploymentPython $package $target $manifest 'verify';$failures+='extra_directory_admitted' }
catch { if ($_.Exception.Message -ne 'runtime_inventory_mismatch') { throw } }
if (-not [IO.Directory]::Exists($extraDirectory)) { throw 'directory_not_preserved' }
Remove-Item -LiteralPath $extraDirectory
# Changed original bytes are refused and preserved, without executing them.
$license=Join-Path $runtime 'LICENSE.txt'
$original=[IO.File]::ReadAllBytes($license)
[IO.File]::WriteAllText($license,'inert changed license')
$changedHash=Get-Digest $license
try { $null=Get-DeploymentPython $package $target $manifest 'verify';$failures+='changed_file_admitted' }
catch { if ($_.Exception.Message -ne 'changed_runtime') { throw } }
if ((Get-Digest $license) -ne $changedHash) { throw 'changed_file_not_preserved' }
[IO.File]::WriteAllBytes($license,$original)
if ([IO.File]::ReadAllText($sentinel) -ne 'unchanged') { throw 'sentinel_changed' }
# Structural ordering: the complete runtime admission call precedes interpreter invocation.
$launcher=[IO.File]::ReadAllText((Join-Path $source 'Start-Deployment.ps1'))
if ($launcher.IndexOf('$python=Get-DeploymentPython') -ge $launcher.IndexOf('& $python @arguments')) { throw 'runtime_admission_order' }
@{status=$(if ($failures.Count) {'failed'} else {'passed'});public_outcomes=$outcomes;failures=$failures;fixture='inert text only';sentinel='unchanged'} | ConvertTo-Json -Depth 8
if ($failures.Count) { exit 1 }
exit 0
