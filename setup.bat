@echo off
REM Create/activate the venv, install deps, then download and unzip the datasets. Usage: setup.bat
cd /d "%~dp0"

echo Setting up the development environment...
if not exist .venv\pyvenv.cfg python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt

git lfs version >nul 2>nul || echo Git LFS is not installed, installing for you and extracting datasets
git lfs install
git lfs pull
if not exist "datasets\Final Tree" tar -xf "datasets\Final Tree.zip" -C datasets
if not exist "datasets\Extra Data" tar -xf "datasets\Extra Data.zip" -C datasets