#!/bin/bash
cd "$(dirname "$0")"

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi

PYTHON=""
if [ -x "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
elif [ -x "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    echo "ERROR: Python 3 is not installed."
    exit 1
fi

echo "============================================"
echo "  RI ENTERPRISES Website Starting..."
echo "  Open: http://127.0.0.1:5000"
echo "  Press Ctrl+C to stop the server"
echo "============================================"
echo

"$PYTHON" app.py
