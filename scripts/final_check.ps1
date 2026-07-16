$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontendPath = Join-Path $projectRoot "frontend"
$backendPath = Join-Path $projectRoot "backend"


function Assert-LastExitCode {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Step
    )

    if ($LASTEXITCODE -ne 0) {
        throw "$Step gagal dengan exit code $LASTEXITCODE"
    }
}


Write-Host ""
Write-Host "1. Memeriksa Python virtual environment..."

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Python virtual environment tidak ditemukan: $pythonPath"
}


Write-Host ""
Write-Host "2. Menjalankan seluruh backend test..."

Push-Location $backendPath

try {
    & $pythonPath -m pytest -q
    Assert-LastExitCode -Step "Backend test"
}
finally {
    Pop-Location
}


Write-Host ""
Write-Host "3. Menjalankan frontend lint..."

Push-Location $frontendPath

try {
    & npm.cmd run lint
    Assert-LastExitCode -Step "Frontend lint"

    Write-Host ""
    Write-Host "4. Menjalankan frontend build..."

    & npm.cmd run build
    Assert-LastExitCode -Step "Frontend build"
}
finally {
    Pop-Location
}


Write-Host ""
Write-Host "5. Memeriksa whitespace Git..."

& git -C $projectRoot diff --check
Assert-LastExitCode -Step "Git diff check"


Write-Host ""
Write-Host "6. Menampilkan status Git..."

& git -C $projectRoot status --short
Assert-LastExitCode -Step "Git status"


Write-Host ""
Write-Host "Pemeriksaan final berhasil."
