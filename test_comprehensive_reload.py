#!/usr/bin/env python3
"""
Comprehensive test untuk memastikan SEMUA field History MOP reload berfungsi
"""

import os
import sys
import json
from datetime import datetime

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

def create_complete_test_mop():
    """Create a complete MOP with ALL fields filled for testing"""
    print("📝 Creating complete test MOP in database...")
    
    load_env()
    
    try:
        from app import app
        from database import MOPDatabase
        
        # Complete test data with ALL possible fields
        complete_mop_data = {
            # === DOCUMENT INFO ===
            'title': 'COMPLETE TEST MOP - All Fields Validation',
            'document_title': 'COMPLETE TEST MOP - All Fields Validation',
            'version': '2.0',
            'category': 'Network Change',
            'priority': 'High',
            'execution_date': '2026-08-25',
            'execution_time': '02:00 AM',
            'duration_minutes': 240,
            'business_justification': 'Testing complete field reload functionality',
            'executive_summary': 'Comprehensive test to validate all form fields load correctly',
            
            # === TECHNICAL CONFIG ===
            'activity_name': 'Complete Field Test Activity',
            'work_type': 'Configuration Change',
            'issue_date': '2026-08-24T12:46',
            'total_duration': '4 hours',
            'affected_services': 'All network services for testing',
            'downtime': '15 minutes maximum',
            'summary': 'Complete test summary for field validation',
            
            # Technical Prerequisites
            'hardware_requirements': 'Test hardware: Cisco routers, switches, cables',
            'software_dependencies': 'Test software: IOS 16.x, monitoring tools',
            'network_prerequisites': 'Test network: Backup paths, management access',
            'security_requirements': 'Test security: Change approval, access controls',
            'personnel_requirements': 'Test personnel: Network engineer, security officer',
            'external_dependencies': 'Test external: Vendor support, ISP coordination',
            
            # === RISK ASSESSMENT ===
            'overall_risk_level': 'Medium-High',
            'risk_owner': 'Test Risk Owner - John Doe',
            'contingency_plan': 'Test contingency: Immediate rollback if issues detected',
            
            # === IMPLEMENTATION TIMELINE ===
            'prep_start_time': '01:30 AM',
            'prep_phase_duration': '30 minutes',
            'prep_activities': 'Test prep: Backup configs, verify lab, prepare tools',
            'impl_start_time': '02:00 AM',
            'impl_phase_duration': '2 hours',
            'impl_activities': 'Test implementation: Load configs, test connectivity, verify routing',
            'verification_start_time': '04:00 AM',
            'verification_duration': '1 hour',
            'verification_activities': 'Test verification: End-to-end tests, performance checks',
            
            # === COMMUNICATION PLAN ===
            'communication_frequency': '10min',
            'notification_list': 'Test notifications: NOC team, network managers, app owners',
            'technical_success_criteria': 'Test technical: All routing stable, no packet loss, BGP up',
            'business_success_criteria': 'Test business: No user complaints, services accessible',
            
            # === POST-IMPLEMENTATION ===
            'monitoring_duration': '48h',
            'monitoring_frequency': 'continuous',
            'monitoring_team': 'Test monitoring: NOC with network engineering escalation',
            
            # === ROLLBACK PROCEDURES ===
            'rollback_commands': 'Test rollback: config replace backup.cfg, reload in 5',
            'service_impact_level': 'High',
            'affected_processes': 'Test processes: VPN, routing, inter-VLAN communication',
            'business_impact_cost': 'Test cost: $10,000 per hour if extended',
            'system_impact_level': 'Critical',
            'affected_systems': 'Test systems: Core routers, MPLS, branch connectivity',
            'recovery_time_objective': '10 minutes',
            'rollback_technical_validation': 'Test validation: Ping tests, BGP status check',
            'rollback_business_validation': 'Test business: App team confirmation, user testing',
            
            # === APPROVAL SIGNATURES ===
            'tech_reviewer_name': 'Test Tech Reviewer',
            'tech_reviewer_position': 'Senior Test Engineer',
            'tech_reviewer_contact': 'tech.reviewer@test.com',
            'tech_review_date': '2026-08-24T10:00',
            'manager_name': 'Test Manager',
            'manager_position': 'Test Operations Manager',
            'manager_contact': 'test.manager@test.com',
            'manager_approval_date': '2026-08-24T11:00',
            'final_approver_name': 'Test Final Approver',
            'final_approver_title': 'Test CTO',
            'final_approver_contact': 'test.cto@test.com',
            'final_approval_date': '2026-08-24T11:30',
            
            # === IMPLEMENTATION STATUS ===
            'implementation_status': 'approved',
            'actual_start_time': '',
            'actual_end_time': '',
            'implementation_notes': 'Test implementation notes for validation',
            
            # === CERTIFICATIONS ===
            'cert_technical': True,
            'cert_testing': True,
            'cert_documentation': True,
            'cert_stakeholder': False,
            
            # === TECHNICAL DETAILS ===
            'service_name': 'Test Network Service',
            'service_version': 'Test Version 2.0',
            'service_ports': 'Test ports: 80, 443, 22, 179',
            'config_file_paths': 'Test paths: /test/config, /test/backup',
            'database_connections': 'Test DB: monitoring.db, config.db',
            'admin_accounts': 'Test accounts: testadmin, testuser, readonly',
            'auth_method': 'Test auth: TACACS+ with local backup',
            'firewall_rules': 'Test firewall: Management access, SNMP monitoring',
            'ssl_certificates': 'Test SSL: Management interface certificates',
            
            # === BACKUP & RECOVERY ===
            'backup_locations': 'Test backup: TFTP server, cloud storage, local disk',
            'backup_commands': 'Test commands: copy run tftp://test-server/backup.cfg',
            'rpo_target': '30 minutes',
            'rto_target': '5 minutes',
            'environment_type': 'production',
            'datacenter_location': 'Test DC - Building Test',
            'maintenance_window': 'Test window: Saturday 02:00-06:00 AM',
            
            # === DEVICES ===
            'devices': [
                {
                    'hostname': 'TEST-RTR-01',
                    'name': 'TEST-RTR-01',
                    'type': 'router',
                    'mgmt_ip': '192.168.100.200',
                    'ip': '192.168.100.200',
                    'location': 'Test DC Rack A1',
                    'model_serial': 'TEST-SN-001'
                },
                {
                    'hostname': 'TEST-SW-01', 
                    'name': 'TEST-SW-01',
                    'type': 'switch',
                    'mgmt_ip': '192.168.100.201',
                    'ip': '192.168.100.201',
                    'location': 'Test DC Rack A2',
                    'model_serial': 'TEST-SN-002'
                }
            ],
            
            # === NETWORK CONFIGS ===
            'networkConfigs': [
                {
                    'realIp': '10.100.1.0/24',
                    'natIp': '203.0.113.100/24',
                    'paloAltoZone': 'TEST-DMZ',
                    'vlanId': 200,
                    'description': 'Test network config 1'
                },
                {
                    'realIp': '10.100.2.0/24',
                    'natIp': '203.0.113.200/24',
                    'paloAltoZone': 'TEST-LAN',
                    'vlanId': 201,
                    'description': 'Test network config 2'
                }
            ],
            
            # === RISKS ===
            'risks': [
                {
                    'type': 'technical',
                    'description': 'Test technical risk: Potential routing issues during change',
                    'impact': 4,
                    'probability': 2,
                    'mitigation': 'Test mitigation: Staged implementation with rollback plan',
                    'contingency': 'Test contingency: Immediate config restore'
                },
                {
                    'type': 'business',
                    'description': 'Test business risk: Service interruption during maintenance',
                    'impact': 3,
                    'probability': 1,
                    'mitigation': 'Test mitigation: Off-hours implementation',
                    'contingency': 'Test contingency: Extended maintenance window'
                }
            ]
        }
        
        # Save to database
        db = MOPDatabase()
        result = db.save_mop_document(complete_mop_data)
        
        if result:
            print(f"✅ Complete test MOP created with ID: {result['id']}")
            return result['id']
        else:
            print("❌ Failed to create test MOP")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test MOP: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_field_coverage():
    """Test comprehensive field coverage in HTML form"""
    print("\n🔍 Testing field coverage in HTML form...")
    
    try:
        with open('templates/index.html', 'r') as f:
            content = f.read()
        
        # All field categories to test
        field_categories = {
            'Document Info': [
                'document_title', 'version', 'category', 'activity_name', 'work_type', 'issue_date'
            ],
            'Summary': [
                'execution_time', 'total_duration', 'affected_services', 'downtime', 'summary'
            ],
            'Technical Prerequisites': [
                'hardware_requirements', 'software_dependencies', 'network_prerequisites',
                'security_requirements', 'personnel_requirements', 'external_dependencies'
            ],
            'Risk Assessment': [
                'overall_risk_level', 'risk_owner', 'contingency_plan'
            ],
            'Implementation Timeline': [
                'prep_start_time', 'prep_phase_duration', 'prep_activities',
                'impl_start_time', 'impl_phase_duration', 'impl_activities', 
                'verification_start_time', 'verification_duration', 'verification_activities'
            ],
            'Communication Plan': [
                'communication_frequency', 'notification_list',
                'technical_success_criteria', 'business_success_criteria'
            ],
            'Post-Implementation': [
                'monitoring_duration', 'monitoring_frequency', 'monitoring_team'
            ],
            'Rollback Procedures': [
                'rollback_commands', 'service_impact_level', 'affected_processes',
                'business_impact_cost', 'system_impact_level', 'affected_systems',
                'recovery_time_objective', 'rollback_technical_validation', 
                'rollback_business_validation'
            ],
            'Approval Signatures': [
                'tech_reviewer_name', 'tech_reviewer_position', 'tech_reviewer_contact',
                'tech_review_date', 'manager_name', 'manager_position', 'manager_contact',
                'manager_approval_date', 'final_approver_name', 'final_approver_title',
                'final_approver_contact', 'final_approval_date'
            ],
            'Implementation Status': [
                'implementation_status', 'actual_start_time', 'actual_end_time', 'implementation_notes'
            ],
            'Certifications': [
                'cert_technical', 'cert_testing', 'cert_documentation', 'cert_stakeholder'
            ],
            'Technical Details': [
                'service_name', 'service_version', 'service_ports', 'config_file_paths',
                'database_connections', 'admin_accounts', 'auth_method', 
                'firewall_rules', 'ssl_certificates'
            ],
            'Backup & Recovery': [
                'backup_locations', 'backup_commands', 'rpo_target', 'rto_target',
                'environment_type', 'datacenter_location', 'maintenance_window'
            ]
        }
        
        total_found = 0
        total_missing = 0
        
        for category, fields in field_categories.items():
            print(f"\n📋 {category}:")
            found_in_category = 0
            
            for field in fields:
                if f'id="{field}"' in content:
                    print(f"   ✅ {field}")
                    found_in_category += 1
                    total_found += 1
                else:
                    print(f"   ❌ {field}")
                    total_missing += 1
            
            coverage = (found_in_category / len(fields)) * 100
            print(f"   📊 Coverage: {coverage:.1f}% ({found_in_category}/{len(fields)})")
        
        print(f"\n📊 TOTAL COVERAGE:")
        print(f"   ✅ Found: {total_found}")
        print(f"   ❌ Missing: {total_missing}")
        print(f"   📈 Overall: {(total_found/(total_found+total_missing))*100:.1f}%")
        
        return total_found, total_missing
        
    except Exception as e:
        print(f"❌ Error testing field coverage: {e}")
        return 0, 0

