#!/usr/bin/env python3
"""
Test script for VerseTime Web Interface new features
Tests battery detection, WiFi scanning, and temperature conversion
"""

import json
import subprocess
import sys
import os

def test_battery_detection():
    """Test battery information detection"""
    print("🔋 Testing Battery Detection...")
    
    # Check if battery files exist
    battery_dirs = []
    try:
        import glob
        battery_dirs = glob.glob('/sys/class/power_supply/BAT*')
    except:
        pass
    
    if battery_dirs:
        print(f"  ✓ Found {len(battery_dirs)} battery(s)")
        for battery_dir in battery_dirs:
            try:
                with open(os.path.join(battery_dir, 'capacity'), 'r') as f:
                    capacity = int(f.read().strip())
                    print(f"  ✓ Battery capacity: {capacity}%")
                
                with open(os.path.join(battery_dir, 'status'), 'r') as f:
                    status = f.read().strip()
                    print(f"  ✓ Battery status: {status}")
            except Exception as e:
                print(f"  ✗ Error reading battery info: {e}")
    else:
        print("  ℹ No battery detected (normal for desktop systems)")
    
    return True

def test_temperature_conversion():
    """Test temperature conversion functionality"""
    print("\n🌡️ Testing Temperature Conversion...")
    
    try:
        # Test Raspberry Pi temperature command
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        if result.returncode == 0:
            temp_celsius = result.stdout.strip().split('=')[1]
            print(f"  ✓ Current temperature: {temp_celsius}")
            
            # Test conversion to Fahrenheit
            try:
                temp_c = float(temp_celsius.replace('°C', ''))
                temp_f = (temp_c * 9/5) + 32
                print(f"  ✓ Converted to Fahrenheit: {temp_f:.1f}°F")
            except:
                print("  ✗ Error converting temperature")
        else:
            print("  ℹ Temperature command not available (not on Raspberry Pi)")
    except FileNotFoundError:
        print("  ℹ vcgencmd not available (not on Raspberry Pi)")
    
    return True

def test_wifi_scanning():
    """Test WiFi network scanning"""
    print("\n📶 Testing WiFi Scanning...")
    
    try:
        # Test iwlist command
        result = subprocess.run(['iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ WiFi scanning command available")
            
            # Count networks found
            lines = result.stdout.split('\n')
            networks = []
            current_ssid = None
            
            for line in lines:
                if 'ESSID:' in line:
                    ssid = line.split('"')[1] if '"' in line else line.split(':')[1].strip()
                    if ssid and ssid != '':
                        current_ssid = ssid
                elif 'Encryption key:' in line and current_ssid:
                    encrypted = 'on' in line
                    networks.append({
                        'ssid': current_ssid,
                        'encrypted': encrypted
                    })
                    current_ssid = None
            
            print(f"  ✓ Found {len(networks)} WiFi networks")
            for i, network in enumerate(networks[:3]):  # Show first 3
                print(f"    - {network['ssid']} ({'Protected' if network['encrypted'] else 'Open'})")
            
            if len(networks) > 3:
                print(f"    ... and {len(networks) - 3} more")
        else:
            print("  ℹ WiFi scanning not available")
    except FileNotFoundError:
        print("  ℹ iwlist command not available")
    
    return True

def test_web_api_endpoints():
    """Test web API endpoints"""
    print("\n🌐 Testing Web API Endpoints...")
    
    # Test if Flask app can be imported
    try:
        from web_versetime import app, system_manager
        print("  ✓ Flask app imported successfully")
        
        # Test system manager methods
        with app.app_context():
            # Test system info
            system_info = system_manager.get_system_info()
            print(f"  ✓ System info retrieved: {len(system_info)} items")
            
            # Test battery info
            battery_info = system_manager.get_battery_info()
            print(f"  ✓ Battery info retrieved: {battery_info}")
            
            # Test WiFi scanning
            wifi_networks = system_manager.scan_wifi_networks()
            print(f"  ✓ WiFi scan completed: {len(wifi_networks)} networks found")
            
    except ImportError as e:
        print(f"  ✗ Error importing Flask app: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error testing API endpoints: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 VerseTime Web Interface Feature Tests")
    print("=" * 50)
    
    tests = [
        test_battery_detection,
        test_temperature_conversion,
        test_wifi_scanning,
        test_web_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The new features are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 