[CmdletBinding()]
param(
    [switch]$Pretty
)

$targetScript = Join-Path $PSScriptRoot "..\targets\windows_server\collect.ps1"
Write-Warning "scripts/windows/collect.ps1 is deprecated. Use scripts/targets/windows_server/collect.ps1 for target Windows Server collection."

if ($Pretty) {
    & $targetScript -Pretty
}
else {
    & $targetScript
}
