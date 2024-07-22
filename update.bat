

@echo off
setlocal enabledelayedexpansion

REM --- Configuration ---
set REPO_URL=https://github.com/WarzoneDevelopper/snake/edit/main/
set LOCAL_VERSION_FILE=version.txt
set REMOTE_VERSION_FILE=%REPO_URL%/version.txt
set MAIN_FILE=main.py
set REMOTE_MAIN_FILE=%REPO_URL%/main.py
set LOG_FILE=update_log.txt

REM --- Color Definitions ---
set COLOR_RESET=0
set COLOR_GREEN=2
set COLOR_RED=4
set COLOR_YELLOW=6
set COLOR_CYAN=3
set COLOR_WHITE=7

REM --- Functions ---
:print_info
    echo [INFO] %~1
    goto :eof

:print_success
    echo [SUCCESS] %~1
    goto :eof

:print_error
    echo [ERROR] %~1
    goto :eof

REM --- Start Log ---
echo Update started at %date% %time% > %LOG_FILE%

REM --- Check if curl is installed ---
where curl >nul 2>nul
if %errorlevel% neq 0 (
    call :print_error "curl is not installed. Please install curl and try again. (Exit Code: 1)"
    echo Error: curl is not installed. Please install curl and try again. (Exit Code: 1) >> %LOG_FILE%
    pause
    exit /b 1
)

REM --- Fetch remote version ---
call :print_info "Fetching remote version..."
curl -s -o remote_version.txt %REMOTE_VERSION_FILE%
if %errorlevel% neq 0 (
    call :print_error "Failed to fetch remote version. (Exit Code: 2)"
    echo Error: Failed to fetch remote version. (Exit Code: 2) >> %LOG_FILE%
    pause
    exit /b 2
)

REM --- Read remote version ---
set /p REMOTE_VERSION=<remote_version.txt

REM --- Read local version ---
if exist %LOCAL_VERSION_FILE% (
    set /p LOCAL_VERSION=<%LOCAL_VERSION_FILE%
) else (
    set LOCAL_VERSION=0
)

REM --- Compare versions ---
echo Local version: %LOCAL_VERSION%
echo Remote version: %REMOTE_VERSION%

if "%REMOTE_VERSION%" gtr "%LOCAL_VERSION%" (
    call :print_info "A new version is available. Starting update..."
    
    REM Simulate downloading with a progress bar
    for /L %%A in (1,1,100) do (
        set /a progress=%%A
        set /p="Updating... !progress!%% complete" <nul
        ping -n 2 >nul
        cls
    )
    
    call :print_info "Downloading new version of main.py..."
    curl -s -o %MAIN_FILE% %REMOTE_MAIN_FILE%
    if %errorlevel% neq 0 (
        call :print_error "Failed to download main.py. (Exit Code: 3)"
        echo Error: Failed to download main.py. (Exit Code: 3) >> %LOG_FILE%
        pause
        exit /b 3
    )

    REM --- Update local version file ---
    echo %REMOTE_VERSION% > %LOCAL_VERSION_FILE%
    call :print_success "Update successful! (Exit Code: 0)"
    echo Update successful! (Exit Code: 0) >> %LOG_FILE%
) else (
    call :print_info "No new version found. Your version is up to date. (Exit Code: 0)"
    echo No new version found. Your version is up to date. (Exit Code: 0) >> %LOG_FILE%
)

REM --- Cleanup ---
del remote_version.txt

REM --- End Log ---
echo Update finished at %date% %time% >> %LOG_FILE%
pause
exit /b 0
