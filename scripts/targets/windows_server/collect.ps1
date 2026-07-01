[CmdletBinding()]
param(
    [switch]$Pretty
)

$ErrorActionPreference = "Continue"
$items = New-Object System.Collections.Generic.List[object]
$collectedAt = (Get-Date).ToUniversalTime().ToString("o")
$seen = @{}
$windowsItems = 1..64 | ForEach-Object {
    $itemId = "W-{0:00}" -f $_
    @{ ItemId = $itemId; Title = "Windows Server item $itemId" }
}

function Add-Item {
    param(
        [Parameter(Mandatory = $true)][string]$ItemId,
        [Parameter(Mandatory = $true)][string]$Title,
        [Parameter(Mandatory = $true)][hashtable]$Evidence
    )

    $seen[$ItemId] = $true
    $items.Add([ordered]@{
        item_id = $ItemId
        title = $Title
        evidence = $Evidence
    })
}

function Get-ItemTitle {
    param([Parameter(Mandatory = $true)][string]$ItemId)
    return "Windows Server item $ItemId"
}

function Read-RegistryDword {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Name
    )
    try {
        $value = (Get-ItemProperty -LiteralPath $Path -Name $Name -ErrorAction Stop).$Name
        return [int]$value
    }
    catch {
        return $null
    }
}

function Get-NetAccountsValue {
    param(
        [string[]]$Lines,
        [string[]]$Labels
    )
    foreach ($line in $Lines) {
        foreach ($label in $Labels) {
            if ($line -match ([regex]::Escape($label) + "\s*[:=]?\s*(\d+)")) {
                return [int]$Matches[1]
            }
        }
    }
    return $null
}

function Get-ServiceDisabledOrAbsent {
    param([Parameter(Mandatory = $true)][string]$Name)
    try {
        $service = Get-Service -Name $Name -ErrorAction SilentlyContinue
        if ($null -eq $service) {
            return $true
        }
        return [bool](($service.Status -ne "Running") -and ($service.StartType -eq "Disabled"))
    }
    catch {
        return $null
    }
}

function Get-SeceditValues {
    $values = @{}
    $tempFile = Join-Path $env:TEMP ("kcii-secedit-{0}.inf" -f ([Guid]::NewGuid().ToString("N")))
    try {
        secedit /export /cfg $tempFile /quiet | Out-Null
        if (Test-Path -LiteralPath $tempFile) {
            foreach ($line in Get-Content -LiteralPath $tempFile -ErrorAction SilentlyContinue) {
                if ($line -match "^\s*([^=;]+?)\s*=\s*(.+?)\s*$") {
                    $values[$Matches[1].Trim()] = $Matches[2].Trim()
                }
            }
        }
    }
    catch {}
    finally {
        Remove-Item -LiteralPath $tempFile -Force -ErrorAction SilentlyContinue
    }
    return $values
}

function Get-IntValue {
    param(
        [hashtable]$Values,
        [string]$Key
    )
    if (-not $Values.ContainsKey($Key)) {
        return $null
    }
    $parsed = 0
    if ([int]::TryParse([string]$Values[$Key], [ref]$parsed)) {
        return $parsed
    }
    return $null
}

function Get-AuditPolicyCoreEnabled {
    try {
        $lines = @(auditpol /get /category:* 2>$null)
        if ($lines.Count -eq 0) {
            return $null
        }
        $required = @("Logon", "Account Management", "Policy Change", "System")
        foreach ($name in $required) {
            $line = $lines | Where-Object { $_ -match $name } | Select-Object -First 1
            if ($null -eq $line) {
                return $false
            }
            if (($line -notmatch "Success") -or ($line -notmatch "Failure")) {
                return $false
            }
        }
        return $true
    }
    catch {
        return $null
    }
}

