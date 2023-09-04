$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 'Latest' -ErrorAction 'Stop' -Verbose

$Headers = @{
    Authorization = "Bearer $env:GITHUB_API_TOKEN";
    Accept = 'application/vnd.github+json';
    'X-GitHub-Api-Version' = '2022-11-28'
}

$uri = 'https://api.github.com/repos/rabbitmq/rabbitmq-server/issues/8691/reactions'

$result = Invoke-WebRequest -Method Get -Headers $Headers -URI $uri

$json = $result | ConvertFrom-Json

foreach ($i in $json)
{
    Write-Host $i.user.login
}
