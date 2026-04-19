@echo off
chcp 65001 >nul
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

:: runtime paths
set "PYTHON=%ROOT%runtime\python\python.exe"
set "PYTHONPATH=%ROOT%runtime\python\Lib\site-packages"
set "PATH=%ROOT%runtime\nodejs;%PATH%"

:: add source to python path
set "PYTHONPATH=%PYTHONPATH%;%ROOT%deeptutor-src"

:: user data directory
set "USER_DATA=%ROOT%workspace\data"
if not exist "%USER_DATA%" mkdir "%USER_DATA%"

:: check .env config
if not exist "%ROOT%configs\.env" (
    echo [ERROR] configs\.env not found
    echo Please copy configs\.env.example to configs\.env and fill in your API Key
    pause
    exit /b 1
)

:: write frontend api config
echo NEXT_PUBLIC_API_BASE=http://localhost:8001 > "%ROOT%deeptutor-src\web\.env.local"

:: start backend
echo [1/2] Starting backend service on port 8001...
start "DeepTutor Backend" /d "%ROOT%deeptutor-src" "%PYTHON%" -m deeptutor.api.run_server

:: wait for backend
timeout /t 5 /nobreak >nul

:: start frontend
echo [2/2] Starting frontend service on port 3782...
start "DeepTutor Frontend" /d "%ROOT%deeptutor-src\web" npm.cmd run dev -- --port 3782

echo.
echo ========================================
echo  DeepTutor Started!
echo  Backend:  http://localhost:8001
echo  Frontend: http://localhost:3782
echo ========================================
echo.
pause