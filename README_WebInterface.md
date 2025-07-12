# VerseTime Web Interface

A modern web interface for configuring and managing the VerseTime Raspberry Pi system. Accessible at `http://versetime.local` or `http://localhost:5000`.

## Features

### 🏠 Home Tab - VerseTime Configuration
- **Bible Version Selection**: Choose from multiple Bible translations (KJV, ASV, BSB, etc.)
- **Display Settings**: Configure time/date display, update intervals, and formatting
- **Time & Date Format**: Customize time and date display formats
- **Verse Selection**: Choose between time-based or random verse selection
- **Service Control**: Restart the VerseTime display service

### ⚙️ Settings Tab - System Management
- **System Information**: View Raspberry Pi model, memory, disk usage, and temperature
- **WiFi Management**: Scan and add new WiFi networks
- **System Services**: Monitor and control VerseTime services
- **Network Configuration**: View network status and access information
- **System Logs**: View recent system activity

## Installation

### Quick Setup

1. **Run the web interface setup script:**
   ```bash
   chmod +x setup_web_interface.sh
   ./setup_web_interface.sh
   ```

2. **Access the web interface:**
   - Local: `http://versetime.local` or `http://localhost:5000`
   - Network: `http://[RASPBERRY_PI_IP]:5000`

### Manual Setup

1. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-flask
   pip3 install -r requirements.txt
   ```

2. **Make the script executable:**
   ```bash
   chmod +x web_versetime.py
   ```

3. **Run the web interface:**
   ```bash
   python3 web_versetime.py
   ```

## Usage

### Home Tab - Configuration

#### Bible Version Selection
- Select from available Bible translations
- Changes take effect immediately
- Service automatically restarts to apply changes

#### Display Settings
- **Show Time**: Toggle time display on/off
- **Show Date**: Toggle date display on/off
- **Clear Screen**: Toggle screen clearing between updates
- **Update Interval**: Set how often verses change (10-3600 seconds)
- **Max Line Length**: Set maximum characters per line (40-120)

#### Time & Date Format
- **Time Format Options:**
  - 12-hour (2:30 PM)
  - 24-hour (14:30)
  - 12-hour with seconds (2:30:45 PM)
  - 24-hour with seconds (14:30:45)

- **Date Format Options:**
  - Full (Monday, January 15, 2024)
  - Short (January 15, 2024)
  - Numeric (01/15/2024)
  - ISO (2024-01-15)

#### Verse Selection
- **Time-based Selection**: Different verses based on current time
- **Display Title**: Customize the display title
- **Border Character**: Change the border character
- **Indent Size**: Adjust text indentation (5-20 spaces)

### Settings Tab - System Management

#### System Information
- **Model**: Raspberry Pi model information
- **Memory**: Total available RAM
- **Disk Usage**: Current disk space usage
- **Temperature**: Current CPU temperature

#### WiFi Management
- **Scan Networks**: Discover available WiFi networks
- **Add Network**: Add new WiFi networks with password
- **Network Status**: View current connection status

#### System Services
- **VerseTime Service**: Display service status
- **Web Interface**: Configuration portal status
- **Network**: WiFi connection status
- **Service Control**: Restart services or reboot system

#### Network Configuration
- **IP Address**: Current network IP
- **Hostname**: System hostname
- **Access URL**: Web interface access links
- **Network Status**: Connection type and signal strength

## API Endpoints

The web interface provides several API endpoints for programmatic access:

### Configuration
- `POST /api/update_config` - Update VerseTime configuration
- `GET /api/system_info` - Get system information

### WiFi Management
- `POST /api/add_wifi` - Add new WiFi network

### Service Control
- `POST /api/restart_service` - Restart VerseTime service

## Configuration File

The web interface manages the `config.py` file automatically. Manual editing is also supported:

```python
# Bible version to use
BIBLE_VERSION = "en-kjv"

# Display settings
UPDATE_INTERVAL = 60
SHOW_TIME = True
SHOW_DATE = True
CLEAR_SCREEN = True

# Format settings
TIME_FORMAT = "%I:%M %p"
DATE_FORMAT = "%A, %B %d, %Y"

# Verse selection
USE_TIME_BASED_SELECTION = True
DISPLAY_TITLE = "VERSE TIME"
BORDER_CHAR = "="
INDENT_SIZE = 10
```

## Services

The setup creates two systemd services:

### versetime.service
- Runs the main VerseTime display program
- Auto-starts on boot
- Restarts automatically if it fails

### versetime-web.service
- Runs the web interface
- Auto-starts on boot
- Provides configuration access

## Troubleshooting

### Web Interface Not Accessible
1. Check if the service is running:
   ```bash
   sudo systemctl status versetime-web.service
   ```

2. Check if port 5000 is open:
   ```bash
   sudo netstat -tlnp | grep :5000
   ```

3. Restart the service:
   ```bash
   sudo systemctl restart versetime-web.service
   ```

### Configuration Changes Not Applied
1. Check if the VerseTime service is running:
   ```bash
   sudo systemctl status versetime.service
   ```

2. Restart the service manually:
   ```bash
   sudo systemctl restart versetime.service
   ```

### WiFi Issues
1. Check WiFi adapter status:
   ```bash
   iwconfig
   ```

2. Scan for networks manually:
   ```bash
   sudo iwlist wlan0 scan
   ```

### Permission Issues
1. Ensure the user has proper permissions:
   ```bash
   sudo usermod -a -G sudo $USER
   ```

2. Check file permissions:
   ```bash
   ls -la web_versetime.py
   chmod +x web_versetime.py
   ```

## Security Considerations

- The web interface runs on port 5000 by default
- No authentication is implemented (add if needed for production)
- Consider using HTTPS for network access
- Restrict access to trusted networks

## Customization

### Adding New Bible Versions
1. Add Bible data to the `bibles/` directory
2. The web interface will automatically detect new versions
3. Restart the web service to see changes

### Custom Themes
Modify the CSS in `templates/base.html` to customize the appearance

### Additional Features
Extend the Flask application by adding new routes and templates

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review system logs: `sudo journalctl -u versetime-web.service`
3. Check service status: `./check_services.sh`
4. Restart all services: `./restart_all.sh`

## License

This web interface is provided as-is for educational and personal use. 