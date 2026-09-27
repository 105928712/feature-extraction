# Create/activate the venv and install deps. Usage: . .\setup.ps1
$venv = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path "$venv\pyvenv.cfg")) { python -m venv $venv }
. "$venv\Scripts\Activate.ps1"
pip install -q -r (Join-Path $PSScriptRoot "requirements.txt")