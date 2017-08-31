@echo off


if "%1"=="" (
    py C:\Users\diego\.cmder\bin\go.py
    goto :EOF
) 

if "%2" NEQ "" (
    py C:\Users\diego\.cmder\bin\go.py %*
    goto :EOF
)

py C:\Users\diego\.cmder\bin\go.py %1> C:\Users\diego\.cmder\bin\temp.txt
set /p d=< C:\Users\diego\.cmder\bin\temp.txt
del C:\Users\diego\.cmder\bin\temp.txt
cd %d%

:EOF