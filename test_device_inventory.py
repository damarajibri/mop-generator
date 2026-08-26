#!/usr/bin/env python3
"""
Test Script: Device Inventory Complete Workflow
Test save dan reload device inventory functionality
"""

import os
import sys

def load_env():
    """Load environment variables"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment loaded")
    except Exception as e:
        print(f"❌ Error loading environment: {e}")

def create_test_mop_with_devices():
    """Create test MOP dengan device inventory"""
    print("📝 Creating test MOP with device inventory...")
    
    load_env()
    
    try:
        from app import app
        
        # Test data dengan devices
        test_data = {
            'title': 'DEVICE INVENTORY TEST - Complete Workflow',
            'document_title': 'DEVICE INVENTORY TEST - Complete Workflow', 
            'version': '5.0',
            'category': 'Device Test',
            'activity_name': 'Device Inventory & Hardware Details Test',
            'work_type': 'Network Infrastructure Change',
            'summary': 'Test complete device inventory save and reload functionality',
            'executive_summary': 'Comprehensive test untuk memastikan device inventory tersimpan dan ter-reload dengan benar',
            
            # Technical Config
            'hardware_requirements': 'DEVICE TEST: Core network equipment including routers, switches, and firewalls',
            'software_dependencies': 'DEVICE TEST: Network OS updates and configuration management tools',
            'network_prerequisites': 'DEVICE TEST: Management network access and backup connectivity established',
            
            # Devices - Multiple devices for comprehensive test
            'devices': [
                {
                    'hostname': 'CORE-RTR-01.company.com',
                    'name': 'CORE-RTR-01.company.com',
                    'type': 'router',
                    'mgmt_ip': '192.168.100.1',
                    'ip': '192.168.100.1',
                    'model_serial': 'Cisco ASR-9006 / SN123456789',
                    'location': 'DC1-Rack10-U42',
                    'os_version': 'IOS XR 7.3.2',
                    'console': 'SSH console.dc1.company.com:2001',
                    'role': 'primary'
                },
                {
                    'hostname': 'DIST-SW-02.company.com', 
                    'name': 'DIST-SW-02.company.com',
                    'type': 'switch',
                    'mgmt_ip': '192.168.100.2',
                    'ip': '192.168.100.2',
                    'model_serial': 'Cisco 9500-48Y4C / SN987654321',
                    'location': 'DC1-Rack12-U20',
                    'os_version': 'IOS XE 16.12.09',
                    'console': 'SSH console.dc1.company.com:2002',
                    'role': 'secondary'
                },
                {
                    'hostname': 'EDGE-FW-01.company.com',
                    'name': 'EDGE-FW-01.company.com', 
                    'type': 'firewall',
                    'mgmt_ip': '192.168.100.3',
                    'ip': '192.168.100.3',
                    'model_serial': 'Palo Alto PA-5250 / SN456789123',
                    'location': 'DC1-Rack8-U15',
                    'os_version': 'PAN-OS 10.2.4',
                    'console': 'HTTPS management interface',
                    'role': 'primary'
                }
            ]
        }
        
        with app.test_client() as client:
            print(f"📤 Sending test data with {len(test_data.get('devices', []))} devices...")
            
            response = client.post('/api/save_mop',
                                  json=test_data,
                                  headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.get_json()
                
                if result.get('success'):
                    mop_id = result.get('database_id')
                    print(f"✅ Test MOP with devices created - ID: {mop_id}")
                    return mop_id
                else:
                    print(f"❌ Save failed: {result}")
            else:
                print(f"❌ Save API error: {response.status_code}")
        
        return None
        
    except Exception as e:
        print(f"❌ Test MOP creation failed: {e}")
        return None

def test_device_reload(mop_id):
    """Test device reload functionality"""
    print(f"\\n🧪 Testing device reload for MOP ID {mop_id}...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get(f'/api/mop_detail/{mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    mop_data = data['data']
                    devices = mop_data.get('devices', [])
                    
                    print(f"✅ API returned {len(devices)} devices")
                    
                    if devices:
                        print(f"\\n🔍 Device Reload Test Results:")
                        
                        expected_devices = [
                            {'hostname': 'CORE-RTR-01.company.com', 'type': 'router', 'mgmt_ip': '192.168.100.1'},
                            {'hostname': 'DIST-SW-02.company.com', 'type': 'switch', 'mgmt_ip': '192.168.100.2'},
                            {'hostname': 'EDGE-FW-01.company.com', 'type': 'firewall', 'mgmt_ip': '192.168.100.3'}
                        ]
                        
                        success_count = 0
                        
                        for i, expected in enumerate(expected_devices):
                            if i < len(devices):
                                actual = devices[i]
                                hostname_match = expected['hostname'] in (actual.get('hostname', '') + actual.get('name', ''))
                                type_match = expected['type'] == actual.get('type', '')
                                ip_match = expected['mgmt_ip'] in (actual.get('mgmt_ip', '') + actual.get('ip', ''))
                                
                                if hostname_match and type_match and ip_match:
                                    success_count += 1
                                    status = "✅ MATCH"
                                else:
                                    status = "❌ MISMATCH"
                                
                                print(f"   Device {i+1}: {status}")
                                print(f"     Expected: {expected['hostname']} ({expected['type']}) - {expected['mgmt_ip']}")
                                print(f"     Actual:   {actual.get('hostname', actual.get('name', 'N/A'))} ({actual.get('type', 'N/A')}) - {actual.get('mgmt_ip', actual.get('ip', 'N/A'))}")
                            else:
                                print(f"   Device {i+1}: ❌ MISSING")
                        
                        coverage = (success_count / len(expected_devices)) * 100
                        print(f"\\n📊 Device Reload Coverage: {success_count}/{len(expected_devices)} ({coverage:.1f}%)")
                        
                        return coverage >= 80
                    else:
                        print("❌ No devices returned from API")
                        return False
                else:
                    print(f"❌ API failed: {data}")
                    return False
            else:
                print(f"❌ API error: {response.status_code}")
                return False
        
    except Exception as e:
        print(f"❌ Device reload test failed: {e}")
        return False

def generate_manual_instructions(mop_id):
    """Generate manual testing instructions"""
    print(f"\\n📋 MANUAL TESTING INSTRUCTIONS FOR DEVICE INVENTORY")
    print("=" * 80)
    
    print(f"🔧 Device Inventory & Hardware Details Test:")
    
    print(f"\\n1. Start Application:")
    print(f"   cd mop_minimal && python3 app.py")
    print(f"   Open browser: http://localhost:8888")
    
    print(f"\\n2. Navigate to History MOP:")
    print(f"   - Click 'History MOP' tab (leftmost)")
    print(f"   - Find MOP ID {mop_id} with title 'DEVICE INVENTORY TEST'")
    print(f"   - Activity Name should show: 'Device Inventory & Hardware Details Test'")
    
    print(f"\\n3. Test Device Reload:")
    print(f"   - Click reload button for MOP ID {mop_id}")
    print(f"   - Watch for success notification")
    print(f"   - Auto-switch to Technical Config tab should occur")
    
    print(f"\\n4. Check Device Inventory Section:")
    print(f"   - Scroll to 'Device Inventory & Hardware Details' section")
    print(f"   - Should see 3 device items populated:")
    
    print(f"\\n     Device 1 - Core Router:")
    print(f"       ✅ Hostname: CORE-RTR-01.company.com")
    print(f"       ✅ Type: Router")
    print(f"       ✅ Management IP: 192.168.100.1")
    print(f"       ✅ Model & Serial: Cisco ASR-9006 / SN123456789")
    print(f"       ✅ Location: DC1-Rack10-U42")
    
    print(f"\\n     Device 2 - Distribution Switch:")
    print(f"       ✅ Hostname: DIST-SW-02.company.com")
    print(f"       ✅ Type: Switch")  
    print(f"       ✅ Management IP: 192.168.100.2")
    print(f"       ✅ Model & Serial: Cisco 9500-48Y4C / SN987654321")
    print(f"       ✅ Location: DC1-Rack12-U20")
    
    print(f"\\n     Device 3 - Edge Firewall:")
    print(f"       ✅ Hostname: EDGE-FW-01.company.com")
    print(f"       ✅ Type: Firewall")
    print(f"       ✅ Management IP: 192.168.100.3")
    print(f"       ✅ Model & Serial: Palo Alto PA-5250 / SN456789123")
    print(f"       ✅ Location: DC1-Rack8-U15")
    
    print(f"\\n5. Console Debugging:")
    print(f"   - Open Developer Tools (F12)")
    print(f"   - Check Console for device loading messages:")
    print(f"     * 📱 Loading devices into form: 3")
    print(f"     * ✅ Device 1 loaded: CORE-RTR-01.company.com")
    print(f"     * ✅ Device 2 loaded: DIST-SW-02.company.com")
    print(f"     * ✅ Device 3 loaded: EDGE-FW-01.company.com")
    print(f"     * ✅ Devices populated into form")
    
    print(f"\\n✅ Success Indicators:")
    print(f"   - All 3 devices visible in form")
    print(f"   - All fields populated correctly")
    print(f"   - No JavaScript errors in console")
    print(f"   - Device data matches expected values")

def main():
    """Main test function"""
    print("🎯 DEVICE INVENTORY & HARDWARE DETAILS COMPLETE TEST")
    print("=" * 80)
    
    # Create test MOP with devices
    mop_id = create_test_mop_with_devices()
    
    if mop_id:
        # Test device reload
        reload_success = test_device_reload(mop_id)
        
        print(f"\\n🎯 DEVICE INVENTORY TEST RESULTS:")
        print("=" * 60)
        print(f"✅ MOP with Devices Creation: SUCCESS (ID: {mop_id})")
        print(f"✅ Device Reload API Test: {'SUCCESS' if reload_success else 'FAILED'}")
        
        if reload_success:
            print(f"\\n🎉 DEVICE INVENTORY FUNCTIONALITY WORKING!")
            print(f"\\n💡 Fixes Applied:")
            print(f"   ✅ Device loading changed from undefined variables to form population")
            print(f"   ✅ Direct DOM manipulation for device form fields") 
            print(f"   ✅ Staggered population with proper timing")
            print(f"   ✅ Support for multiple devices with addDeviceItem integration")
            print(f"   ✅ Comprehensive field mapping (hostname, type, IP, etc.)")
            
            generate_manual_instructions(mop_id)
        else:
            print(f"\\n⚠️  DEVICE RELOAD ISSUES DETECTED")
            print(f"   - Check API device data structure")
            print(f"   - Verify device save mechanism")
            print(f"   - Test manual reload in browser")
        
        return reload_success
    else:
        print(f"\\n❌ DEVICE TEST FAILED - Could not create test MOP")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)