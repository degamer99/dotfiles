@echo off
rem —— determine where we were launched from ——
set "outDir=%~dp0"
set "outFile=%outDir%wifi_passwords.csv"

rem —— write CSV header ——
> "%outFile%" echo SSID,Password

rem —— loop over each wifi profile ——
for /f "skip=9 tokens=*" %%p in ('netsh wlan show profiles') do (
  rem only lines with "All User Profile     : <name>"
  echo %%p | findstr /r /c:"All User Profile *: " >nul || continue
  for /f "tokens=2,* delims=:" %%A in ("%%p") do (
    set "ssid=%%~B"
    call :trim ssid
    rem pull the clear‑text key
    for /f "skip=9 tokens=*" %%k in ('netsh wlan show profile name^="%ssid%" key^=clear') do (
      echo %%k | findstr /r /c:"Key Content *: " >nul || continue
      for /f "tokens=2,* delims=:" %%X in ("%%k") do (
        set "pass=%%~Y"
        call :trim pass
        rem append a line to CSV (quote SSID/password if they contain commas)
        call :quote ssid qssid
        call :quote pass qpass
        >> "%outFile%" echo %qssid%,%qpass%
      )
    )
  )
)
exit /b

:trim
  setlocal enabledelayedexpansion
  set "v=!%1!"
  rem remove leading spaces
  for /f "tokens=* delims= " %%i in ("!v!") do set "v=%%i"
  rem remove trailing spaces
  for /l %%i in (1,1,31) do if "!v:~-1!"==" " set "v=!v:~0,-1!"
  endlocal & set "%1=%v%"
exit /b

:quote
  rem wraps %1 into "%1%" if it contains a comma or quote
  setlocal enabledelayedexpansion
  set "t=!%1!"
  set "t=!t:"=""!"
  if "!t:,=!"=="!t!" (
    endlocal & set "%2=%t%"
  ) else (
    endlocal & set "%2=\"!t!\"%"
  )
exit /b
