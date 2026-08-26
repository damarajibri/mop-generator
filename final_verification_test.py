#!/usr/bin/env python3
"""
Final Test: History MOP Activity Name dan Technical Config Reload
Verifikasi semua perbaikan sudah berfungsi dengan benar
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

def test_activity_name_fix():
    """Test Activity Name fix di History MOP"""
    print("🧪 Testing Activity Name fix...")
    
    load_env()
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test History API
            response = client.get('/api/mop_history?page=1&page_size=3')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    print(f"✅ History API working - {len(data['data'])} records")
                    
                    # Check Activity Name data
                    activity_names_found = 0
                    
                    for item in data['data']:
                        activity_name = item.get('activity_name', '')
                        title = item.get('title', '')
                        
                        if activity_name and activity_name != 'General Activity':
                            activity_names_found += 1
                            
                        print(f"   ID {item['id']}: \"{title}\" -> Activity: \"{activity_name}\"")
                    
                    coverage = (activity_names_found / len(data['data'])) * 100 if data['data'] else 0
                    print(f"📊 Activity Name Coverage: {activity_names_found}/{len(data['data'])} ({coverage:.1f}%)")
                    
                    return coverage >= 50  # At least 50% should have specific activity names
                    
                else:
                    print(f"❌ History API failed: {data}")
            else:
                print(f"❌ History API error: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Activity Name test failed: {e}")
        return False

def test_technical_config_reload():
    """Test Technical Config reload functionality"""
    print("\\n🔧 Testing Technical Config reload...")
    
    try:
        from app import app
        
        # Use MOP ID 40 which has comprehensive Technical Config data
        mop_id = 40
        
        with app.test_client() as client:
            response = client.get(f'/api/mop_detail/{mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    mop_data = data['data']
                    print(f"✅ Detail API working - {len(mop_data)} total fields")
                    
                    # Test key Technical Config fields
                    tech_fields = {
                        'hardware_requirements': mop_data.get('hardware_requirements'),
                        'software_dependencies': mop_data.get('software_dependencies'),
                        'network_prerequisites': mop_data.get('network_prerequisites'),
                        'prep_start_time': mop_data.get('prep_start_time'),
                        'impl_start_time': mop_data.get('impl_start_time'),
                        'verification_start_time': mop_data.get('verification_start_time'),
                        'technical_success_criteria': mop_data.get('technical_success_criteria'),
                        'rollback_commands': mop_data.get('rollback_commands'),
                        'communication_frequency': mop_data.get('communication_frequency')
                    }
                    
                    # Count fields with data
                    fields_with_data = 0
                    
                    print("\\n🔍 Technical Config Field Check:")
                    for field, value in tech_fields.items():
                        if value and str(value).strip() and value != 'None':
                            fields_with_data += 1
                            status = "✅ HAS DATA"
                            display = str(value)[:40] + "..." if len(str(value)) > 40 else value
                        else:
                            status = "⚪ EMPTY"
                            display = f"'{value}'"
                        
                        print(f"   {field:25} | {status} | {display}")
                    
                    coverage = (fields_with_data / len(tech_fields)) * 100
                    print(f"\\n📊 Technical Config Coverage: {fields_with_data}/{len(tech_fields)} ({coverage:.1f}%)")
                    
                    return coverage >= 70  # At least 70% should have data
                    
                else:
                    print(f"❌ Detail API failed: {data}")
            else:
                print(f"❌ Detail API error: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Technical Config test failed: {e}")
        return False

def create_test_mop():
    """Create a test MOP dengan semua Technical Config fields"""
    print("\\n📝 Creating test MOP with complete Technical Config...")
    
    try:
        from app import app
        
        # Complete test data for final verification
        test_data = {
            'title': 'FINAL TEST - Activity Name & Technical Config Fix',
            'document_title': 'FINAL TEST - Activity Name & Technical Config Fix',
            'version': '3.0',
            'category': 'Final Test',
            'activity_name': 'Comprehensive Fix Verification Test',
            'work_type': 'System Enhancement',
            'summary': 'Final test to verify Activity Name display and Technical Config reload functionality',
            'executive_summary': 'Comprehensive test of all fixes applied to History MOP and Technical Config sections',
            
            # Complete Technical Config
            'hardware_requirements': 'FINAL TEST: Cisco ASR 9000 series router, backup power supply, console cables',
            'software_dependencies': 'FINAL TEST: IOS XR 7.3.2, TFTP server, monitoring tools',
            'network_prerequisites': 'FINAL TEST: Management network access, backup routing path established',
            'security_requirements': 'FINAL TEST: Security team approval, change control board sign-off',
            'personnel_requirements': 'FINAL TEST: Senior network engineer, system admin on standby',
            'external_dependencies': 'FINAL TEST: Vendor support confirmed, ISP coordination completed',
            
            # Implementation Timeline
            'prep_start_time': 'FINAL TEST: 01:00 AM',
            'prep_phase_duration': 'FINAL TEST: 45 minutes',
            'prep_activities': 'FINAL TEST: Configuration backup, lab testing, rollback procedures verification',
            'impl_start_time': 'FINAL TEST: 01:45 AM',
            'impl_phase_duration': 'FINAL TEST: 90 minutes',
            'impl_activities': 'FINAL TEST: Configuration deployment, connectivity testing, protocol verification',
            'verification_start_time': 'FINAL TEST: 03:15 AM',
            'verification_duration': 'FINAL TEST: 45 minutes',
            'verification_activities': 'FINAL TEST: End-to-end testing, performance validation, monitoring setup',
            
            # Communication & Success Criteria
            'communication_frequency': '10min',
            'notification_list': 'FINAL TEST: NOC team, network engineers, application teams, management',
            'technical_success_criteria': 'FINAL TEST: Zero packet loss, all protocols stable, latency within SLA',
            'business_success_criteria': 'FINAL TEST: No service interruption, user experience maintained',
            
            # Rollback
            'rollback_commands': 'FINAL TEST: configure terminal, rollback configuration last 1, commit',
            'recovery_time_objective': 'FINAL TEST: Maximum 5 minutes for service restoration'
        }
        
        with app.test_client() as client:
            response = client.post('/api/save_mop',
                                  json=test_data,
                                  headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.get_json()
                
                if result.get('success'):
                    mop_id = result.get('database_id')
                    print(f"✅ Test MOP created successfully - ID: {mop_id}")
                    return mop_id
                else:
                    print(f"❌ Save failed: {result}")
            else:
                print(f"❌ Save API error: {response.status_code}")
        
        return None
        
    except Exception as e:
        print(f"❌ Test MOP creation failed: {e}")
        return None

def main():
    """Main test function"""
    print("🎯 FINAL VERIFICATION: History MOP Activity Name & Technical Config Fix")
    print("=" * 80)
    
    # Test 1: Activity Name fix
    activity_name_success = test_activity_name_fix()
    
    # Test 2: Technical Config reload
    technical_config_success = test_technical_config_reload()
    
    # Test 3: Create new test MOP
    new_mop_id = create_test_mop()
    
    print(f"\\n🎯 FINAL VERIFICATION RESULTS:")
    print("=" * 50)
    print(f"✅ Activity Name Fix: {'SUCCESS' if activity_name_success else 'NEEDS ATTENTION'}")
    print(f"✅ Technical Config Reload: {'SUCCESS' if technical_config_success else 'NEEDS ATTENTION'}")
    print(f"✅ New Test MOP Created: {'SUCCESS' if new_mop_id else 'FAILED'}")
    
    overall_success = activity_name_success and technical_config_success and new_mop_id
    
    if overall_success:
        print(f"\\n🎉 ALL TESTS PASSED!")
        print(f"\\n📋 Manual Testing Instructions:")
        print(f"   1. Start application: python3 app.py")
        print(f"   2. Go to History MOP tab")
        print(f"   3. Verify Activity Name column shows correct data")
        print(f"   4. Click reload on MOP ID {new_mop_id}")
        print(f"   5. Switch to Technical Config tab")
        print(f"   6. Verify all fields are populated")
        print(f"   7. Check browser console for loading summary")
        
        print(f"\\n✨ Expected Results:")
        print(f"   - Activity Name shows: 'Comprehensive Fix Verification Test'")
        print(f"   - Technical Config fields contain 'FINAL TEST:' prefix")
        print(f"   - Console shows high percentage loading success")
        print(f"   - All sections properly populated")
        
    else:
        print(f"\\n⚠️  SOME TESTS FAILED - Review results above")
        
        if not activity_name_success:
            print(f"   - Activity Name: Check API mapping in get_mop_history")
        if not technical_config_success:
            print(f"   - Technical Config: Check database save and API retrieval")
        if not new_mop_id:
            print(f"   - Test MOP Creation: Check save functionality")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)