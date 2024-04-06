@echo off

REM Path to the Python installer
set python_installer="python-3.12.2-amd64.exe"

REM Install Python
echo Installing Python...
%python_installer% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0

REM Check if Python installation was successful
if %errorlevel% neq 0 (
    echo Python installation failed. Exiting...
    exit /b 1
)

REM Run python setup.py install for dependencies-win/setuptools-69.2.0
echo Installing dependencies for setuptools-69.2.0...
cd setuptools-69.2.0
python setup.py install
cd ..

REM Run python setup.py install for dependencies-win/pip24.0
echo Installing dependencies for pip24.0...
cd dependencies-win\pip24.0
python setup.py install
cd ..

REM Run pip install for requirements.txt
echo Installing requirements...
pip install --no-index --find-links dependencies-win -r requirements-win.txt

echo Installation complete.