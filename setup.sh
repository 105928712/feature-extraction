#!/usr/bin/env bash
# Create/activate the venv, install deps, then download and unzip the datasets. Usage: source setup.sh
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Setting up the development environment..."
[ -f .venv/pyvenv.cfg ] || python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

git lfs version >/dev/null 2>&1 || echo "Git LFS is not installed, installing for you and extracting datasets"
git lfs install
git lfs pull
[ -d "datasets/Final Tree" ] || unzip -q "datasets/Final Tree.zip" -d datasets
[ -d "datasets/Extra Data" ] || unzip -q "datasets/Extra Data.zip" -d datasets
