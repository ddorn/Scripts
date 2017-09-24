@echo off

py C:\Users\diego\.cmder\bin\go.py %* --out-dir-file=C:\Users\diego\.cmder\bin\temp.txt

if exist C:\Users\diego\.cmder\bin\temp.txt ( 
    :: read the output dir to go 
    set /p d=< C:\Users\diego\.cmder\bin\temp.txt
    :: delete the temp file so it doesn't interfere for the next go
    del C:\Users\diego\.cmder\bin\temp.txt
    :: Move !
    cd %d%
)