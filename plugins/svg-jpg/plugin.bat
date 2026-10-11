@echo off
set "TOOL=%~1"
set "INPUT_FILE=%~2"
set "OUTPUT_FILE=%~3"
set "WIDTH_OPT="

if not "%~4"=="" if not "%~4"=="None" if not "%~4"=="{width}" (
    set "WIDTH_OPT=--width %~4"
)

python "%~dp0plugin.py" "%TOOL%" "%INPUT_FILE%" "%OUTPUT_FILE%" %WIDTH_OPT%
