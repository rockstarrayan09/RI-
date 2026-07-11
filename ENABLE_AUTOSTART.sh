#!/bin/bash
cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"
PLIST="$HOME/Library/LaunchAgents/com.ri-enterprises.website.plist"
START_SCRIPT="$PROJECT_DIR/START_WEBSITE.sh"

chmod +x "$START_SCRIPT"

PYTHON=""
if [ -x "$PROJECT_DIR/venv/bin/python3" ]; then
    PYTHON="$PROJECT_DIR/venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
else
    echo "ERROR: Python 3 is not installed."
    exit 1
fi

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ri-enterprises.website</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>$PROJECT_DIR/app.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/data/website.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/data/website-error.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"

echo "SUCCESS: Website will start automatically when macOS turns on."
echo "Launch agent: $PLIST"
