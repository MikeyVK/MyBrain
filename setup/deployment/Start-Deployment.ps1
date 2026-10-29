# Deployment-only Windows boundary. No global configuration or credentials are changed.
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Stop-Deployment([string]$Code,[int]$ExitCode=3) {
    $problem=[Exception]::new($Code)
    $problem.Data['deployment_exit']=$ExitCode
    throw $problem
}
function Assert-NoReparse([string]$Path) {
    $current=[IO.Path]::GetFullPath($Path)
    while ($current) {
        try {
            $attributes=[IO.File]::GetAttributes($current)
            if (($attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { Stop-Deployment 'reparse_path' }
        } catch [IO.FileNotFoundException] { } catch [IO.DirectoryNotFoundException] { }
        $parent=[IO.Path]::GetDirectoryName($current.TrimEnd('\','/'))
        if ($parent -eq $current) { break }
        $current=$parent
    }
}
function Assert-Relative([string]$Name) {
    if (-not $Name -or $Name.StartsWith('/') -or $Name.Contains('\')) { Stop-Deployment 'unsafe_path' }
    foreach ($part in $Name.Split('/')) {
        if (-not $part -or $part -eq '.' -or $part -eq '..' -or $part -match '[<>:"|?*\x00-\x1f]' -or $part -match '[. ]$' -or $part -match '^(?i:con|prn|aux|nul|com[0-9]|lpt[0-9])(\..*)?$') { Stop-Deployment 'unsafe_path' }
    }
}
function Get-Digest([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Get-PortableFiles([string]$Root) {
    $todo=[Collections.Generic.Stack[string]]::new();$todo.Push($Root)
    while ($todo.Count -gt 0) {
        $directory=$todo.Pop()
        foreach ($item in [IO.Directory]::EnumerateFileSystemEntries($directory)) {
            Assert-NoReparse $item
            if ([IO.Directory]::Exists($item)) { $todo.Push($item) } else { $item }
        }
    }
}
function Read-DeploymentPackage([string]$Root) {
    Assert-NoReparse $Root
    $manifestPath=Join-Path $Root 'manifest.json'
    if (-not (Test-Path -LiteralPath $manifestPath) -or -not (Test-Path -LiteralPath (Join-Path $Root 'manifest.sha256'))) { Stop-Deployment 'missing_manifest' }
    if ((Get-Digest $manifestPath) -ne ([IO.File]::ReadAllText((Join-Path $Root 'manifest.sha256')).Trim())) { Stop-Deployment 'manifest_digest' }
    $manifest=[IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
    $allowed=@('$comment','schema_version','package_id','created_utc','builder_revision','target','network_mode','files','sources','dependencies','exclusions','limits')
    foreach ($prop in $manifest.PSObject.Properties.Name) { if ($prop -notin $allowed) { Stop-Deployment 'manifest_schema' } }
    if ($manifest.schema_version -ne 1 -or -not $manifest.package_id -or @($manifest.files).Count -eq 0) { Stop-Deployment 'manifest_schema' }
    $names=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    $declared=@{}
    [long]$total=0
    foreach ($entry in $manifest.files) {
        Assert-Relative $entry.path
        if ($entry.path -in @('manifest.json','manifest.sha256') -or -not $names.Add($entry.path)) { Stop-Deployment 'duplicate_path' }
        if ($entry.sha256 -cnotmatch '^[a-f0-9]{64}$' -or $entry.size_bytes -lt 0) { Stop-Deployment 'file_schema' }
        $path=Join-Path $Root $entry.path
        Assert-NoReparse $path
        if (-not [IO.File]::Exists($path) -or (Get-Item -LiteralPath $path).Length -ne $entry.size_bytes -or (Get-Digest $path) -cne $entry.sha256) { Stop-Deployment 'payload_digest' }
        $total+=$entry.size_bytes
        $declared[$entry.path]=$entry
    }
    if ($total -gt 2000000000 -or $names.Count -gt 20000) { Stop-Deployment 'package_bounds' }
    $files=@(Get-PortableFiles $Root)
    if ($files.Count -ne $names.Count+2) { Stop-Deployment 'inventory_mismatch' }
    foreach ($path in $files) {
        $relative=$path.Substring($Root.TrimEnd('\','/').Length+1).Replace('\','/')
        if ($relative -notin @('manifest.json','manifest.sha256') -and -not $names.Contains($relative)) { Stop-Deployment 'inventory_mismatch' }
    }
    if ($manifest.PSObject.Properties.Name -contains 'sources') {
        foreach ($source in $manifest.sources) {
            foreach ($original in $source.files) {
                $key=$source.tree_path+'/'+$original.path
                if (-not $declared.ContainsKey($key) -or $declared[$key].sha256 -cne $original.sha256) { Stop-Deployment 'source_reconstruction' }
            }
        }
    }
    return $manifest
}
function Assert-Target([string]$Destination,[string]$Package,$Manifest) {
    $target=[IO.Path]::GetFullPath($Destination).TrimEnd('\','/')
    Assert-NoReparse $target
    if ($target.Length -lt 4 -or $target.Length -gt 100 -or $target -eq $Package -or $Package.StartsWith($target+'\',[StringComparison]::OrdinalIgnoreCase) -or $target.StartsWith($Package+'\',[StringComparison]::OrdinalIgnoreCase)) { Stop-Deployment 'unsafe_destination' 4 }
    if (Test-Path -LiteralPath $target) {
        if (-not [IO.Directory]::Exists($target)) { Stop-Deployment 'destination_not_directory' 4 }
        if (@(Get-ChildItem -Force -LiteralPath $target).Count -gt 0) {
            $ownerPath=Join-Path $target '.deployment/owner.json'
            if (-not [IO.File]::Exists($ownerPath)) { Stop-Deployment 'foreign_destination' 4 }
            $owner=[IO.File]::ReadAllText($ownerPath) | ConvertFrom-Json
            if ($owner.package_id -cne $Manifest.package_id -or $owner.manifest_sha256 -cne (Get-Digest (Join-Path $Package 'manifest.json')) -or $owner.target -ine $target) { Stop-Deployment 'destination_identity' 4 }
        }
    }
    return $target
}
function Write-NewJson([string]$Path,$Value) {
    $bytes=[Text.UTF8Encoding]::new($false).GetBytes(($Value | ConvertTo-Json -Depth 20)+[Environment]::NewLine)
    $stream=[IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length) } finally { $stream.Dispose() }
}
function Inspect-Zip($Zip) {
    $names=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    [long]$total=0
    if ($Zip.Entries.Count -gt 20000) { Stop-Deployment 'archive_bounds' }
    foreach ($entry in $Zip.Entries) {
        $name=$entry.FullName.TrimEnd('/')
        Assert-Relative $name
        if (-not $names.Add($name)) { Stop-Deployment 'duplicate_archive_path' }
        $kind=($entry.ExternalAttributes -shr 16) -band 61440
        if ($kind -notin @(0,32768,16384)) { Stop-Deployment 'archive_link' }
        $total+=$entry.Length
        if ($entry.Length -gt 600000000 -or $total -gt 2000000000) { Stop-Deployment 'archive_bounds' }
    }
}
function Expand-VerifiedZip([string]$Archive,[string]$Target) {
    Assert-NoReparse $Target
    if (Test-Path -LiteralPath $Target) { Stop-Deployment 'existing_stage' 4 }
    $zip=[IO.Compression.ZipFile]::OpenRead($Archive)
    try {
        Inspect-Zip $zip
        [IO.Directory]::CreateDirectory($Target) | Out-Null
        foreach ($entry in $zip.Entries) {
            $out=Join-Path $Target $entry.FullName
            Assert-NoReparse $out
            if ($entry.FullName.EndsWith('/')) { [IO.Directory]::CreateDirectory($out) | Out-Null; continue }
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($out)) | Out-Null
            $src=$entry.Open();$dst=[IO.File]::Open($out,[IO.FileMode]::CreateNew)
            try { $src.CopyTo($dst) } finally { $src.Dispose();$dst.Dispose() }
        }
    } finally { $zip.Dispose() }
}
function Get-DeploymentPython([string]$Root,[string]$Target,$Manifest,[string]$Command) {
    $runtime=Join-Path $Target 'tooling/python'
    $python=Join-Path $runtime 'python.exe'
    $artifact=@($Manifest.dependencies | Where-Object { $_.name -eq 'CPython' })
    if ($artifact.Count -ne 1) { Stop-Deployment 'runtime_dependency_required' }
    $archive=Join-Path $Root $artifact[0].filename
    if ((Get-Digest $archive) -cne $artifact[0].sha256) { Stop-Deployment 'runtime_digest' }
    if (-not [IO.File]::Exists($python)) {
        if ($Command -ne 'bootstrap' -and $Command -ne 'recover') { Stop-Deployment 'bootstrap_required' 2 }
        $metadata=Join-Path $Target '.deployment'
        [IO.Directory]::CreateDirectory($metadata) | Out-Null
        $owner=Join-Path $metadata 'owner.json'
        if (-not [IO.File]::Exists($owner)) { Write-NewJson $owner @{ package_id=$Manifest.package_id; manifest_sha256=(Get-Digest (Join-Path $Root 'manifest.json')); target=$Target } }
        $stage=Join-Path $metadata 'python-stage'
        if (Test-Path -LiteralPath $stage) {
            # Preserve interrupted bytes rather than removing an unverified tree.
            $quarantine=Join-Path $metadata ('quarantine/python-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffffff'))
            Assert-NoReparse $stage;Assert-NoReparse $quarantine
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($quarantine)) | Out-Null
            Move-Item -LiteralPath $stage -Destination $quarantine
        }
        Expand-VerifiedZip $archive $stage
        [IO.Directory]::CreateDirectory((Join-Path $Target 'tooling')) | Out-Null
        if (Test-Path -LiteralPath $runtime) { Stop-Deployment 'runtime_conflict' 4 }
        Assert-NoReparse $runtime
        Move-Item -LiteralPath $stage -Destination $runtime
    }
    $zip=[IO.Compression.ZipFile]::OpenRead($archive)
    try {
        Inspect-Zip $zip
        # Admit the complete archive inventory before any interpreter startup.
        # No cache or extension-based exemptions: normal managed runs use -B.
        $runtimeFiles=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
        $runtimeDirectories=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
        foreach ($entry in $zip.Entries) {
            $name=$entry.FullName.TrimEnd('/')
            $parts=$name.Split('/')
            for ($i=1;$i -lt $parts.Count;$i++) { [void]$runtimeDirectories.Add(($parts[0..($i-1)] -join '/')) }
            if ($entry.FullName.EndsWith('/')) { [void]$runtimeDirectories.Add($name) }
            else { [void]$runtimeFiles.Add($name) }
        }
        $observedFiles=@(Get-PortableFiles $runtime)
        if ($observedFiles.Count -ne $runtimeFiles.Count) { Stop-Deployment 'runtime_inventory_mismatch' 4 }
        foreach ($path in $observedFiles) {
            $relative=$path.Substring($runtime.Length+1).Replace('\','/')
            if (-not $runtimeFiles.Contains($relative)) { Stop-Deployment 'runtime_inventory_mismatch' 4 }
        }
        $observedDirectories=@([IO.Directory]::EnumerateDirectories($runtime,'*',[IO.SearchOption]::AllDirectories))
        if ($observedDirectories.Count -ne $runtimeDirectories.Count) { Stop-Deployment 'runtime_inventory_mismatch' 4 }
        foreach ($path in $observedDirectories) {
            Assert-NoReparse $path
            $relative=$path.Substring($runtime.Length+1).Replace('\','/')
            if (-not $runtimeDirectories.Contains($relative)) { Stop-Deployment 'runtime_inventory_mismatch' 4 }
        }

        foreach ($entry in $zip.Entries) {
            if ($entry.FullName.EndsWith('/')) { continue }
            $out=Join-Path $runtime $entry.FullName
            Assert-NoReparse $out
            if (-not [IO.File]::Exists($out) -or (Get-Item -LiteralPath $out).Length -ne $entry.Length) { Stop-Deployment 'changed_runtime' 4 }
            $src=$entry.Open();$sha=[Security.Cryptography.SHA256]::Create()
            try { $expected=([BitConverter]::ToString($sha.ComputeHash($src))).Replace('-','').ToLowerInvariant() } finally { $src.Dispose();$sha.Dispose() }
            if ((Get-Digest $out) -cne $expected) { Stop-Deployment 'changed_runtime' 4 }
        }
    } finally { $zip.Dispose() }
    return $python
}
function Remove-VerifiedStaging([string]$Root,[string]$Target,$Manifest) {
    $metadata=Join-Path $Target '.deployment'
    if (-not [IO.File]::Exists((Join-Path $metadata 'owner.json'))) { Stop-Deployment 'bootstrap_required' 2 }
    if (Test-Path -LiteralPath (Join-Path $metadata 'writer.lock')) { Stop-Deployment 'writer_lock_requires_resume' 4 }
    $removed=@()
    foreach ($stageName in @('python-stage','git-stage')) {
        $stage=Join-Path $metadata $stageName
        if (-not (Test-Path -LiteralPath $stage)) { continue }
        Assert-NoReparse $stage
        if (-not ([IO.Path]::GetFullPath($stage)).StartsWith(([IO.Path]::GetFullPath($metadata)+'\'),[StringComparison]::OrdinalIgnoreCase)) { Stop-Deployment 'staging_outside_destination' 4 }
        if ($stageName -eq 'python-stage') {
            $dependency=@($Manifest.dependencies | Where-Object { $_.name -eq 'CPython' })[0]
            $archive=Join-Path $Root $dependency.filename
        } else {
            $dependency=@($Manifest.dependencies | Where-Object { $_.name -eq 'MinGit' })[0]
            $archive=Join-Path $metadata 'downloads/mingit.zip'
        }
        if (-not [IO.File]::Exists($archive) -or (Get-Digest $archive) -cne $dependency.sha256) { Stop-Deployment 'staging_provenance_unverified' 4 }
        $zip=[IO.Compression.ZipFile]::OpenRead($archive)
        try {
            Inspect-Zip $zip
            $entries=@{};$directories=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
            foreach ($entry in $zip.Entries) {
                $name=$entry.FullName.TrimEnd('/')
                $parts=$name.Split('/')
                for ($i=1;$i -lt $parts.Count;$i++) { [void]$directories.Add(($parts[0..($i-1)] -join '/')) }
                if (-not $entry.FullName.EndsWith('/')) { $entries[$name]=$entry } else { [void]$directories.Add($name) }
            }
            foreach ($path in @(Get-PortableFiles $stage)) {
                $relative=$path.Substring($stage.Length+1).Replace('\','/')
                if (-not $entries.ContainsKey($relative)) { Stop-Deployment 'unverified_staging_content' 4 }
                $stream=$entries[$relative].Open();$sha=[Security.Cryptography.SHA256]::Create()
                try { $expected=([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant() } finally { $stream.Dispose();$sha.Dispose() }
                if ((Get-Digest $path) -cne $expected) { Stop-Deployment 'changed_staging_preserved' 4 }
            }
            foreach ($directory in [IO.Directory]::EnumerateDirectories($stage,'*',[IO.SearchOption]::AllDirectories)) {
                Assert-NoReparse $directory
                if (-not $directories.Contains($directory.Substring($stage.Length+1).Replace('\','/'))) { Stop-Deployment 'unverified_staging_directory' 4 }
            }
        } finally { $zip.Dispose() }
        Assert-NoReparse $stage
        # The resolved target is a verified-owned named staging directory inside this destination.
        Remove-Item -LiteralPath $stage -Recurse
        $removed+=$stageName
    }
    return $removed
}

function Invoke-ReadOnlyGit([string]$Executable,[string]$Arguments,[string]$WorkingDirectory) {
    $process=[Diagnostics.Process]::new()
    try {
        $info=[Diagnostics.ProcessStartInfo]::new()
        $info.FileName=$Executable;$info.Arguments=$Arguments;$info.WorkingDirectory=$WorkingDirectory
        $info.UseShellExecute=$false;$info.CreateNoWindow=$true
        $info.RedirectStandardOutput=$true;$info.RedirectStandardError=$true
        foreach($key in @($info.EnvironmentVariables.Keys)) {
            if($key -like 'GIT_*' -or $key -like 'PGMCP_*' -or $key -like 'PYTHON*') { $info.EnvironmentVariables.Remove($key) }
        }
        $info.EnvironmentVariables['GIT_CONFIG_NOSYSTEM']='1'
        $info.EnvironmentVariables['GIT_CONFIG_GLOBAL']='NUL'
        $info.EnvironmentVariables['GIT_CONFIG_SYSTEM']='NUL'
        $info.EnvironmentVariables['GIT_OPTIONAL_LOCKS']='0'
        $process.StartInfo=$info
        [void]$process.Start()
        if(-not $process.WaitForExit(3000)) { $process.Kill();$process.WaitForExit();return $null }
        if($process.ExitCode -ne 0) { return $null }
        return $process.StandardOutput.ReadToEnd()
    } catch { return $null } finally { $process.Dispose() }
}
function Get-SuitableGit([string]$Executable,[string]$WorkingDirectory) {
    $version=Invoke-ReadOnlyGit $Executable '--version' $WorkingDirectory
    if(-not $version -or $version -notmatch 'git version (\d+)\.(\d+)\.(\d+)') { return $null }
    $parsed=[Version]::new([int]$Matches[1],[int]$Matches[2],[int]$Matches[3])
    if($parsed -lt [Version]'2.51.0') { return $null }
    $commands=Invoke-ReadOnlyGit $Executable '--list-cmds=main' $WorkingDirectory
    if(-not $commands) { return $null }
    $names=$commands -split '\s+'
    foreach($required in @('init','add','commit','status')) { if($required -notin $names) { return $null } }
    return $parsed.ToString()
}
function Test-PrimaryGitSource([string]$Url) {
    $request=$null;$response=$null;$wait=$null
    try {
        $uri=[Uri]$Url
        if($uri.Scheme -ne 'https' -or $uri.UserInfo) { return @{reachable=$false;status_code=0} }
        $request=[Net.HttpWebRequest]::Create($uri)
        $request.Method='HEAD';$request.AllowAutoRedirect=$true;$request.MaximumAutomaticRedirections=3
        $request.Timeout=8000;$request.ReadWriteTimeout=8000
        $request.UseDefaultCredentials=$false;$request.Credentials=$null
        $pending=$request.BeginGetResponse($null,$null);$wait=$pending.AsyncWaitHandle
        if(-not $wait.WaitOne(8000)) { return @{reachable=$false;status_code=0} }
        $response=$request.EndGetResponse($pending)
        $status=[int]$response.StatusCode
        return @{reachable=($status -ge 200 -and $status -lt 300);status_code=$status}
    } catch { return @{reachable=$false;status_code=0} }
    finally { if($response){$response.Close()};if($request){$request.Abort()};if($wait){$wait.Close()} }
}
function Get-PreflightGit([string]$Root,[string]$Target,$Manifest,[scriptblock]$NetworkProbe) {
    $localRoot=Join-Path $Target 'tooling/git'
    $localGit=Join-Path $localRoot 'cmd/git.exe'
    if(Test-Path -LiteralPath $localRoot) {
        # Existing target executables are admitted by their owned exact inventory before use.
        $journalPath=Join-Path $Target '.deployment/journal.json'
        Assert-NoReparse $journalPath
        if(-not [IO.File]::Exists($journalPath)) { Stop-Deployment 'git_local_provenance_unverified' 2 }
        $journal=[IO.File]::ReadAllText($journalPath) | ConvertFrom-Json
        if('outputs' -notin $journal.PSObject.Properties.Name) { Stop-Deployment 'git_local_provenance_unverified' 2 }
        $records=@{}
        foreach($entry in $journal.outputs.PSObject.Properties) {
            if($entry.Name.StartsWith('tooling/git/')) { $records[$entry.Name.Substring(12)]=$entry.Value }
        }
        $files=@(Get-PortableFiles $localRoot)
        if(-not $records.Count -or $files.Count -ne $records.Count) { Stop-Deployment 'git_local_inventory_conflict' 4 }
        foreach($file in $files) {
            $relative=$file.Substring($localRoot.Length+1).Replace('\','/')
            if(-not $records.ContainsKey($relative) -or (Get-Digest $file) -cne $records[$relative]) { Stop-Deployment 'git_local_inventory_conflict' 4 }
        }
        $version=Get-SuitableGit $localGit $Root
        if(-not $version) { Stop-Deployment 'git_local_unusable' 2 }
        return @{ready=$true;source='target_verified_inventory';version=$version;network_required=$false;download_required=$false;availability='usable'}
    }
    $hostGit=Get-Command git -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if($hostGit) {
        $version=Get-SuitableGit $hostGit.Source $Root
        if($version) { return @{ready=$true;source='host';version=$version;network_required=$false;download_required=$false;availability='usable'} }
    }
    $fallback=@($Manifest.dependencies | Where-Object { $_.name -eq 'MinGit' -and $_.delivery -eq 'download' })
    if($fallback.Count -ne 1) { return @{ready=$false;source='missing';network_required=$false;download_required=$false;availability='prerequisite_unverified'} }
    $cached=Join-Path $Target '.deployment/downloads/mingit.zip'
    Assert-NoReparse $cached
    if([IO.File]::Exists($cached)) {
        if((Get-Digest $cached) -cne $fallback[0].sha256) { Stop-Deployment 'git_cached_artifact_conflict' 4 }
        $zip=[IO.Compression.ZipFile]::OpenRead($cached)
        try {
            Inspect-Zip $zip
            if('cmd/git.exe' -notin @($zip.Entries.FullName)) { Stop-Deployment 'git_cached_layout_conflict' 4 }
        } finally { $zip.Dispose() }
        return @{ready=$true;source='verified_target_cache';network_required=$false;download_required=$false;availability='cached_for_bootstrap'}
    }
    $url=[string]$fallback[0].provenance_url
    try {
        $probe=if($NetworkProbe){& $NetworkProbe $url}else{Test-PrimaryGitSource $url}
        $reachable=($probe.reachable -eq $true)
    } catch { $reachable=$false }
    return @{ready=$reachable;source='pinned_primary';network_required=$true;download_required=$true;primary_url=$url;availability=$(if($reachable){'primary_reachable'}else{'primary_unverified'})}
}

function Invoke-Deployment([string]$Command,[string]$Destination,[string]$BindingName='', [string]$Action='Resume',[scriptblock]$NetworkProbe=$null) {
    try {
        if (-not [Environment]::Is64BitProcess -or $PSVersionTable.PSVersion -lt [Version]'5.1' -or [Environment]::OSVersion.Platform -ne 'Win32NT') { Stop-Deployment 'windows_x64_powershell51_required' 2 }
        $root=[IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\','/')
        $manifest=Read-DeploymentPackage $root
        $target=Assert-Target $Destination $root $manifest
        if ($Command -eq 'preflight') {
            $drive=[IO.DriveInfo]::new([IO.Path]::GetPathRoot($target))
            if ($drive.AvailableFreeSpace -lt 1000000000) { Stop-Deployment 'insufficient_free_space' 2 }
            $git=Get-PreflightGit $root $target $manifest $NetworkProbe
            $report=@{status='completed';code='preflight_verified';network_mode=$manifest.network_mode;host_activation='pending';destination=$target;git=$git}
            $exitCode=0
            if(-not $git.ready) { $report.status='pending';$report.code='git_download_unverified';$exitCode=2 }
            $report | ConvertTo-Json -Depth 8 | ForEach-Object { [Console]::Out.WriteLine($_) }
            return $exitCode
        }
        $metadata=Join-Path $target '.deployment'
        if ($Command -eq 'verify' -and -not [IO.File]::Exists((Join-Path $metadata 'owner.json'))) { Stop-Deployment 'bootstrap_required' 2 }
        $nativeLock=Join-Path $metadata 'runtime.lock'
        if (Test-Path -LiteralPath $nativeLock) {
            if ($Command -ne 'recover') { Stop-Deployment 'runtime_lock_requires_recovery' 4 }
            Assert-NoReparse $nativeLock
            $pidValue=[int]([IO.File]::ReadAllText($nativeLock))
            $process=Get-Process -Id $pidValue -ErrorAction SilentlyContinue
            if ($process) { Stop-Deployment 'runtime_writer_still_live' 4 }
            Remove-Item -LiteralPath $nativeLock
        }
        if ($Command -eq 'recover' -and $Action -eq 'DiscardStaging') {
            $removed=@(Remove-VerifiedStaging $root $target $manifest)
            @{status='completed';code='verified_staging_discarded';stages_removed=$removed} | ConvertTo-Json | ForEach-Object { [Console]::Out.WriteLine($_) }
            return 0
        }
        [IO.Directory]::CreateDirectory($metadata) | Out-Null
        $ownerPath=Join-Path $metadata 'owner.json'
        if (-not [IO.File]::Exists($ownerPath)) { Write-NewJson $ownerPath @{ package_id=$manifest.package_id; manifest_sha256=(Get-Digest (Join-Path $root 'manifest.json')); target=$target } }
        $lockStream=[IO.File]::Open($nativeLock,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
        $lockBytes=[Text.Encoding]::ASCII.GetBytes([string]$PID);$lockStream.Write($lockBytes,0,$lockBytes.Length);$lockStream.Dispose()
        try {
            $python=Get-DeploymentPython $root $target $manifest $Command
            $script=Join-Path $root 'tools/deploy.py'
            $arguments=@('-I','-B',$script,$Command,'--package',$root,'--destination',$target)
            if ($BindingName) { $arguments+=@('--binding-name',$BindingName) }
            if ($Command -eq 'recover') { $arguments+=@('--action',$Action) }
            & $python @arguments | ForEach-Object { [Console]::Out.WriteLine($_) }
            return $LASTEXITCODE
        } finally { Remove-Item -LiteralPath $nativeLock }
    } catch {
        $exitCode=5
        if ($_.Exception.Data.Contains('deployment_exit')) { $exitCode=[int]$_.Exception.Data['deployment_exit'] }
        @{status='blocked';code=$_.Exception.Message;diagnostic=$_.ToString()} | ConvertTo-Json -Compress | ForEach-Object { [Console]::Out.WriteLine($_) }
        return $exitCode
    }
}
