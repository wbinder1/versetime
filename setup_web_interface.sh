#!/bin/bash

# VerseTime Web Interface Setup Script
# This script sets up the web interface and configures versetime.local domain

echo "Setting up VerseTime Web Interface..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y python3 python3-pip python3-flask
sudo apt-get install -y apache2-utils  # For password protection if needed
sudo apt-get install -y iwlist iwconfig  # For WiFi scanning
sudo apt-get install -y hostapd dnsmasq  # For WiFi hotspot (optional)

# Install Flask and other Python dependencies
echo "Installing Python dependencies..."
pip3 install flask

# Make the web script executable
chmod +x web_versetime.py

# Create systemd service for web interface
echo "Creating systemd service for web interface..."
sudo tee /etc/systemd/system/versetime-web.service > /dev/null << EOF
[Unit]
Description=VerseTime Web Interface
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/web_versetime.py
Restart=always
RestartSec=10
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Configure local domain (versetime.local)
echo "Configuring local domain..."

# Add entry to /etc/hosts
if ! grep -q "versetime.local" /etc/hosts; then
    echo "127.0.0.1 versetime.local" | sudo tee -a /etc/hosts
fi

# Configure Apache as reverse proxy (optional)
echo "Configuring Apache reverse proxy..."
sudo tee /etc/apache2/sites-available/versetime.conf > /dev/null << EOF
<VirtualHost *:80>
    ServerName versetime.local
    ServerAlias www.versetime.local
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    ErrorLog \${APACHE_LOG_DIR}/versetime_error.log
    CustomLog \${APACHE_LOG_DIR}/versetime_access.log combined
</VirtualHost>
EOF

# Enable required Apache modules
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite

# Enable the site
sudo a2ensite versetime.conf

# Disable default site
sudo a2dissite 000-default.conf

# Restart Apache
sudo systemctl restart apache2

# Enable and start the web service
echo "Enabling and starting web service..."
sudo systemctl enable versetime-web.service
sudo systemctl start versetime-web.service

# Create desktop shortcut for web interface
if [ -d ~/Desktop ]; then
    echo "Creating desktop shortcut for web interface..."
    cat > ~/Desktop/VerseTime-Web.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=VerseTime Web
Comment=VerseTime Web Configuration Interface
Exec=xdg-open http://versetime.local
Icon=text-html
Terminal=false
Categories=Network;WebBrowser;
EOF
    chmod +x ~/Desktop/VerseTime-Web.desktop
fi

# Create a simple status script
cat > check_services.sh << 'EOF'
#!/bin/bash
echo "=== VerseTime Services Status ==="
echo "Web Interface:"
sudo systemctl status versetime-web.service --no-pager -l
echo ""
echo "Display Service:"
sudo systemctl status versetime.service --no-pager -l
echo ""
echo "Apache Web Server:"
sudo systemctl status apache2 --no-pager -l
EOF

chmod +x check_services.sh

# Create a restart script
cat > restart_all.sh << 'EOF'
#!/bin/bash
echo "Restarting all VerseTime services..."
sudo systemctl restart versetime-web.service
sudo systemctl restart versetime.service
sudo systemctl restart apache2
echo "All services restarted!"
EOF

chmod +x restart_all.sh

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Web Interface is now available at:"
echo "  http://versetime.local"
echo "  http://localhost:5000"
echo ""
echo "Services created:"
echo "  - versetime.service (display service)"
echo "  - versetime-web.service (web interface)"
echo ""
echo "Useful commands:"
echo "  ./check_services.sh    - Check service status"
echo "  ./restart_all.sh       - Restart all services"
echo "  sudo systemctl status versetime-web.service  - Check web service"
echo ""
echo "To access the web interface from other devices on your network:"
echo "  http://[RASPBERRY_PI_IP]:5000"
echo ""
echo "The web interface allows you to:"
echo "  - Change Bible versions"
echo "  - Configure display settings"
echo "  - Add WiFi networks"
echo "  - Monitor system status"
echo "  - Restart services" 