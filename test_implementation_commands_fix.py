#!/usr/bin/env python3
"""
Test Implementation Commands Loading & Saving
Memverifikasi bahwa Implementation Commands bisa disimpan dan dimuat dengan benar
"""

import os
import requests
import json
import time

def load_env():
    """Load environment variables"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

def test_implementation_commands():
    """Test Implementation Commands functionality end-to-end"""
    
    print("🎯 IMPLEMENTATION COMMANDS COMPREHENSIVE TEST")
    print("="*60)
    
    # Load environment
    load_env()
    
    port = os.environ.get('PORT', '4000')
    base_url = f"http://localhost:{port}"
    
    print(f"🌐 Testing against: {base_url}")
    
    # Test data with Implementation Commands
    test_data = {
        'document_title': 'TEST Implementation Commands Fix',
        'version': 'v2.0',
        'activity_name': 'Test Implementation Commands Loading/Saving',
        'work_type': 'Implementation',
        'summary': 'Comprehensive test for Implementation Commands functionality',
        
        # Implementation Commands (the fields we're testing)
        'general_implementation_commands': '''# General Implementation Commands Test
echo "Starting implementation process"
configure terminal
hostname TEST-DEVICE
interface GigabitEthernet0/1
 description TEST INTERFACE
 no shutdown
exit
write memory''',
        
        'general_implementation_commands_html': '''<div class="code-block">
# General Implementation Commands Test<br>
echo "Starting implementation process"<br>
configure terminal<br>
hostname TEST-DEVICE<br>
interface GigabitEthernet0/1<br>
 description TEST INTERFACE<br>
 no shutdown<br>
exit<br>
write memory
</div>''',
        
        'pre_implementation_commands': '''# Pre-Implementation Commands Test
show version
show running-config
show interfaces status
show ip route
ping 8.8.8.8''',
        
        'pre_implementation_commands_html': '''<div class="code-block">
# Pre-Implementation Commands Test<br>
show version<br>
show running-config<br>
show interfaces status<br>
show ip route<br>
ping 8.8.8.8
</div>''',
        
        'implementation_commands': '''# Implementation Commands Test
configure terminal
no ip domain lookup
service timestamps debug datetime msec
service timestamps log datetime msec
logging buffered 8192
ntp server 192.168.1.100
exit
write memory''',
        
        'implementation_commands_html': '''<div class="code-block">
# Implementation Commands Test<br>
configure terminal<br>
no ip domain lookup<br>
service timestamps debug datetime msec<br>
service timestamps log datetime msec<br>
logging buffered 8192<br>
ntp server 192.168.1.100<br>
exit<br>
write memory
</div>''',
        
        'verification_commands': '''# Verification Commands Test
show ntp status
show logging
show running-config | include timestamp
show running-config | include ntp
show running-config | include domain
ping 192.168.1.100''',
        
        'verification_commands_html': '''<div class="code-block">
# Verification Commands Test<br>
show ntp status<br>
show logging<br>
show running-config | include timestamp<br>
show running-config | include ntp<br>
show running-config | include domain<br>
ping 192.168.1.100
</div>''',
        
        # Rollback command (existing field)
        'rollback_commands': '''# Rollback Commands Test
configure terminal
no ntp server 192.168.1.100
no service timestamps debug datetime msec
no service timestamps log datetime msec
ip domain lookup
exit
write memory''',
        
        # Other required fields
        'category': 'Network Infrastructure',
        'execution_time': '2024-12-26 02:00',
        'total_duration': '30 minutes',
        'implementation_status': 'planned'
    }
    
    try:
        # Step 1: Save MOP with Implementation Commands
        print("\n1️⃣ Saving MOP with Implementation Commands...")
        
        save_response = requests.post(f"{base_url}/api/save_mop", json=test_data)
        
        if save_response.status_code == 200:
            save_result = save_response.json()
            if save_result.get('success'):
                mop_id = save_result.get('database_id')
                print(f"✅ MOP saved successfully! ID: {mop_id}")
                print(f"   Filename: {save_result.get('filename')}")
            else:
                print(f"❌ Save failed: {save_result.get('message')}")
                return False
        else:
            print(f"❌ Save request failed: {save_response.status_code}")
            return False
        
        # Step 2: Wait a bit for database commit
        time.sleep(1)
        
        # Step 3: Retrieve saved MOP
        print(f"\n2️⃣ Retrieving MOP {mop_id} to verify Implementation Commands...")
        
        detail_response = requests.get(f"{base_url}/api/mop_detail/{mop_id}")
        
        if detail_response.status_code == 200:
            detail_result = detail_response.json()
            if detail_result.get('success'):
                loaded_data = detail_result.get('data', {})
                print("✅ MOP retrieved successfully!")
                
                # Step 4: Verify Implementation Commands fields
                print("\n3️⃣ Verifying Implementation Commands fields...")
                
                command_fields = {
                    'general_implementation_commands': 'General Implementation Commands',
                    'general_implementation_commands_html': 'General Implementation Commands (HTML)',
                    'pre_implementation_commands': 'Pre-Implementation Commands',
                    'pre_implementation_commands_html': 'Pre-Implementation Commands (HTML)',
                    'implementation_commands': 'Implementation Commands',
                    'implementation_commands_html': 'Implementation Commands (HTML)',
                    'verification_commands': 'Verification Commands',
                    'verification_commands_html': 'Verification Commands (HTML)',
                    'rollback_commands': 'Rollback Commands (existing field)'
                }
                
                success_count = 0
                total_fields = len(command_fields)
                
                for field_name, field_desc in command_fields.items():
                    saved_value = test_data.get(field_name, '')
                    loaded_value = loaded_data.get(field_name, '')
                    
                    if loaded_value and loaded_value.strip():
                        if saved_value.strip() == loaded_value.strip():
                            print(f"   ✅ {field_desc}: MATCH")
                            success_count += 1
                        else:
                            print(f"   ⚠️  {field_desc}: DATA MISMATCH")
                            print(f"      Saved:  '{saved_value[:50]}...'")
                            print(f"      Loaded: '{loaded_value[:50]}...'")
                    else:
                        print(f"   ❌ {field_desc}: NOT LOADED (empty)")
                
                # Step 5: Results summary
                success_rate = (success_count / total_fields) * 100
                print(f"\n📊 VERIFICATION RESULTS:")
                print(f"   Successfully loaded: {success_count}/{total_fields} fields ({success_rate:.1f}%)")
                
                if success_rate >= 80:
                    print(f"   🎉 TEST PASSED - Implementation Commands working!")
                    
                    # Show sample content
                    print(f"\n📋 Sample loaded content:")
                    if loaded_data.get('general_implementation_commands'):
                        print(f"   General Commands: {loaded_data['general_implementation_commands'][:100]}...")
                    if loaded_data.get('verification_commands'):
                        print(f"   Verification Commands: {loaded_data['verification_commands'][:100]}...")
                    
                    return True
                else:
                    print(f"   ❌ TEST FAILED - Too many fields missing")
                    return False
                
            else:
                print(f"❌ Retrieve failed: {detail_result.get('message')}")
                return False
        else:
            print(f"❌ Retrieve request failed: {detail_response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running:")
        print("   cd mop_minimal && python3 app.py")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_browser_loading():
    """Test if Implementation Commands will load in browser"""
    
    print("\n4️⃣ Browser Loading Test...")
    print("   The following should work in browser after server restart:")
    print("   1. Go to History MOP tab")
    print("   2. Find the test MOP (Implementation Commands Fix)")
    print("   3. Click reload button")
    print("   4. Go to Implementation tab")
    print("   5. Check 'General Implementation Commands' rich editor")
    print("   6. Should see the test commands loaded")
    print("\n💡 Manual verification needed in browser!")

if __name__ == "__main__":
    if test_implementation_commands():
        test_browser_loading()
        print("\n🎯 ALL TESTS COMPLETED!")
        print("✅ Implementation Commands loading and saving should now work")
    else:
        print("\n❌ TESTS FAILED!")
        print("⚠️  Implementation Commands still need debugging")