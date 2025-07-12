#!/usr/bin/env python3
"""
Raspberry Pi VerseTime Display
Displays Bible verses with the current time, similar to versetime.net
"""

import json
import os
import random
import time
from datetime import datetime
import glob

# Import configuration
try:
    from config import *
except ImportError:
    # Default configuration if config.py doesn't exist
    BIBLE_VERSION = "en-kjv"
    UPDATE_INTERVAL = 60
    SHOW_TIME = True
    SHOW_DATE = True
    CLEAR_SCREEN = True
    MAX_LINE_LENGTH = 70
    TIME_FORMAT = "%I:%M %p"
    DATE_FORMAT = "%A, %B %d, %Y"
    USE_TIME_BASED_SELECTION = True
    DISPLAY_TITLE = "VERSE TIME"
    BORDER_CHAR = "="
    INDENT_SIZE = 10

class VerseTimeDisplay:
    def __init__(self, bible_path=None):
        if bible_path is None:
            bible_path = f"bibles/{BIBLE_VERSION}"
        self.bible_path = bible_path
        self.verses_cache = []
        self.load_all_verses()
        
    def load_all_verses(self):
        """Load all verses from the KJV Bible into memory"""
        print("Loading Bible verses...")
        
        # Get all book directories
        books_path = os.path.join(self.bible_path, "books")
        if not os.path.exists(books_path):
            print(f"Error: Bible path not found: {books_path}")
            return
            
        book_dirs = [d for d in os.listdir(books_path) 
                    if os.path.isdir(os.path.join(books_path, d)) and not d.startswith('.')]
        
        total_verses = 0
        
        for book in book_dirs:
            book_path = os.path.join(books_path, book)
            chapter_files = glob.glob(os.path.join(book_path, "chapters", "*.json"))
            
            for chapter_file in chapter_files:
                try:
                    with open(chapter_file, 'r', encoding='utf-8') as f:
                        chapter_data = json.load(f)
                        
                    if 'data' in chapter_data:
                        for verse in chapter_data['data']:
                            # Clean up the verse text (remove footnotes)
                            text = verse.get('text', '')
                            # Remove footnote references like "1.1 ungodly: or, wicked"
                            if '.' in text and ':' in text:
                                parts = text.split('.')
                                if len(parts) > 1 and ':' in parts[1]:
                                    text = parts[0]
                            
                            if text.strip():
                                self.verses_cache.append({
                                    'book': verse.get('book', ''),
                                    'chapter': verse.get('chapter', ''),
                                    'verse': verse.get('verse', ''),
                                    'text': text.strip()
                                })
                                total_verses += 1
                                
                except Exception as e:
                    print(f"Error loading {chapter_file}: {e}")
                    continue
        
        print(f"Loaded {total_verses} verses from {len(book_dirs)} books")
    
    def get_random_verse(self):
        """Get a random verse from the loaded verses"""
        if not self.verses_cache:
            return None
        return random.choice(self.verses_cache)
    
    def get_time_based_verse(self):
        """Get a verse based on current time (hour:minute)"""
        if not self.verses_cache:
            return None
            
        now = datetime.now()
        # Use hour and minute to determine verse index
        time_index = (now.hour * 60 + now.minute) % len(self.verses_cache)
        return self.verses_cache[time_index]
    
    def get_verse(self):
        """Get a verse based on configuration settings"""
        if USE_TIME_BASED_SELECTION:
            return self.get_time_based_verse()
        else:
            return self.get_random_verse()
    
    def format_time(self):
        """Format current time in a readable format"""
        now = datetime.now()
        return now.strftime(TIME_FORMAT)
    
    def format_date(self):
        """Format current date in a readable format"""
        now = datetime.now()
        return now.strftime(DATE_FORMAT)
    
    def display_verse(self, verse, show_time=None, show_date=None):
        """Display a verse with time and date"""
        if not verse:
            print("No verse available")
            return
        
        # Use configuration defaults if not specified
        if show_time is None:
            show_time = SHOW_TIME
        if show_date is None:
            show_date = SHOW_DATE
            
        # Clear screen if configured
        if CLEAR_SCREEN:
            os.system('clear' if os.name == 'posix' else 'cls')
        
        border_line = BORDER_CHAR * 80
        indent = " " * INDENT_SIZE
        title_indent = " " * 20
        
        print(border_line)
        print(title_indent + DISPLAY_TITLE)
        print(border_line)
        print()
        
        if show_time:
            time_indent = " " * 25
            print(time_indent + self.format_time())
            print()
            
        if show_date:
            date_indent = " " * 20
            print(date_indent + self.format_date())
            print()
        
        print(indent + f"{verse['book']} {verse['chapter']}:{verse['verse']}")
        print()
        
        # Format the verse text with proper line breaks
        text = verse['text']
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= MAX_LINE_LENGTH:
                current_line += (" " + word) if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            print(indent + line)
        
        print()
        print(border_line)
        exit_indent = " " * 25
        print(exit_indent + "Press Ctrl+C to exit")
        print(border_line)

def main():
    """Main function to run the VerseTime display"""
    print("Starting VerseTime for Raspberry Pi...")
    
    # Initialize the display
    display = VerseTimeDisplay()
    
    if not display.verses_cache:
        print("Error: No verses loaded. Please check the Bible data path.")
        return
    
    print("VerseTime is ready! Displaying verses with current time...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Get a verse based on configuration
            verse = display.get_verse()
            
            # Display the verse
            display.display_verse(verse)
            
            # Wait before updating
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nExiting VerseTime...")
        print("Thank you for using VerseTime!")

if __name__ == "__main__":
    main() 