$ProgressPreference = 'Continue'
$VerbosePreference = 'Continue'
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
Set-StrictMode -Version 2.0

[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor 'Tls12'

New-Variable -Name curdir  -Option Constant -Value $PSScriptRoot
Write-Host "[INFO] curdir: $curdir"

If ($args.Count -eq 0)
{
    Write-Error 'first arg must be a file'
}

If (-Not (Test-Path -LiteralPath $args[0]))
{
    Write-Error 'first arg must be a file'
}

New-Variable -Name logs_file  -Option Constant -Value (Join-Path -Path $curdir -ChildPath $args[0])
New-Variable -Name tmp_file  -Option Constant -Value (New-TemporaryFile)

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'Channel error on connection' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'channel exception' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'accepting AMQP connection' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'has a client-provided name' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'granted access to' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'closing AMQP connection' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file

& rg.exe --no-ignore --hidden --fixed-strings --no-line-number --invert-match 'pending publisher confirms' $logs_file > $tmp_file
Move-Item -Force $tmp_file $logs_file