function Get-EventLogSummary {
    try {
        $service = Get-Service -Name "EventLog" -ErrorAction Stop
        $logs = Get-WinEvent -ListLog Security,System,Application -ErrorAction Stop
        $minimumMb = [int](($logs | Measure-Object -Property MaximumSizeInBytes -Minimum).Minimum / 1MB)
        return @{
            service_running = [bool]($service.Status -eq "Running")
            minimum_size_mb = $minimumMb
            config_ok = [bool](($service.Status -eq "Running") -and ($minimumMb -ge 64))
        }
    }
    catch {
        return $null
    }
}

$seceditValues = Get-SeceditValues

try {
    $admin = Get-LocalUser -ErrorAction Stop | Where-Object { $_.SID.Value -match "-500$" } | Select-Object -First 1
    if ($null -eq $admin) {
        throw "Built-in Administrator account was not found"
    }
    Add-Item -ItemId "W-01" -Title (Get-ItemTitle "W-01") -Evidence @{
        collection_status = "collected"
        administrator_account_renamed = [bool]($admin.Name -ne "Administrator")
    }
}
catch {
    Add-Item -ItemId "W-01" -Title (Get-ItemTitle "W-01") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Administrator account rename status could not be collected"
    }
}

try {
    $guest = Get-LocalUser -ErrorAction Stop | Where-Object { $_.SID.Value -match "-501$" } | Select-Object -First 1
    if ($null -eq $guest) {
        throw "Built-in Guest account was not found"
    }
    Add-Item -ItemId "W-02" -Title (Get-ItemTitle "W-02") -Evidence @{
        collection_status = "collected"
        guest_account_enabled = [bool]$guest.Enabled
    }
}
catch {
    Add-Item -ItemId "W-02" -Title (Get-ItemTitle "W-02") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Guest account status could not be collected"
    }
}

$netAccounts = @()
try {
    $netAccounts = @(net accounts 2>$null)
}
catch {
    $netAccounts = @()
}

if ($netAccounts.Count -gt 0) {
    $lockoutThreshold = Get-NetAccountsValue -Lines $netAccounts -Labels @("Lockout threshold")
    if ($null -ne $lockoutThreshold) {
        Add-Item -ItemId "W-04" -Title (Get-ItemTitle "W-04") -Evidence @{
            collection_status = "collected"
            account_lockout_threshold = $lockoutThreshold
            account_lockout_threshold_ok = [bool](($lockoutThreshold -gt 0) -and ($lockoutThreshold -le 5))
        }
    }

    $lockoutDuration = Get-NetAccountsValue -Lines $netAccounts -Labels @("Lockout duration")
    $observationWindow = Get-NetAccountsValue -Lines $netAccounts -Labels @("Lockout observation window")
    if (($null -ne $lockoutDuration) -or ($null -ne $observationWindow)) {
        Add-Item -ItemId "W-08" -Title (Get-ItemTitle "W-08") -Evidence @{
            collection_status = "collected"
            account_lockout_duration_minutes = $lockoutDuration
            lockout_observation_window_minutes = $observationWindow
            account_lockout_duration_ok = [bool](($null -ne $lockoutDuration) -and ($null -ne $observationWindow) -and ($lockoutDuration -ge 60) -and ($observationWindow -ge 60))
        }
    }

    $minimumLength = Get-NetAccountsValue -Lines $netAccounts -Labels @("Minimum password length")
    $maximumAge = Get-NetAccountsValue -Lines $netAccounts -Labels @("Maximum password age")
    $minimumAge = Get-NetAccountsValue -Lines $netAccounts -Labels @("Minimum password age")
    $passwordHistory = Get-NetAccountsValue -Lines $netAccounts -Labels @("Length of password history maintained")
}

