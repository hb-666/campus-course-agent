# Start frontend: Vite @ http://localhost:5173
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

if (-not (Test-Path (Join-Path $here "node_modules"))) {
    Write-Host "[!] node_modules missing, run: npm install" -ForegroundColor Yellow
}
npm run dev
