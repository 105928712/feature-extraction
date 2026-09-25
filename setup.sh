#!/usr/bin/env bash
# Create/activate the venv and install deps. Usage: source setup.sh
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

[ -f pyvenv.cfg ] || python3 -m venv .
source bin/activate
pip install -q -r requirements.txt
