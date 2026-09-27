@echo off
REM Create/activate the venv and install deps. Usage: setup.bat
cd /d "%~dp0"

if not exist .venv\pyvenv.cfg python -m venv .venv
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt