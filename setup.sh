#!/usr/bin/env bash
# Create/activate the venv and install deps. Usage: source setup.sh
SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ -f "$SETUP_DIR/.venv/pyvenv.cfg" ] || python3 -m venv "$SETUP_DIR/.venv" || return 1
source "$SETUP_DIR/.venv/bin/activate" || return 1
pip install -q -r "$SETUP_DIR/requirements.txt"

unset SETUP_DIR