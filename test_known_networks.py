#!/usr/bin/env python3
"""
Test script for VerseTime Known Networks functionality
Tests reading, updating, and deleting WiFi networks
"""

import json
import sys
import os

def test_known_networks_import():
    """Test importing the web interface and system manager"""
    print("🔧 Testing Known Networks Import...")
    
    try:
        from web_versetime import system_manager
        print("  ✓ System manager imported successfully")
        return system_manager
    except ImportError as e:
        print(f"  ✗ Error importing system manager: {e}")
        return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def test_get_known_networks(system_manager):
    """Test getting known networks"""
    print("\n📋 Testing Get Known Networks...")
    
    try:
        networks = system_manager.get_known_networks()
        print(f"  ✓ Retrieved {len(networks)} known networks")
        
        for i, network in enumerate(networks):
            print(f"    {i+1}. {network['ssid']} ({'Protected' if network.get('encrypted') else 'Open'})")
        
        return networks
    except Exception as e:
        print(f"  ✗ Error getting known networks: {e}")
        return []

def test_add_network(system_manager):
    """Test adding a new network"""
    print("\n➕ Testing Add Network...")
    
    try:
        # Test adding a protected network
        result = system_manager.add_wifi_network("TestNetwork", "testpassword123")
        if result:
            print("  ✓ Test network added successfully")
        else:
            print("  ℹ Test network already exists or failed to add")
        
        # Test adding an open network
        result = system_manager.add_wifi_network("TestOpenNetwork", "")
        if result:
            print("  ✓ Test open network added successfully")
        else:
            print("  ℹ Test open network already exists or failed to add")
        
        return True
    except Exception as e:
        print(f"  ✗ Error adding network: {e}")
        return False

def test_update_network(system_manager, networks):
    """Test updating a network"""
    print("\n✏️ Testing Update Network...")
    
    if not networks:
        print("  ℹ No networks to update")
        return False
    
    try:
        # Update the first network
        first_network = networks[0]
        new_ssid = first_network['ssid'] + "_updated"
        new_password = "newpassword123"
        
        result = system_manager.update_network(0, new_ssid, new_password)
        if result:
            print(f"  ✓ Network updated successfully: {new_ssid}")
            
            # Verify the update
            updated_networks = system_manager.get_known_networks()
            if updated_networks and updated_networks[0]['ssid'] == new_ssid:
                print("  ✓ Update verified")
            else:
                print("  ⚠ Update verification failed")
            
            return True
        else:
            print("  ✗ Failed to update network")
            return False
    except Exception as e:
        print(f"  ✗ Error updating network: {e}")
        return False

def test_delete_network(system_manager, networks):
    """Test deleting a network"""
    print("\n🗑️ Testing Delete Network...")
    
    if not networks:
        print("  ℹ No networks to delete")
        return False
    
    try:
        # Delete the first network
        first_network = networks[0]
        ssid = first_network['ssid']
        
        result = system_manager.delete_network(ssid, 0)
        if result:
            print(f"  ✓ Network deleted successfully: {ssid}")
            
            # Verify the deletion
            updated_networks = system_manager.get_known_networks()
            if not updated_networks or updated_networks[0]['ssid'] != ssid:
                print("  ✓ Deletion verified")
            else:
                print("  ⚠ Deletion verification failed")
            
            return True
        else:
            print("  ✗ Failed to delete network")
            return False
    except Exception as e:
        print(f"  ✗ Error deleting network: {e}")
        return False

def test_wpa_supplicant_parsing():
    """Test wpa_supplicant.conf parsing"""
    print("\n📄 Testing WPA Supplicant Parsing...")
    
    # Create a test wpa_supplicant.conf content
    test_content = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="TestNetwork1"
    psk="password123"
    key_mgmt=WPA-PSK
}

network={
    ssid="TestNetwork2"
    key_mgmt=NONE
}

network={
    ssid="TestNetwork3"
    psk="anotherpassword"
    key_mgmt=WPA-PSK
}
"""
    
    try:
        # Create a temporary test file
        test_file = '/tmp/test_wpa_supplicant.conf'
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Test parsing
        from web_versetime import SystemManager
        test_manager = SystemManager()
        test_manager.wifi_config_file = test_file
        
        networks = test_manager.get_known_networks()
        print(f"  ✓ Parsed {len(networks)} networks from test file")
        
        for i, network in enumerate(networks):
            print(f"    {i+1}. {network['ssid']} ({'Protected' if network.get('encrypted') else 'Open'})")
        
        # Clean up
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"  ✗ Error testing parsing: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 VerseTime Known Networks Tests")
    print("=" * 50)
    
    # Test import
    system_manager = test_known_networks_import()
    if not system_manager:
        print("\n❌ Cannot proceed without system manager")
        return False
    
    # Test parsing
    test_wpa_supplicant_parsing()
    
    # Test getting known networks
    networks = test_get_known_networks(system_manager)
    
    # Test adding network
    test_add_network(system_manager)
    
    # Refresh networks list
    networks = test_get_known_networks(system_manager)
    
    # Test updating network
    if networks:
        test_update_network(system_manager, networks)
    
    # Refresh networks list again
    networks = test_get_known_networks(system_manager)
    
    # Test deleting network
    if networks:
        test_delete_network(system_manager, networks)
    
    print("\n" + "=" * 50)
    print("✅ Known networks functionality tests completed")
    print("Note: Some tests may fail if running on a system without proper WiFi configuration")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 