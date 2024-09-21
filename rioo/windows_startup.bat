@echo off
set RETRY_COUNT=0
set MAX_RETRY=3
set LOGFILE=%USERPROFILE%\flask_ngrok_startup.log

:: Function to log messages
:log_message
echo %date% %time% - %1 >> %LOGFILE%
exit /b 0

:: Function to start Flask server in the background
:start_flask
set RETRY_COUNT=0
:flask_loop
if %RETRY_COUNT% geq %MAX_RETRY% (
    call :log_message "Flask failed to start after %MAX_RETRY% attempts."
    exit /b 1
)

call :log_message "Attempting to start Flask server on port 80..."
cd C:\path\to\your\flask\project
@REM call venv\Scripts\activate
start /B python run.py >nul 2>&1

:: Check if Flask started correctly
netstat -ano | findstr :80 >nul
if errorlevel 1 (
    call :log_message "Flask failed to start. Retrying..."
    set /a RETRY_COUNT+=1
    timeout /t 5 /nobreak
    goto flask_loop
) else (
    call :log_message "Flask server started successfully on port 80."
    exit /b 0
)

:: Function to start Ngrok in the background
:start_ngrok
set RETRY_COUNT=0
:ngrok_loop
if %RETRY_COUNT% geq %MAX_RETRY% (
    call :log_message "Ngrok failed to start after %MAX_RETRY% attempts."
    exit /b 1
)

call :log_message "Attempting to start Ngrok on port 80..."
start /B ngrok http 80 >nul 2>&1

:: Check if Ngrok started correctly
tasklist | findstr /I "ngrok.exe" >nul
if errorlevel 1 (
    call :log_message "Ngrok failed to start. Retrying..."
    set /a RETRY_COUNT+=1
    timeout /t 5 /nobreak
    goto ngrok_loop
) else (
    call :log_message "Ngrok started successfully."
    exit /b 0
)

:: Main Script
:start_process
call :log_message "Starting Flask and Ngrok..."
call :start_flask
if errorlevel 1 (
    call :log_message "Flask startup failed. Exiting..."
    exit /b 1
)
call :start_ngrok
if errorlevel 1 (
    call :log_message "Ngrok startup failed. Exiting..."
    exit /b 1
)

:: Keep the script alive and monitor services
call :log_message "Flask and Ngrok started successfully. Monitoring services..."
exit /b 0
