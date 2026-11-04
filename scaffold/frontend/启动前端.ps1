# 启动前端：Vite @ http://localhost:5173
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

Write-Host "[*] 工作目录: $here" -ForegroundColor Cyan

# 1) 依赖检查
if (-not (Test-Path (Join-Path $here "node_modules"))) {
    Write-Host "[!] 缺少 node_modules，正在安装依赖..." -ForegroundColor Yellow
    npm install
}

# 2) 清理 Vite 监听会踩到的残留临时目录（会导致 EBUSY 崩溃）
$tmpDirs = Get-ChildItem -LiteralPath $here -Recurse -Force -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like '*.tmpdir' }
if ($tmpDirs) {
    Write-Host ("[*] 清理残留临时目录 {0} 个" -f @($tmpDirs).Count) -ForegroundColor Yellow
    $tmpDirs | ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
}

# 3) 端口占用检查
$busy = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
if ($busy) {
    Write-Host ("[X] 5173 已被占用 (PID={0})" -f $busy[0].OwningProcess) -ForegroundColor Red
    Write-Host "    先停掉它，或确认是不是已经启动过前端了" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] 启动中，稍等几秒后访问 http://localhost:5173" -ForegroundColor Green
Write-Host "     (Ctrl+C 停止)" -ForegroundColor DarkGray
npm run dev
