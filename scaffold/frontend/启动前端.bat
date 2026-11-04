@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0启动前端.ps1"
echo.
echo 前端已停止，按任意键关闭窗口...
pause >nul
