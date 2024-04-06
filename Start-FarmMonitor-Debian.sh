#!/bin/bash

# Check if app.py is running
if ! pgrep -f "python3 app.py" > /dev/null; then
    echo "Starting app.py"
    python3 app.py &
fi

# Check if A.py is running
if ! pgrep -f "python3 TrackerServer.py" > /dev/null; then
    echo "Starting TrackerServer.py"
    python3 TrackerServer.py &
fi

# Check if B.py is running
if ! pgrep -f "python3 SensorServer.py" > /dev/null; then
    echo "Starting SensorServer.py"
    python3 SensorServer.py &
fi


html_file="templates/menu.html"

# Check if the file exists
if [ -f "$html_file" ]; then
    # Open the HTML file in the default web browser
    xdg-open "$html_file"
else
    echo "File not found: $html_file"
fi