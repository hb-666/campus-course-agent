# Env self-check: which python, which venv, are deps present
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = Join-Path $here ".venv\Scripts\python.exe"

Write-Host "=== python on PATH ===" -ForegroundColor Cyan
(Get-Command python -ErrorAction SilentlyContinue).Source

Write-Host "`n=== project venv ===" -ForegroundColor Cyan
if (Test-Path $py) {
    & $py -c "import sys; print('exe    :', sys.executable); print('version:', sys.version.split()[0])"
    Write-Host "`n=== core deps ===" -ForegroundColor Cyan
    & $py -c "import fastapi, sqlalchemy, pymysql, bcrypt, jwt; print('fastapi/sqlalchemy/pymysql/bcrypt/jwt: OK')" 2>&1
    & $py -c "import fastmcp; print('fastmcp:', fastmcp.__version__)" 2>&1 | Select-String -Pattern "^fastmcp|Error"
} else {
    Write-Host "[X] venv missing, rebuild it" -ForegroundColor Red
}
