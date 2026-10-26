@echo off
REM Build the C gears DLL for the Iscandar engine.
REM Run from the engine folder, after vcvarsall.bat x86 (so cl is
REM on PATH). Step 1 regenerates status.h from Status.py, so the
REM C gears can never build against stale status codes; step 2
REM compiles the gears and the commit path into one DLL.
REM   python gen_status.py
REM   cl /LD RowsCheck.c PlanesCheck.c PairsRowDriver.c PlaneSmallDriver.c LargePlanesDriver.c LargeRowsDriver.c Mark.c Unmark.c Commit.c
python gen_status.py
if errorlevel 1 exit /b 1
cl /LD RowsCheck.c PlanesCheck.c PairsRowDriver.c PlaneSmallDriver.c LargePlanesDriver.c LargeRowsDriver.c Mark.c Unmark.c Commit.c
