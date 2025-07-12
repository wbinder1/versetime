# VerseTime for Raspberry Pi

A Python application that displays Bible verses with the current time, similar to [versetime.net](https://versetime.net/). This program is designed to run on a Raspberry Pi and can be used as a digital clock with Bible verses.

## Features

- Displays current time and date
- Shows Bible verses from the King James Version (KJV)
- Time-based verse selection (different verse for each minute)
- Clean, readable terminal display
- Auto-start capability with systemd service
- Desktop shortcut creation

## Requirements

- Raspberry Pi (any model)
- Raspberry Pi OS (formerly Raspbian)
- Python 3.6 or higher
- KJV Bible data (included in this repository)

## Installation

### Quick Setup

1. **Clone or download this repository to your Raspberry Pi:**
   ```bash
   git clone https://github.com/wbinder1/versetime.git
   cd versetime
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup_raspberry_pi.sh
   ./setup_raspberry_pi.sh
   ```

The setup script will:
- Update system packages
- Install required Python dependencies
- Make the main script executable
- Create a desktop shortcut
- Create a systemd service for auto-start

### Manual Setup

If you prefer to set up manually:

1. **Install Python dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. **Make the script executable:**
   ```bash
   chmod +x raspberry_pi_versetime.py
   ```

## Usage

### Running Manually

To run VerseTime manually:

```bash
python3 raspberry_pi_versetime.py
```

### Auto-Start Service

To enable VerseTime to start automatically on boot:

```bash
sudo systemctl enable versetime.service
sudo systemctl start versetime.service
```

To check the service status:

```bash
sudo systemctl status versetime.service
```

To stop the service:

```bash
sudo systemctl stop versetime.service
```

## How It Works

1. **Verse Loading:** The program loads all verses from the KJV Bible into memory on startup
2. **Time-Based Selection:** Each minute, a different verse is selected based on the current time
3. **Display:** The current time, date, and selected verse are displayed in a formatted layout
4. **Auto-Refresh:** The display updates every minute automatically

## Display Format

The program displays:
- Current time (12-hour format with AM/PM)
- Current date (full format)
- Bible reference (Book Chapter:Verse)
- Verse text (formatted with proper line breaks)

Example output:
```
================================================================================
                    VERSE TIME
================================================================================

                         2:30 PM

                Monday, January 15, 2024

          Psalms 1:1

          Blessed is the man that walketh not in the counsel of the ungodly, 
          nor standeth in the way of sinners, nor sitteth in the seat of the 
          scornful.

================================================================================
                    Press Ctrl+C to exit
================================================================================
```

## Customization

### Changing Bible Version

To use a different Bible version, modify the `bible_path` parameter in the `VerseTimeDisplay` class:

```python
display = VerseTimeDisplay(bible_path="bibles/en-asv")  # American Standard Version
```

Available versions in this repository:
- `en-kjv` - King James Version
- `en-asv` - American Standard Version
- `en-bsb` - Berean Study Bible
- And many more...

### Display Options

You can customize the display by modifying the `display_verse` method:
- Change the update interval (currently 60 seconds)
- Modify the display format
- Add or remove time/date display
- Change the verse selection algorithm

## Troubleshooting

### Common Issues

1. **"Bible path not found" error:**
   - Make sure the `bibles/en-kjv` directory exists
   - Check that the Bible data files are properly downloaded

2. **Permission denied errors:**
   - Make sure the script is executable: `chmod +x raspberry_pi_versetime.py`
   - Run setup script with proper permissions

3. **Service won't start:**
   - Check service status: `sudo systemctl status versetime.service`
   - View logs: `sudo journalctl -u versetime.service`

### Performance

- The program loads all verses into memory on startup
- Memory usage is approximately 50-100MB depending on Bible version
- CPU usage is minimal (only updates once per minute)

## License

This project uses Bible text that is in the public domain. The program code is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the program.

## Support

For issues or questions, please check the troubleshooting section above or create an issue in the repository. 