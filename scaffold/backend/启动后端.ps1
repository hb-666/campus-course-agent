# Start backend: FastAPI @ http://127.0.0.1:8000
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

$py = Join-Path $here ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "[X] venv not found: $py" -ForegroundColor Red
    Write-Host "    rebuild: uv venv --python 3.12 .venv" -ForegroundColor Yellow
    Write-Host "    deps   : uv pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] interpreter: $py" -ForegroundColor Cyan
& $py -m uvicorn app.main:app --reload --port 8000
