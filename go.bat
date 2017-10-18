@echo off

set "tmpfile=%TEMP%\go%RANDOM%.tmp"

py C:\Users\diego\.cmder\bin\go.py --out-dir-file="%tmpfile%" %*

if exist "%tmpfile%" (
    :: THOSE LINES ARE ESSENTIAL.... BUT WHY ?????????????????? Fuck.
    goto wtf
    :wtf
    :: read the output dir to go 
    set /p d=<"%tmpfile%"
    :: delete the temp file so it doesn't interfere for the next go
    del "%tmpfile%"
    :: Move !
    cd %d%
)
