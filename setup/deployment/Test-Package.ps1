param([Parameter(Mandatory=$true)][string]$Archive,[Parameter(Mandatory=$true)][string]$Destination,[string]$Python)
. (Join-Path $PSScriptRoot 'Start-Deployment.ps1')
try {
    $target=[IO.Path]::GetFullPath($Destination).TrimEnd('\','/')
    Assert-NoReparse $target
    if ($target.Length -lt 4 -or (Test-Path -LiteralPath $target)) { Stop-Deployment 'fresh_test_destination_required' 4 }
    $package=Join-Path $target 'package'
    Expand-VerifiedZip ([IO.Path]::GetFullPath($Archive)) $package
    $manifest=Read-DeploymentPackage $package
    $installation=Join-Path $target 'installation'
    $shell=Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
    $preflight=& $shell -NoProfile -File (Join-Path $package 'Preflight.ps1') -Destination $installation
    if ($LASTEXITCODE -ne 0) { [Console]::Out.WriteLine(($preflight -join [Environment]::NewLine)); exit 5 }
    $bootstrap=& $shell -NoProfile -File (Join-Path $package 'Bootstrap.ps1') -Destination $installation
    $bootstrapExit=$LASTEXITCODE
    $bootstrapResult=($bootstrap -join [Environment]::NewLine) | ConvertFrom-Json
    if ($bootstrapExit -ne 2 -or $bootstrapResult.code -ne 'local_tooling_verified_host_activation_pending') { [Console]::Out.WriteLine(($bootstrap -join [Environment]::NewLine)); exit 5 }
    $python=Join-Path $installation 'workspace/.venv/Scripts/python.exe'
    & $python -I -B (Join-Path $package 'tools/release_tests.py') --archive ([IO.Path]::GetFullPath($Archive)) --package $package --destination $installation
    exit $LASTEXITCODE
} catch {
    [Console]::Out.WriteLine(($_ | Out-String))
    exit 5
}
