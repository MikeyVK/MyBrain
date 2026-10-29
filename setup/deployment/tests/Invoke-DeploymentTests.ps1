param([ValidateSet('Contracts','Provisioning','Archive')][string]$Suite='Contracts',[string]$Python)
$ErrorActionPreference='Stop'
if (-not $Python) { $Python=Join-Path $PSScriptRoot '../../../.venv/Scripts/python.exe' }
$files=@{Contracts=@('test_contracts.py','test_journal.py','test_preflight.py');Provisioning=@('test_provisioning.py','test_git_promotion.py');Archive=@('test_archive.py')}
foreach ($test in $files[$Suite]) {
    & $Python -B (Join-Path $PSScriptRoot $test)
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
exit 0
