#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements-render.txt
python scripts/download_flower_model.py
