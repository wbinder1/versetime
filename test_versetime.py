#!/usr/bin/env python3
"""
Test script for VerseTime Raspberry Pi program
"""

import sys
import os

# Add current directory to path so we can import the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from raspberry_pi_versetime import VerseTimeDisplay
    print("✓ Successfully imported VerseTimeDisplay")
except ImportError as e:
    print(f"✗ Failed to import VerseTimeDisplay: {e}")
    sys.exit(1)

def test_verse_loading():
    """Test that verses are loaded correctly"""
    print("\nTesting verse loading...")
    
    display = VerseTimeDisplay()
    
    if not display.verses_cache:
        print("✗ No verses loaded")
        return False
    
    print(f"✓ Loaded {len(display.verses_cache)} verses")
    
    # Test getting a random verse
    verse = display.get_random_verse()
    if verse:
        print(f"✓ Random verse: {verse['book']} {verse['chapter']}:{verse['verse']}")
        print(f"  Text: {verse['text'][:50]}...")
    else:
        print("✗ Failed to get random verse")
        return False
    
    # Test getting time-based verse
    verse = display.get_time_based_verse()
    if verse:
        print(f"✓ Time-based verse: {verse['book']} {verse['chapter']}:{verse['verse']}")
        print(f"  Text: {verse['text'][:50]}...")
    else:
        print("✗ Failed to get time-based verse")
        return False
    
    return True

def test_time_formatting():
    """Test time and date formatting"""
    print("\nTesting time formatting...")
    
    display = VerseTimeDisplay()
    
    time_str = display.format_time()
    date_str = display.format_date()
    
    print(f"✓ Time format: {time_str}")
    print(f"✓ Date format: {date_str}")
    
    return True

def test_display():
    """Test the display function"""
    print("\nTesting display function...")
    
    display = VerseTimeDisplay()
    verse = display.get_random_verse()
    
    if verse:
        print("✓ Displaying a sample verse:")
        display.display_verse(verse)
        return True
    else:
        print("✗ No verse to display")
        return False

def main():
    """Run all tests"""
    print("VerseTime Raspberry Pi Test Suite")
    print("=" * 40)
    
    tests = [
        ("Verse Loading", test_verse_loading),
        ("Time Formatting", test_time_formatting),
        ("Display Function", test_display)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✓ {test_name} test passed")
                passed += 1
            else:
                print(f"✗ {test_name} test failed")
        except Exception as e:
            print(f"✗ {test_name} test failed with error: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! VerseTime is ready to use.")
        print("\nTo run VerseTime:")
        print("  python3 raspberry_pi_versetime.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 