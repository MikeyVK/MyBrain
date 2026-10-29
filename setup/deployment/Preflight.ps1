param([Parameter(Mandatory=$true)][string]$Destination,[string]$BindingName='', [ValidateSet('Resume','DiscardStaging')][string]$Action='Resume')
. (Join-Path $PSScriptRoot 'Start-Deployment.ps1')
$deploymentExit=Invoke-Deployment -Command 'preflight' -Destination $Destination -BindingName $BindingName -Action $Action
exit $deploymentExit