if ($null -eq $minimumLength) { $minimumLength = Get-IntValue -Values $seceditValues -Key "MinimumPasswordLength" }
if ($null -eq $maximumAge) { $maximumAge = Get-IntValue -Values $seceditValues -Key "MaximumPasswordAge" }
if ($null -eq $minimumAge) { $minimumAge = Get-IntValue -Values $seceditValues -Key "MinimumPasswordAge" }
if ($null -eq $passwordHistory) { $passwordHistory = Get-IntValue -Values $seceditValues -Key "PasswordHistorySize" }
$passwordComplexityValue = Get-IntValue -Values $seceditValues -Key "PasswordComplexity"
$passwordComplexityEnabled = $null
if ($null -ne $passwordComplexityValue) { $passwordComplexityEnabled = [bool]($passwordComplexityValue -ne 0) }
if ($null -ne $minimumLength) {
    $passwordPolicyOk = [bool](
        ($minimumLength -ge 8) -and
        ($passwordComplexityEnabled -eq $true) -and
        ($null -ne $maximumAge) -and ($maximumAge -gt 0) -and ($maximumAge -le 90) -and
        ($null -ne $minimumAge) -and ($minimumAge -ge 1) -and
        ($null -ne $passwordHistory) -and ($passwordHistory -ge 5)
    )
    Add-Item -ItemId "W-09" -Title (Get-ItemTitle "W-09") -Evidence @{
        collection_status = "collected"
        minimum_password_length = $minimumLength
        password_complexity_enabled = $passwordComplexityEnabled
        maximum_password_age_days = $maximumAge
        minimum_password_age_days = $minimumAge
        password_history_size = $passwordHistory
        password_policy_ok = $passwordPolicyOk
    }
}

try {
    $dontDisplay = Read-RegistryDword -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "dontdisplaylastusername"
    if ($null -ne $dontDisplay) {
        Add-Item -ItemId "W-10" -Title (Get-ItemTitle "W-10") -Evidence @{
            collection_status = "collected"
            last_username_hidden = [bool]($dontDisplay -eq 1)
        }
    }
}
catch {}

try {
    $limitBlankPasswordUse = Read-RegistryDword -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "LimitBlankPasswordUse"
    if ($null -ne $limitBlankPasswordUse) {
        Add-Item -ItemId "W-13" -Title (Get-ItemTitle "W-13") -Evidence @{
            collection_status = "collected"
            blank_password_remote_logon_blocked = [bool]($limitBlankPasswordUse -eq 1)
        }
    }
}
catch {}

try {
    $adminShareCount = 0
    $shares = @(Get-SmbShare -ErrorAction Stop)
    foreach ($share in $shares) {
        if ($share.Name -match '^(ADMIN\$|[A-Z]\$)$') {
            $adminShareCount += 1
        }
    }
    Add-Item -ItemId "W-17" -Title (Get-ItemTitle "W-17") -Evidence @{
        collection_status = "collected"
        default_admin_share_count = $adminShareCount
        default_admin_shares_disabled = [bool]($adminShareCount -eq 0)
    }
}
catch {
    Add-Item -ItemId "W-17" -Title (Get-ItemTitle "W-17") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "SMB share summary could not be collected"
    }
}

try {
    $remoteRegistryDisabled = Get-ServiceDisabledOrAbsent -Name "RemoteRegistry"
    if ($null -eq $remoteRegistryDisabled) {
        throw "RemoteRegistry service status could not be collected"
    }
    Add-Item -ItemId "W-18" -Title (Get-ItemTitle "W-18") -Evidence @{
        collection_status = "collected"
        remote_registry_service_disabled = $remoteRegistryDisabled
        unnecessary_services_disabled = $remoteRegistryDisabled
    }
}
catch {
    Add-Item -ItemId "W-18" -Title (Get-ItemTitle "W-18") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Service summary could not be collected"
    }
}

try {
    $ftpDisabled = Get-ServiceDisabledOrAbsent -Name "FTPSVC"
    if ($null -eq $ftpDisabled) {
        throw "FTP service status could not be collected"
    }
    Add-Item -ItemId "W-21" -Title (Get-ItemTitle "W-21") -Evidence @{
        collection_status = "collected"
        ftp_service_disabled = $ftpDisabled
    }
}
catch {
    Add-Item -ItemId "W-21" -Title (Get-ItemTitle "W-21") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "FTP service status could not be collected"
    }
}

