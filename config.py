# VerseTime Configuration File
# Modify these settings to customize your VerseTime display

# Bible version to use
BIBLE_VERSION = "en-kjv"  # Options: en-kjv, en-asv, en-bsb, en-dra, etc.

# Display settings
UPDATE_INTERVAL = 60  # Seconds between updates (60 = 1 minute)
SHOW_TIME = True      # Display current time
SHOW_DATE = True      # Display current date
CLEAR_SCREEN = True   # Clear screen before each update

# Display formatting
MAX_LINE_LENGTH = 70  # Maximum characters per line for verse text
TIME_FORMAT = "%I:%M %p"  # Time format (12-hour with AM/PM)
DATE_FORMAT = "%A, %B %d, %Y"  # Date format

# Verse selection
USE_TIME_BASED_SELECTION = True  # Use time-based verse selection
# If False, will use random verse selection instead

# Auto-start settings
AUTO_START_ENABLED = False  # Set to True to enable auto-start service
SERVICE_NAME = "versetime"  # Systemd service name

# Logging
ENABLE_LOGGING = False  # Enable debug logging
LOG_FILE = "versetime.log"  # Log file path

# Display customization
DISPLAY_TITLE = "VERSE TIME"
BORDER_CHAR = "="
INDENT_SIZE = 10  # Number of spaces for indentation 