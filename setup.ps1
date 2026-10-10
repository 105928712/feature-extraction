# Create/activate the venv, install deps, then download and unzip the datasets. Usage: . .\setup.ps1
Set-Location $PSScriptRoot

Write-Host "Setting up the development environment..."
if (-not (Test-Path .venv\pyvenv.cfg)) { python -m venv .venv }
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt

git lfs version *> $null; if ($LASTEXITCODE -ne 0) { Write-Host "Git LFS is not installed, installing for you and extracting datasets" }
git lfs install
git lfs pull
if (-not (Test-Path "datasets\Final Tree")) { tar -xf "datasets\Final Tree.zip" -C datasets }
if (-not (Test-Path "datasets\Extra Data")) { tar -xf "datasets\Extra Data.zip" -C datasets }
