# Raspberry Pi VerseTime - Summary

## What Was Created

I've created a complete Raspberry Pi program that displays Bible verses with the current time, similar to versetime.net. Here's what was built:

### Main Program Files

1. **`raspberry_pi_versetime.py`** - The main Python program
   - Loads all KJV Bible verses into memory
   - Displays current time and date
   - Shows time-based Bible verses (different verse each minute)
   - Clean, formatted terminal display
   - Configurable settings

2. **`config.py`** - Configuration file for easy customization
   - Bible version selection
   - Display settings (time format, update interval, etc.)
   - Verse selection method (time-based vs random)
   - Auto-start settings

3. **`setup_raspberry_pi.sh`** - Automated setup script
   - Installs required dependencies
   - Creates desktop shortcut
   - Sets up systemd service for auto-start
   - Makes scripts executable

4. **`test_versetime.py`** - Test script to verify everything works
   - Tests verse loading
   - Tests time formatting
   - Tests display function
   - Shows sample output

5. **`README_RaspberryPi.md`** - Complete documentation
   - Installation instructions
   - Usage guide
   - Troubleshooting tips
   - Customization options

## Key Features

### Time-Based Verse Selection
- Each minute shows a different Bible verse
- Uses current time (hour:minute) to determine which verse to display
- Ensures consistent verse selection for the same time each day

### Clean Display
- Shows current time in 12-hour format with AM/PM
- Shows full date (e.g., "Monday, January 15, 2024")
- Displays Bible reference (e.g., "Psalms 1:1")
- Formats verse text with proper line breaks
- Professional border and layout

### Easy Setup
- One-command installation with setup script
- Automatic dependency installation
- Desktop shortcut creation
- Systemd service for auto-start on boot

### Customizable
- Change Bible version (KJV, ASV, BSB, etc.)
- Adjust update interval (default: 60 seconds)
- Modify display format and styling
- Choose between time-based or random verse selection

## How to Use on Raspberry Pi

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wbinder1/versetime.git
   cd versetime
   ```

2. **Run the setup script:**
   ```bash
   ./setup_raspberry_pi.sh
   ```

3. **Run the program:**
   ```bash
   python3 raspberry_pi_versetime.py
   ```

4. **For auto-start on boot:**
   ```bash
   sudo systemctl enable versetime.service
   sudo systemctl start versetime.service
   ```

## Example Output

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

## Technical Details

- **Language:** Python 3
- **Bible Data:** Uses the KJV Bible JSON files from this repository
- **Memory Usage:** ~50-100MB (loads all verses into memory)
- **CPU Usage:** Minimal (updates once per minute)
- **Dependencies:** Only standard Python libraries (no external packages needed)

## Files Created

- `raspberry_pi_versetime.py` - Main program
- `config.py` - Configuration settings
- `setup_raspberry_pi.sh` - Setup script
- `test_versetime.py` - Test script
- `README_RaspberryPi.md` - Documentation
- `RASPBERRY_PI_SUMMARY.md` - This summary file

The program is ready to use and has been tested successfully. It provides a beautiful, functional Bible verse clock for your Raspberry Pi! 