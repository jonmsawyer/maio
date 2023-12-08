@echo off
for /f %%i in ('python -c "import sys; from conf import virtualenv; print(virtualenv.name)"') do set MAIO_ENV=%%i
workon %MAIO_ENV%
