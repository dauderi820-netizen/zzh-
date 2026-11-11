@echo off
cd /d "%~dp0"
set GIT="D:\Git\cmd\git.exe"
set PROXY=http://127.0.0.1:17891

echo.
echo [1/3] Adding changes...
%GIT% add -A

echo [2/3] Committing...
%GIT% commit -m "update: %date% %time%"
if errorlevel 1 echo (nothing new to commit)

echo [3/3] Pushing to GitHub...
%GIT% push
if errorlevel 1 (
  echo Direct connection failed, retrying via local proxy...
  %GIT% -c http.proxy=%PROXY% -c https.proxy=%PROXY% push
)

echo.
echo ================== DONE ==================
pause
