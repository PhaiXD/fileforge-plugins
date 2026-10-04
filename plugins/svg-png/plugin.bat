@echo off
set TOOL=%1
set INPUT_FILE=%2
set OUTPUT_FILE=%3

:: Map width option if provided
set WIDTH=
if not "%~4"=="" if not "%~4"=="None" set WIDTH=--width %~4

python "%~dp0plugin.py" %TOOL% %INPUT_FILE% %OUTPUT_FILE% %WIDTH%
