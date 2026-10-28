#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="python"
else
    echo "[-] Error: Python 3 is not installed or not in PATH."
    exit 1
fi

"$PY_BIN" main.py "$@"

