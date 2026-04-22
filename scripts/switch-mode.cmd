@echo off
set MODE=%1
if "%MODE%"=="" goto usage
powershell -ExecutionPolicy Bypass -File "%~dp0switch-mode.ps1" -Mode %MODE%
goto end
:usage
echo Usage: scripts\switch-mode.cmd demo^|local^|lens
:end
