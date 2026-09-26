@echo off
REM Create/activate the venv and install deps. Usage: setup.bat
cd /d "%~dp0"

if not exist pyvenv.cfg python -m venv .
call Scripts\activate.bat
pip install -q -r requirements.txt
