param([string]$Package,[string]$Destination,[ValidateSet('reachable','unavailable','unproven')][string]$Mode)
Import-Module Microsoft.PowerShell.Utility,Microsoft.PowerShell.Management
. (Join-Path $Package 'Start-Deployment.ps1')
$keys=@('PATH','GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT','PIP_TARGET','PYTHONPATH','TEMP','TMP')
$before=@{};foreach($key in $keys){$before[$key]=[string][Environment]::GetEnvironmentVariable($key)}
$probe={
    param([string]$Url)
    [Console]::Error.WriteLine('primary_probe:'+$Url)
    if($Mode -eq 'unproven'){throw 'synthetic unavailable transport'}
    return @{reachable=($Mode -eq 'reachable');status_code=$(if($Mode -eq 'reachable'){200}else{503})}
}
$code=Invoke-Deployment -Command preflight -Destination $Destination -NetworkProbe $probe
$after=@{};foreach($key in $keys){$after[$key]=[string][Environment]::GetEnvironmentVariable($key)}
if($after.Count -ne $before.Count){throw ('caller_environment_changed:'+$key+':beforeNull='+($null -eq $before[$key])+':afterNull='+($null -eq $after[$key])+':beforeLength='+([string]$before[$key]).Length+':afterLength='+([string]$after[$key]).Length)}
foreach($key in $before.Keys){if($before[$key] -cne $after[$key]){throw ('caller_environment_changed:'+$key)}}
exit $code
