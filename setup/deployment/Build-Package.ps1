param([Parameter(Mandatory=$true)][string]$Destination,[Parameter(Mandatory=$true)][string]$Sources,[string]$Python)
$ErrorActionPreference='Stop'
$script=Join-Path $PSScriptRoot 'builder.py'
if (-not (Test-Path -LiteralPath $script)) { $script=Join-Path $PSScriptRoot 'tools/builder.py' }
if (-not $Python) { $Python=Join-Path $PSScriptRoot '../../.venv/Scripts/python.exe' }
if (-not (Test-Path -LiteralPath $Python)) { throw 'Provide -Python with the verified build environment interpreter' }
& $Python -B $script --output $Destination --sources $Sources
exit $LASTEXITCODE
