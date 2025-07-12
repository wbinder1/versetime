#!/bin/bash

# Raspberry Pi VerseTime Setup Script
# This script sets up the VerseTime display on a Raspberry Pi

echo "Setting up VerseTime for Raspberry Pi..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required Python packages
echo "Installing Python dependencies..."
sudo apt-get install -y python3 python3-pip

# Install additional packages for better display
sudo apt-get install -y python3-tk  # For GUI support if needed
sudo apt-get install -y fonts-liberation  # Better font support

# Make the main script executable
chmod +x raspberry_pi_versetime.py

# Create a desktop shortcut (optional)
if [ -d ~/Desktop ]; then
    echo "Creating desktop shortcut..."
    cat > ~/Desktop/VerseTime.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=VerseTime
Comment=Bible verses with current time
Exec=python3 $(pwd)/raspberry_pi_versetime.py
Icon=accessories-text-editor
Terminal=true
Categories=Utility;
EOF
    chmod +x ~/Desktop/VerseTime.desktop
fi

# Create a systemd service for auto-start (optional)
echo "Creating systemd service for auto-start..."
sudo tee /etc/systemd/system/versetime.service > /dev/null << EOF
[Unit]
Description=VerseTime Bible Verse Display
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/raspberry_pi_versetime.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable the service (optional - uncomment if you want auto-start)
# sudo systemctl enable versetime.service

echo ""
echo "Setup complete!"
echo ""
echo "To run VerseTime manually:"
echo "  python3 raspberry_pi_versetime.py"
echo ""
echo "To start the service automatically on boot:"
echo "  sudo systemctl enable versetime.service"
echo ""
echo "To start the service now:"
echo "  sudo systemctl start versetime.service"
echo ""
echo "To check service status:"
echo "  sudo systemctl status versetime.service" 