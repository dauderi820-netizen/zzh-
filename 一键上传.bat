@echo off
cd /d "%~dp0"
set GIT="D:\Git\cmd\git.exe"

echo.
echo [1/3] Adding changes...
%GIT% add -A

echo [2/3] Committing...
%GIT% commit -m "update: %date% %time%"
if errorlevel 1 echo (nothing new to commit)

echo [3/3] Pushing to GitHub...
%GIT% push

echo.
echo ================== DONE ==================
pause
