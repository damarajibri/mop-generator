#!/usr/bin/env python3
"""
Test Script: Network Configuration & IP Addressing Complete Workflow
Test save dan reload network configuration functionality
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

def create_test_mop_with_network_configs():
    """Create test MOP dengan network configuration data"""
    print("📝 Creating test MOP with network configurations...")
    
    load_env()
    
    try:
        from app import app
        
        # Test data dengan comprehensive network configs
        test_data = {
            'title': 'NETWORK CONFIG TEST - Complete Network & IP Addressing',
            'document_title': 'NETWORK CONFIG TEST - Complete Network & IP Addressing', 
            'version': '6.0',
            'category': 'Network Test',
            'activity_name': 'Network Configuration & IP Addressing Test',
            'work_type': 'Network Infrastructure Configuration',
            'summary': 'Test complete network configuration save and reload functionality',
            'executive_summary': 'Comprehensive test untuk memastikan network configurations tersimpan dan ter-reload dengan benar',
            
            # Technical Config
            'hardware_requirements': 'NETWORK TEST: Network switches, routers, and firewalls for IP addressing',
            'software_dependencies': 'NETWORK TEST: Network management tools and configuration utilities',
            'network_prerequisites': 'NETWORK TEST: Access to network infrastructure and management interfaces',
            
            # Devices untuk konteks
            'devices': [
                {
                    'hostname': 'CORE-SW-01.company.com',
                    'name': 'CORE-SW-01.company.com',
                    'type': 'switch',
                    'mgmt_ip': '192.168.100.10',
                    'ip': '192.168.100.10',
                    'location': 'DC1-Rack5-U20'
                },
                {
                    'hostname': 'EDGE-FW-01.company.com',
                    'name': 'EDGE-FW-01.company.com', 
                    'type': 'firewall',
                    'mgmt_ip': '192.168.100.20',
                    'ip': '192.168.100.20',
                    'location': 'DC1-Rack3-U10'
                }
            ],
            
            # Network Configurations - Multiple configs for comprehensive test
            'networkConfigs': [
                {
                    'realIp': '10.200.1.0/24',
                    'natIp': '203.0.113.50/24',
                    'paloAltoZone': 'DMZ-SERVERS',
                    'vlanId': 100,
                    'description': 'Network Config Test 1: DMZ Server Network with NAT translation'
                },
                {
                    'realIp': '10.200.2.0/24', 
                    'natIp': '203.0.113.60/24',
                    'paloAltoZone': 'TRUST-LAN',
                    'vlanId': 200,
                    'description': 'Network Config Test 2: Internal LAN network with public NAT'
                },
                {
                    'realIp': '10.200.3.100',
                    'natIp': '203.0.113.70',
                    'paloAltoZone': 'UNTRUST-WAN', 
                    'vlanId': 300,
                    'description': 'Network Config Test 3: Single host NAT configuration for WAN access'
                }
            ]
        }
        
        with app.test_client() as client:
            print(f"📤 Sending test data with {len(test_data.get('networkConfigs', []))} network configs...")
            
            response = client.post('/api/save_mop',
                                  json=test_data,
                                  headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.get_json()
                
                if result.get('success'):
                    mop_id = result.get('database_id')
                    print(f"✅ Test MOP with network configs created - ID: {mop_id}")
                    return mop_id
                else:
                    print(f"❌ Save failed: {result}")
            else:
                print(f"❌ Save API error: {response.status_code}")
        
        return None
        
    except Exception as e:
        print(f"❌ Test MOP creation failed: {e}")
        return None

def test_network_config_reload(mop_id):
    """Test network config reload functionality"""
    print(f"\\n🧪 Testing network config reload for MOP ID {mop_id}...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get(f'/api/mop_detail/{mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    mop_data = data['data']
                    networkConfigs = mop_data.get('networkConfigs', [])
                    
                    print(f"✅ API returned {len(networkConfigs)} network configs")
                    
                    if networkConfigs:
                        print(f"\\n🔍 Network Config Reload Test Results:")
                        
                        expected_configs = [
                            {'realIp': '10.200.1.0/24', 'natIp': '203.0.113.50/24', 'zone': 'DMZ-SERVERS', 'vlan': 100},
                            {'realIp': '10.200.2.0/24', 'natIp': '203.0.113.60/24', 'zone': 'TRUST-LAN', 'vlan': 200},
                            {'realIp': '10.200.3.100', 'natIp': '203.0.113.70', 'zone': 'UNTRUST-WAN', 'vlan': 300}
                        ]
                        
                        success_count = 0
                        
                        for i, expected in enumerate(expected_configs):
                            if i < len(networkConfigs):
                                actual = networkConfigs[i]
                                realip_match = expected['realIp'] == actual.get('realIp', '')
                                natip_match = expected['natIp'] == actual.get('natIp', '')
                                zone_match = expected['zone'] == actual.get('paloAltoZone', '')
                                vlan_match = expected['vlan'] == actual.get('vlanId', 0)
                                
                                if realip_match and natip_match and zone_match and vlan_match:
                                    success_count += 1
                                    status = "✅ MATCH"
                                else:
                                    status = "❌ MISMATCH"
                                
                                print(f"   Config {i+1}: {status}")
                                print(f"     Expected: {expected['realIp']} -> {expected['natIp']} (Zone: {expected['zone']}, VLAN: {expected['vlan']})")
                                print(f"     Actual:   {actual.get('realIp', 'N/A')} -> {actual.get('natIp', 'N/A')} (Zone: {actual.get('paloAltoZone', 'N/A')}, VLAN: {actual.get('vlanId', 'N/A')})")
                            else:
                                print(f"   Config {i+1}: ❌ MISSING")
                        
                        coverage = (success_count / len(expected_configs)) * 100
                        print(f"\\n📊 Network Config Reload Coverage: {success_count}/{len(expected_configs)} ({coverage:.1f}%)")
                        
                        return coverage >= 80
                    else:
                        print("❌ No network configs returned from API")
                        return False
                else:
                    print(f"❌ API failed: {data}")
                    return False
            else:
                print(f"❌ API error: {response.status_code}")
                return False
        
    except Exception as e:
        print(f"❌ Network config reload test failed: {e}")
        return False

def test_existing_network_config():
    """Test dengan MOP yang sudah ada network config (MOP ID 33)"""
    print(f"\\n🧪 Testing existing MOP with network configs (ID 33)...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.get('/api/mop_detail/33')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    networkConfigs = data['data'].get('networkConfigs', [])
                    print(f"✅ Existing MOP 33 has {len(networkConfigs)} network configs")
                    
                    if networkConfigs:
                        print(f"🔍 Existing network configs:")
                        for i, config in enumerate(networkConfigs):
                            print(f"   Config {i+1}: {config.get('realIp')} -> {config.get('natIp')} (Zone: {config.get('paloAltoZone')}, VLAN: {config.get('vlanId')})")
                        return True
                    else:
                        print("⚪ No configs in existing MOP")
                        return False
                else:
                    print(f"❌ Existing MOP API failed")
                    return False
            else:
                print(f"❌ Existing MOP API error")
                return False
                
    except Exception as e:
        print(f"❌ Existing network config test failed: {e}")
        return False

def generate_manual_instructions(mop_id):
    """Generate manual testing instructions"""
    print(f"\\n📋 MANUAL TESTING INSTRUCTIONS FOR NETWORK CONFIGURATION")
    print("=" * 80)
    
    print(f"🔧 Network Configuration & IP Addressing Test:")
    
    print(f"\\n1. Start Application:")
    print(f"   cd mop_minimal && python3 app.py")
    print(f"   Open browser: http://localhost:3000")
    
    print(f"\\n2. Navigate to History MOP:")
    print(f"   - Click 'History MOP' tab (leftmost)")
    print(f"   - Find MOP ID {mop_id} with title 'NETWORK CONFIG TEST'")
    print(f"   - Activity Name should show: 'Network Configuration & IP Addressing Test'")
    
    print(f"\\n3. Test Network Config Reload:")
    print(f"   - Click reload button for MOP ID {mop_id}")
    print(f"   - Watch for success notification")
    print(f"   - Auto-switch to Technical Config tab should occur")
    
    print(f"\\n4. Check Network Configuration Section:")
    print(f"   - Scroll to 'Network Configuration & IP Addressing' section")
    print(f"   - Should see 3 network config items populated:")
    
    print(f"\\n     Config 1 - DMZ Servers:")
    print(f"       ✅ Real IP: 10.200.1.0/24")
    print(f"       ✅ NAT IP: 203.0.113.50/24") 
    print(f"       ✅ Security Zone: DMZ-SERVERS")
    print(f"       ✅ VLAN ID: 100")
    print(f"       ✅ Description: Network Config Test 1: DMZ Server Network...")
    
    print(f"\\n     Config 2 - Internal LAN:")
    print(f"       ✅ Real IP: 10.200.2.0/24")
    print(f"       ✅ NAT IP: 203.0.113.60/24")
    print(f"       ✅ Security Zone: TRUST-LAN")
    print(f"       ✅ VLAN ID: 200")
    print(f"       ✅ Description: Network Config Test 2: Internal LAN...")
    
    print(f"\\n     Config 3 - WAN Access:")
    print(f"       ✅ Real IP: 10.200.3.100")
    print(f"       ✅ NAT IP: 203.0.113.70")
    print(f"       ✅ Security Zone: UNTRUST-WAN")
    print(f"       ✅ VLAN ID: 300")
    print(f"       ✅ Description: Network Config Test 3: Single host NAT...")
    
    print(f"\\n5. Console Debugging:")
    print(f"   - Open Developer Tools (F12)")
    print(f"   - Check Console for network loading messages:")
    print(f"     * 🌐 Loading network configs into form: 3")
    print(f"     * ✅ Network config 1 loaded: 10.200.1.0/24 -> 203.0.113.50/24")
    print(f"     * ✅ Network config 2 loaded: 10.200.2.0/24 -> 203.0.113.60/24")
    print(f"     * ✅ Network config 3 loaded: 10.200.3.100 -> 203.0.113.70")
    print(f"     * ✅ Network configs populated into form")
    
    print(f"\\n✅ Success Indicators:")
    print(f"   - All 3 network configs visible in form")
    print(f"   - All fields populated correctly (Real IP, NAT IP, Zone, VLAN)")
    print(f"   - No JavaScript errors in console")
    print(f"   - Network data matches expected values")

def main():
    """Main test function"""
    print("🎯 NETWORK CONFIGURATION & IP ADDRESSING COMPLETE TEST")
    print("=" * 80)
    
    # Test existing network config first
    existing_ok = test_existing_network_config()
    
    # Create test MOP with network configs
    mop_id = create_test_mop_with_network_configs()
    
    if mop_id:
        # Test network config reload
        reload_success = test_network_config_reload(mop_id)
        
        print(f"\\n🎯 NETWORK CONFIGURATION TEST RESULTS:")
        print("=" * 70)
        print(f"✅ Existing MOP Network Configs: {'SUCCESS' if existing_ok else 'NO DATA'}")
        print(f"✅ MOP with Network Configs Creation: SUCCESS (ID: {mop_id})")
        print(f"✅ Network Config Reload API Test: {'SUCCESS' if reload_success else 'FAILED'}")
        
        if reload_success:
            print(f"\\n🎉 NETWORK CONFIGURATION FUNCTIONALITY WORKING!")
            print(f"\\n💡 Fixes Applied:")
            print(f"   ✅ Network config loading changed from undefined variables to form population")
            print(f"   ✅ Direct DOM manipulation for network config form fields") 
            print(f"   ✅ Staggered population with proper timing")
            print(f"   ✅ Support for multiple network configs with addIPZoneConfiguration integration")
            print(f"   ✅ Comprehensive field mapping (Real IP, NAT IP, Zone, VLAN, Description)")
            print(f"   ✅ IP address parsing for subnet notation (e.g., 10.1.1.0/24)")
            
            generate_manual_instructions(mop_id)
        else:
            print(f"\\n⚠️  NETWORK CONFIG RELOAD ISSUES DETECTED")
            print(f"   - Check API network config data structure")
            print(f"   - Verify network config save mechanism")
            print(f"   - Test manual reload in browser")
        
        return reload_success
    else:
        print(f"\\n❌ NETWORK CONFIG TEST FAILED - Could not create test MOP")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)