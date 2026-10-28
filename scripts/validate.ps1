$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    Push-Location backend
    python -m compileall -q app
    python -m pytest -q
    Pop-Location
    Push-Location frontend
    npm run lint
    npm test
    npm run build
    Pop-Location
    terraform fmt -check -recursive terraform
    kubectl kustomize k8s/overlays/development | Out-Null
    Write-Host 'Local validation complete.'
} finally { Pop-Location }
