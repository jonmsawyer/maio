@echo off

rem # Get parent directory of the running script, regardless of where the
rem # script is being run from.
set MAIO_SCRIPTS_DIR=%~dp0

rem # Remove the trailing backslash off of the path (a \ will escape strings if
rem # we're not careful.
set MAIO_SCRIPTS_DIR=%MAIO_SCRIPTS_DIR:~0,-1%

rem # Get the parent directory of the parent directory of the running script.
for %%a in (%MAIO_SCRIPTS_DIR:~0,-1%) do set MAIO_BASE_DIR=%%~dpa

rem # Remove the trailing backslash off of the path (a \ will escape strings if
rem # we're not careful.
set MAIO_BASE_DIR=%MAIO_BASE_DIR:~0,-1%

rem # CD into the directory "to be safe" (not really necessary).
cd /d %MAIO_BASE_DIR%

rem # Get the Python Virtual Environment path for SMS project.
for /f %%i in ('python -c "import sys; sys.path.insert(0, r'%MAIO_BASE_DIR%'); from conf import virtualenv; print(virtualenv.path); "') do set MAIO_VENV_DIR=%%i

rem # Get the virtual environment name for the SMS project.
for /f %%j in ('python -c "import sys; sys.path.insert(0, r'%MAIO_BASE_DIR%'); from conf import virtualenv; print(virtualenv.name); "') do set MAIO_VENV=%%j

rem # Set the full path of the virtual environment for ease.
set VIRTUAL_ENV=%MAIO_VENV_DIR%\%MAIO_VENV%

rem # Backup the path just in case.
set _OLD_PATH=%PATH%

rem # Set the new path to be the virtual environment this script should run
rem # under.
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%

rem # Finally, properly send SMS alerts with proper context.
%VIRTUAL_ENV%\Scripts\python.exe %MAIO_BASE_DIR%\manage.py convert_videos %*

rem # Restore the old backed-up path.
set PATH=%_OLD_PATH%
