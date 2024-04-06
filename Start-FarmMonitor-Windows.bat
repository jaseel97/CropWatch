@REM @echo off
@REM start cmd /k python app.py
@REM timeout /t 5
@REM start http://localhost:5000

@echo off
tasklist /FI "IMAGENAME eq python.exe" /FO CSV > python_processes.txt

findstr /i "app.py" python_processes.txt > nul
if errorlevel 1 (
    start cmd /k "python app.py"
)

findstr /i "TrackerServer.py" python_processes.txt > nul
if errorlevel 1 (
    start cmd /k "python TrackerServer.py"
)

findstr /i "SensorServer.py" python_processes.txt > nul
if errorlevel 1 (
    start cmd /k "python SensorServer.py"
)

timeout /t 5
start "" "templates\menu.html"
@REM start http://localhost:5000
del python_processes.txt

