param(
    [switch]$Debug = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = 'Stop'
Set-PSDebug -Off
Set-StrictMode -Version 'Latest' -ErrorAction 'Stop' -Verbose

if ($Debug) {
    $DebugPreference = 'Continue'
    Set-PSDebug -Strict -Trace 1
}

if ($Verbose) {
    $VerbosePreference = 'Continue'
}

New-Variable -Name erlangRegKeyPath -Option Constant `
    -Value 'HKLM:\SOFTWARE\WOW6432Node\Ericsson\Erlang'

New-Variable -Name erlangRegKey -Option Constant `
    -Value (Get-ChildItem $erlangRegKeyPath)

if ($erlangRegKey -eq $null) {
    Write-Error "Could not find Erlang installation registry key at $erlangRegKeyPath"
}

New-Variable -Name erts_version -Option Constant `
    -Value (Select-Object -InputObject $erlangRegKey -Last 1).PSChildName
Write-Verbose "erts_version: $erts_version"

New-Variable -Name erlangErtsRegKeyPath -Option Constant `
    -Value "HKLM:\SOFTWARE\WOW6432Node\Ericsson\Erlang\$erts_version"

New-Variable -Name erlangErtsRegKey -Option Constant `
    -Value (Get-ItemProperty -Path HKLM:\SOFTWARE\WOW6432Node\Ericsson\Erlang\$erts_version)

if ($erlangErtsRegKey -eq $null) {
    Write-Error "Could not find Erlang erts registry key at $erlangErtsRegKeyPath"
}

New-Variable -Name erlangProgramFilesPath -Option Constant `
    -Value ($erlangErtsRegKey.'(default)')

if (Test-Path -Path $erlangProgramFilesPath) {
    Write-Verbose "Erlang installation directory: '$erlangProgramFilesPath'"
}
else {
    Write-Error 'Could not find Erlang installation directory!'
}

New-Variable -Name allowedExes  -Option Constant -Value @('erl.exe', 'epmd.exe', 'werl.exe')

New-Variable -Name exes  -Option Constant -Value `
    $(Get-ChildItem -Filter '*.exe' -Recurse -Path $erlangProgramFilesPath | Where-Object { $_.Name -in $allowedExes })

foreach ($exe in $exes) {
    Write-Verbose "Updating or creating firewall rule for '$exe'"
    $fwRuleName = "rabbitmq-allow-$($exe.Name)"
    $fwParams = @{
        'Name' = $fwRuleName
        'DisplayName' = $fwRuleName
        'Direction' = 'In'
        'Program' = $exe
        'Profile' = 'any'
        'Enabled' = [Microsoft.PowerShell.Cmdletization.GeneratedTypes.NetSecurity.Enabled]::True
        'Action' = 'Allow'
    }
    if (!(Get-NetFirewallRule -ErrorAction 'SilentlyContinue'  -Name $fwRuleName)) {
        New-NetFirewallRule @fwParams
    }
    else {
        Set-NetFirewallRule @fwParams
    }
}
