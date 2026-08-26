#!/usr/bin/env python3
"""
Debug Script: Technical Config Form Loading
Test form loading functionality untuk Technical Config fields
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

def debug_form_field_mapping():
    """Debug form field mapping untuk Technical Config"""
    print("🔍 Debugging Technical Config form field mapping...")
    
    load_env()
    
    try:
        from app import app
        
        # Test MOP ID 40 yang punya Technical Config data
        mop_id = 40
        
        with app.test_client() as client:
            print(f"📡 Getting data for MOP ID {mop_id}...")
            
            # Get data from API
            response = client.get(f'/api/mop_detail/{mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    mop_data = data['data']
                    print(f"✅ Got MOP data with {len(mop_data)} fields")
                    
                    # Focus on Technical Config fields mapping
                    tech_config_fields = {
                        # Prerequisites section
                        'hardware_requirements': 'Hardware Requirements',
                        'software_dependencies': 'Software Dependencies', 
                        'network_prerequisites': 'Network Prerequisites',
                        'security_requirements': 'Security Requirements',
                        'personnel_requirements': 'Personnel Requirements',
                        'external_dependencies': 'External Dependencies',
                        
                        # Implementation Timeline
                        'prep_start_time': 'Prep Start Time',
                        'prep_phase_duration': 'Prep Phase Duration', 
                        'prep_activities': 'Prep Activities',
                        'impl_start_time': 'Implementation Start Time',
                        'impl_phase_duration': 'Implementation Phase Duration',
                        'impl_activities': 'Implementation Activities',
                        'verification_start_time': 'Verification Start Time',
                        'verification_duration': 'Verification Duration',
                        'verification_activities': 'Verification Activities',
                        
                        # Communication Plan
                        'communication_frequency': 'Communication Frequency',
                        'notification_list': 'Notification List',
                        'technical_success_criteria': 'Technical Success Criteria',
                        'business_success_criteria': 'Business Success Criteria',
                        
                        # Rollback Procedures
                        'rollback_commands': 'Rollback Commands',
                        'service_impact_level': 'Service Impact Level',
                        'affected_processes': 'Affected Processes',
                        'business_impact_cost': 'Business Impact Cost',
                        'system_impact_level': 'System Impact Level',
                        'affected_systems': 'Affected Systems',
                        'recovery_time_objective': 'Recovery Time Objective'
                    }
                    
                    print(f"\\n🔧 Technical Config Field Analysis:")
                    print("=" * 80)
                    
                    # Check each field's data
                    has_data_count = 0
                    total_count = 0
                    
                    for field_id, field_name in tech_config_fields.items():
                        total_count += 1
                        value = mop_data.get(field_id)
                        
                        if value and str(value).strip() and value != 'None':
                            has_data_count += 1
                            status = "✅ HAS DATA"
                            display_value = str(value)[:60] + "..." if len(str(value)) > 60 else value
                        else:
                            status = "⚪ EMPTY"
                            display_value = f"'{value}'"
                        
                        print(f"  {field_id:30} | {status} | {display_value}")
                    
                    coverage = (has_data_count / total_count) * 100
                    print("=" * 80)
                    print(f"📊 Technical Config Data Coverage: {has_data_count}/{total_count} fields ({coverage:.1f}%)")
                    
                    if coverage < 50:
                        print("\\n⚠️  LOW COVERAGE - Possible issues:")
                        print("   1. Data not saved properly to database")
                        print("   2. Database column mapping issues") 
                        print("   3. API retrieval problems")
                        
                        # Debug specific database content
                        print("\\n🔍 Direct database check...")
                        debug_database_content(mop_id)
                    else:
                        print(f"\\n✅ Good coverage - data should load properly in form")
                        
                        # Generate JavaScript test code
                        print(f"\\n🧪 JavaScript console test code:")
                        print("// Run this in browser console to test form loading:")
                        print("fetch('/api/mop_detail/40')")
                        print("  .then(r => r.json())")
                        print("  .then(data => {")
                        print("    console.log('API Data:', data);")
                        print("    if (data.success) {")
                        print("      loadDataIntoForm(data.data);")
                        print("    }")
                        print("  });")
                        
                    return coverage >= 50
                else:
                    print(f"❌ API failed: {data}")
            else:
                print(f"❌ API error: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_database_content(mop_id):
    """Debug database content directly"""
    try:
        from database import MOPDatabase
        
        db = MOPDatabase()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get specific Technical Config fields from database
        cursor.execute("""
            SELECT hardware_requirements, software_dependencies, network_prerequisites,
                   prep_start_time, impl_start_time, verification_start_time,
                   technical_success_criteria, rollback_commands
            FROM mop_documents WHERE id = ?
        """, (mop_id,))
        
        row = cursor.fetchone()
        
        if row:
            field_names = [
                'hardware_requirements', 'software_dependencies', 'network_prerequisites',
                'prep_start_time', 'impl_start_time', 'verification_start_time', 
                'technical_success_criteria', 'rollback_commands'
            ]
            
            print("\\n🗄️  Direct Database Values:")
            for i, field_name in enumerate(field_names):
                value = row[i]
                status = "✅ HAS DATA" if value else "⚪ NULL/EMPTY"
                display = str(value)[:50] + "..." if value and len(str(value)) > 50 else value
                print(f"   {field_name:25} | {status} | {display}")
        else:
            print(f"❌ No record found for MOP ID {mop_id}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database debug failed: {e}")

def main():
    """Main debug function"""
    print("🎯 DEBUG: Technical Config Form Loading")
    print("=" * 60)
    
    success = debug_form_field_mapping()
    
    print(f"\\n🎯 DEBUG RESULTS:")
    print("=" * 30)
    
    if success:
        print("✅ Technical Config data is available")
        print("\\n💡 If form still not loading:")
        print("   1. Check browser console for JavaScript errors")
        print("   2. Verify form field IDs match loadDataIntoForm function")
        print("   3. Test JavaScript manually in browser console")
        print("   4. Check if Technical Config tab is active when loading")
    else:
        print("❌ Technical Config data issues found")
        print("\\n🔧 Next steps:")
        print("   1. Fix database save mechanism")
        print("   2. Verify field mapping in save function")
        print("   3. Re-test data save and retrieval")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)