try {
    $snmpDisabled = Get-ServiceDisabledOrAbsent -Name "SNMP"
    if ($null -eq $snmpDisabled) {
        throw "SNMP service status could not be collected"
    }
    Add-Item -ItemId "W-29" -Title (Get-ItemTitle "W-29") -Evidence @{
        collection_status = "collected"
        snmp_service_disabled = $snmpDisabled
    }
}
catch {
    Add-Item -ItemId "W-29" -Title (Get-ItemTitle "W-29") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "SNMP service status could not be collected"
    }
}

try {
    $telnet = Get-Service -Name "TlntSvr" -ErrorAction SilentlyContinue
    $telnetDisabled = $true
    if ($null -ne $telnet) {
        $telnetDisabled = [bool](($telnet.Status -ne "Running") -and ($telnet.StartType -eq "Disabled"))
    }
    Add-Item -ItemId "W-34" -Title (Get-ItemTitle "W-34") -Evidence @{
        collection_status = "collected"
        telnet_service_disabled = $telnetDisabled
    }
}
catch {
    Add-Item -ItemId "W-34" -Title (Get-ItemTitle "W-34") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Telnet service status could not be collected"
    }
}

try {
    $auditPolicyCoreEnabled = Get-AuditPolicyCoreEnabled
    if ($null -eq $auditPolicyCoreEnabled) {
        throw "Audit policy summary could not be collected"
    }
    Add-Item -ItemId "W-40" -Title (Get-ItemTitle "W-40") -Evidence @{
        collection_status = "collected"
        audit_policy_core_enabled = $auditPolicyCoreEnabled
    }
}
catch {
    Add-Item -ItemId "W-40" -Title (Get-ItemTitle "W-40") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Audit policy summary could not be collected"
    }
}

try {
    $eventLogSummary = Get-EventLogSummary
    if ($null -eq $eventLogSummary) {
        throw "Event log summary could not be collected"
    }
    Add-Item -ItemId "W-42" -Title (Get-ItemTitle "W-42") -Evidence @{
        collection_status = "collected"
        event_log_service_running = $eventLogSummary.service_running
        minimum_event_log_size_mb = $eventLogSummary.minimum_size_mb
        event_log_config_ok = $eventLogSummary.config_ok
    }
}
catch {
    Add-Item -ItemId "W-42" -Title (Get-ItemTitle "W-42") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Event log summary could not be collected"
    }
}

try {
    $profiles = Get-NetFirewallProfile -ErrorAction Stop
    Add-Item -ItemId "W-64" -Title (Get-ItemTitle "W-64") -Evidence @{
        collection_status = "collected"
        firewall_enabled = -not [bool]($profiles | Where-Object { -not $_.Enabled })
    }
}
catch {
    Add-Item -ItemId "W-64" -Title (Get-ItemTitle "W-64") -Evidence @{
        collection_status = "permission_denied_or_unavailable"
        manual_required = $true
        reason = "Firewall profile status could not be collected"
    }
}

foreach ($item in $windowsItems) {
    if (-not $seen.ContainsKey($item.ItemId)) {
        Add-Item -ItemId $item.ItemId -Title $item.Title -Evidence @{
            collection_status = "not_automated_by_windows_mvp"
            manual_required = $true
            reason = "official Windows Server item is registered, but collect.ps1 does not automate this item yet"
        }
    }
}

$orderedItems = New-Object System.Collections.Generic.List[object]
foreach ($item in $windowsItems) {
    foreach ($collectedItem in $items) {
        if ($collectedItem.item_id -eq $item.ItemId) {
            $orderedItems.Add($collectedItem)
            break
        }
    }
}

$payload = [ordered]@{
    schema_version = "kcii-windows-paste-v2"
    platform = "windows"
    guide_version = "kcii-2025-12"
    collected_at = $collectedAt
    items = $orderedItems
}

if ($Pretty) {
    $payload | ConvertTo-Json -Depth 6
}
else {
    $payload | ConvertTo-Json -Depth 6 -Compress
}