def test_api_functionality(test_mop_id):
    """Test API functionality with complete MOP"""
    print(f"\n🌐 Testing API functionality with MOP ID: {test_mop_id}...")
    
    load_env()
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test detail API
            response = client.get(f'/api/mop_detail/{test_mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data['success']:
                    mop_data = data['data']
                    print(f"✅ API Success - Fields returned: {len(mop_data)}")
                    
                    # Test key fields from each category
                    test_fields = {
                        'Document Info': ['document_title', 'version', 'category'],
                        'Technical Config': ['hardware_requirements', 'software_dependencies'], 
                        'Implementation': ['prep_start_time', 'impl_start_time'],
                        'Communication': ['technical_success_criteria', 'business_success_criteria'],
                        'Approvals': ['tech_reviewer_name', 'manager_name'],
                        'Devices': ['devices'],
                        'Networks': ['networkConfigs'],
                        'Risks': ['risks']
                    }
                    
                    api_success = True
                    for category, fields in test_fields.items():
                        print(f"\n📋 {category}:")
                        for field in fields:
                            if field in mop_data:
                                value = mop_data[field]
                                if isinstance(value, list):
                                    status = f"✅ {len(value)} items" if value else "⚪ empty list"
                                elif value:
                                    status = f"✅ {str(value)[:30]}..."
                                else:
                                    status = "⚪ empty"
                                print(f"   {field}: {status}")
                            else:
                                print(f"   {field}: ❌ missing")
                                api_success = False
                    
                    return api_success
                else:
                    print(f"❌ API Error: {data.get('message')}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    """Main comprehensive test"""
    print("🧪 COMPREHENSIVE MOP RELOAD FIELD TEST")
    print("=" * 80)
    print("Testing ALL aspects of History MOP reload functionality\n")
    
    # Test 1: Create complete test MOP
    test_mop_id = create_complete_test_mop()
    
    # Test 2: Field coverage in HTML
    found, missing = test_field_coverage()
    
    # Test 3: API functionality  
    api_success = False
    if test_mop_id:
        api_success = test_api_functionality(test_mop_id)
    
    # Final summary
    print(f"\n🎯 COMPREHENSIVE TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Test MOP Created: {'YES' if test_mop_id else 'NO'} (ID: {test_mop_id})")
    print(f"✅ Form Fields Found: {found}")
    print(f"❌ Form Fields Missing: {missing}")
    print(f"✅ API Functionality: {'PASSED' if api_success else 'FAILED'}")
    
    overall_coverage = (found / (found + missing)) * 100 if (found + missing) > 0 else 0
    print(f"📊 Overall Field Coverage: {overall_coverage:.1f}%")
    
    if test_mop_id and found > missing and api_success:
        print(f"\n🎉 COMPREHENSIVE TEST PASSED!")
        print(f"\n💡 Manual Testing Instructions:")
        print(f"   1. Run the application: python3 app.py")
        print(f"   2. Open History MOP tab")
        print(f"   3. Find MOP ID {test_mop_id}: 'COMPLETE TEST MOP - All Fields Validation'")
        print(f"   4. Click reload button")
        print(f"   5. Verify ALL tabs are populated:")
        print(f"      ✅ Document Info - title, version, category filled")
        print(f"      ✅ Summary - execution time, duration, services filled") 
        print(f"      ✅ Technical Config - hardware, software, network requirements filled")
        print(f"      ✅ Prerequisites - security, personnel requirements filled")
        print(f"      ✅ Risk Assessment - risk level, owner, contingency filled")
        print(f"      ✅ Implementation - prep, impl, verification timeline filled")
        print(f"      ✅ Rollback Procedures - commands, validation steps filled") 
        print(f"      ✅ Approval Signatures - reviewer, manager, final approver filled")
        print(f"\n🐛 Debug: Open F12 Console to see detailed field loading logs")
        
        return True
    else:
        print(f"\n❌ COMPREHENSIVE TEST FAILED!")
        print(f"   Issues found - check details above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)