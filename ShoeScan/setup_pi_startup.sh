#!/bin/bash

# Identify the absolute path of the current directory on the Pi
PROJECT_DIR="$(pwd)"

echo "Setting up ShoeScan autostart in directory: $PROJECT_DIR"

# Create the autostart directory if it doesn't exist
mkdir -p ~/.config/autostart

# Create the streamlit_startup.desktop file
cat <<EOF > ~/.config/autostart/streamlit_startup.desktop
[Desktop Entry]
Type=Application
Name=ShoeScan Streamlit Autostart
Comment=Launch ShoeScan Interface on boot
Exec=lxterminal -e "bash -c 'cd \"${PROJECT_DIR}\" && source venv/bin/activate && streamlit run frontend.py; exec bash'"
Terminal=false
EOF

echo "Successfully created ~/.config/autostart/streamlit_startup.desktop"
echo "You can now reboot your Raspberry Pi to test the startup script."
