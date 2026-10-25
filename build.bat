@echo off
REM Build the active C file as a DLL, for VS Code Ctrl+Shift+B use.
REM Run from a VS 2010 command prompt, or after vcvarsall.bat amd64,
REM so cl matches 64-bit Python. Usage: build.bat RowsCheck.c
if "%1"=="" echo Usage: build.bat file.c & exit /b 1
call vcvarsall.bat amd64
if errorlevel 1 exit /b 1
cl /LD %1
