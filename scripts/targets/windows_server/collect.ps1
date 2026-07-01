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
    if ($null -ne $minimumLength) {
        Add-Item -ItemId "W-09" -Title (Get-ItemTitle "W-09") -Evidence @{
            collection_status = "collected"
            minimum_password_length = $minimumLength
            maximum_password_age_days = $maximumAge
            minimum_password_age_days = $minimumAge
            password_history_size = $passwordHistory
        }
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
