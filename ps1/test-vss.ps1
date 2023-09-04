$ErrorActionPreference = 'Stop'
$DebugPreference = 'Continue'
$VerbosePreference = 'Continue'
Set-StrictMode -Version Latest -ErrorAction 'Stop'

$path = 'C:/Users/bakkenl/AppData/Roaming/RabbitMQ/log'

$directoryRoot = [System.IO.Directory]::GetDirectoryRoot($Path).ToString()
Write-Verbose -Message "directoryRoot: $directoryRoot"

$shadow = (Get-WmiObject -List Win32_ShadowCopy).Create($directoryRoot, "ClientAccessible")
$shadowCopy = Get-WmiObject Win32_ShadowCopy | ? { $_.ID -eq $shadow.ShadowID }
$snapshotPath = $shadowCopy.DeviceObject + "\" + $Path.Replace($directoryRoot, "")
