@echo off
if "%~1"=="" (
  echo Usage: scripts\ingest-lens.cmd "query text" [batch_size] [max_records]
  exit /b 1
)
set QUERY=%~1
set BATCH=%~2
if "%BATCH%"=="" set BATCH=25
set MAXREC=%~3
if "%MAXREC%"=="" set MAXREC=100
powershell -ExecutionPolicy Bypass -File "%~dp0ingest-lens.ps1" -Query "%QUERY%" -BatchSize %BATCH% -MaxRecords %MAXREC%
