@echo off
setlocal enabledelayedexpansion

REM Configurations
set REPO_URL=https://github.com/WarzoneDevelopper/snake/edit/main/
set LOCAL_VERSION_FILE=version.txt
set REMOTE_VERSION_FILE=%REPO_URL%/version.txt
set MAIN_FILE=main.py
set REMOTE_MAIN_FILE=%REPO_URL%/main.py

REM Check if curl is installed
where curl >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: curl is not installed. Please install curl and try again. (Exit Code: 1)
    pause
    exit /b 1
)

REM Fetch remote version
curl -s -o remote_version.txt %REMOTE_VERSION_FILE%
if %errorlevel% neq 0 (
    echo Error: Failed to fetch remote version. (Exit Code: 2)
    pause
    exit /b 2
)

REM Read remote version
set /p REMOTE_VERSION=<remote_version.txt

REM Read local version
if exist %LOCAL_VERSION_FILE% (
    set /p LOCAL_VERSION=<%LOCAL_VERSION_FILE%
) else (
    set LOCAL_VERSION=0
)

REM Compare versions
echo Local version: %LOCAL_VERSION%
echo Remote version: %REMOTE_VERSION%

if "%REMOTE_VERSION%" gtr "%LOCAL_VERSION%" (
    echo Updating main.py to version %REMOTE_VERSION%...
    curl -s -o %MAIN_FILE% %REMOTE_MAIN_FILE%
    if %errorlevel% neq 0 (
        echo Error: Failed to update main.py. (Exit Code: 3)
        pause
        exit /b 3
    )
    REM Update local version file
    echo %REMOTE_VERSION% > %LOCAL_VERSION_FILE%
    echo Update successful! (Exit Code: 0)
) else (
    echo No update necessary. (Exit Code: 0)
)

REM Cleanup
del remote_version.txt

pause
exit /b 0

