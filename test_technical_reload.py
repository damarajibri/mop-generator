#!/usr/bin/env python3
"""
Test script untuk memverifikasi reload data Technical Config dan Implementation
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

def test_form_fields():
    """Test which form fields are available in the HTML"""
    print("🔍 Testing available form fields in HTML template...")
    
    try:
        with open('templates/index.html', 'r') as f:
            content = f.read()
        
        # Common field IDs to check
        technical_fields = [
            'hardware_requirements', 'software_dependencies', 'network_prerequisites',
            'security_requirements', 'personnel_requirements', 'external_dependencies',
            'prep_start_time', 'prep_phase_duration', 'prep_activities',
            'impl_start_time', 'impl_phase_duration', 'impl_activities',
            'verification_start_time', 'verification_duration', 'verification_activities',
            'communication_frequency', 'notification_list',
            'technical_success_criteria', 'business_success_criteria',
            'monitoring_duration', 'monitoring_frequency', 'monitoring_team',
            'rollback_commands', 'service_impact_level', 'affected_processes',
            'tech_reviewer_name', 'manager_name', 'final_approver_name'
        ]
        
        found_fields = []
        missing_fields = []
        
        for field in technical_fields:
            if f'id="{field}"' in content:
                found_fields.append(field)
            else:
                missing_fields.append(field)
        
        print(f"✅ Found fields ({len(found_fields)}):")
        for field in found_fields:
            print(f"   - {field}")
        
        if missing_fields:
            print(f"❌ Missing fields ({len(missing_fields)}):")
            for field in missing_fields:
                print(f"   - {field}")
        
        return len(found_fields), len(missing_fields)
        
    except Exception as e:
        print(f"❌ Error checking fields: {e}")
        return 0, 0

def test_api_response():
    """Test API response structure"""
    print("\\n🔍 Testing API response data structure...")
    
    load_env()
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Get history first
            history_response = client.get('/api/mop_history?page=1&page_size=1')
            history_data = history_response.get_json()
            
            if history_data['success'] and history_data['data']:
                test_id = history_data['data'][0]['id']
                print(f"Testing with MOP ID: {test_id}")
                
                # Get detailed data
                detail_response = client.get(f'/api/mop_detail/{test_id}')
                detail_data = detail_response.get_json()
                
                if detail_data['success']:
                    mop_data = detail_data['data']
                    
                    # Check key sections
                    sections = {
                        'Basic Info': ['document_title', 'version', 'category'],
                        'Technical Prerequisites': ['hardware_requirements', 'software_dependencies', 'network_prerequisites'],
                        'Implementation Timeline': ['prep_start_time', 'impl_start_time', 'verification_start_time'],
                        'Communication': ['communication_frequency', 'notification_list'],
                        'Success Criteria': ['technical_success_criteria', 'business_success_criteria'],
                        'Monitoring': ['monitoring_duration', 'monitoring_frequency'],
                        'Rollback': ['rollback_commands', 'service_impact_level'],
                        'Approvals': ['tech_reviewer_name', 'manager_name', 'final_approver_name']
                    }
                    
                    for section_name, fields in sections.items():
                        print(f"\\n📋 {section_name}:")
                        section_found = 0
                        for field in fields:
                            if field in mop_data and mop_data[field] is not None:
                                value = str(mop_data[field])[:30]
                                if value:
                                    print(f"   ✅ {field}: {value}...")
                                    section_found += 1
                                else:
                                    print(f"   ⚪ {field}: (empty)")
                            else:
                                print(f"   ❌ {field}: (missing)")
                        
                        coverage = (section_found / len(fields)) * 100
                        print(f"   📊 Coverage: {coverage:.0f}% ({section_found}/{len(fields)})")
                
                return True
            else:
                print("❌ No MOP data found for testing")
                return False
                
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 MOP Data Reload - Technical Config & Implementation Test")
    print("=" * 70)
    
    # Test 1: Check form fields
    found, missing = test_form_fields()
    
    # Test 2: Check API response
    api_success = test_api_response()
    
    # Summary
    print("\\n📊 Test Summary:")
    print("=" * 40)
    print(f"✅ Form fields found: {found}")
    print(f"❌ Form fields missing: {missing}")
    print(f"🌐 API response test: {'✅ PASSED' if api_success else '❌ FAILED'}")
    
    if found > 0 and api_success:
        print("\\n🎉 Technical Config & Implementation reload is ready!")
        print("\\n💡 Expected behavior:")
        print("   1. Click History MOP tab")
        print("   2. Click reload button on any MOP")
        print("   3. Check Technical Config tab - fields should be populated")
        print("   4. Check Implementation tab - timeline should be loaded")
        print("   5. Check other tabs for complete data")
        print("\\n🐛 Debug: Open browser console (F12) to see detailed field loading logs")
    else:
        print("\\n⚠️  Some issues found - check the details above")
    
    return found > missing and api_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)