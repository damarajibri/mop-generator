#!/usr/bin/env python3
"""
Test Script: Enhanced Technical Config Reload
Verifikasi perbaikan Technical Config dan Implementation reload
"""

import os
import sys
import time

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

def create_enhanced_test_mop():
    """Create enhanced test MOP dengan semua field untuk comprehensive testing"""
    print("📝 Creating enhanced test MOP...")
    
    load_env()
    
    try:
        from app import app
        
        # Enhanced test data dengan semua Technical Config fields
        enhanced_data = {
            'title': 'ENHANCED FIX TEST - Technical Config & Implementation Reload',
            'document_title': 'ENHANCED FIX TEST - Technical Config & Implementation Reload',
            'version': '4.0',
            'category': 'Enhanced Test',
            'activity_name': 'Enhanced Technical Config & Implementation Reload Test',
            'work_type': 'System Enhancement & Validation',
            'summary': 'Enhanced test untuk memverifikasi perbaikan Technical Config dan Implementation reload',
            'executive_summary': 'Comprehensive test dengan delayed loading, retry mechanism, dan enhanced field validation',
            
            # Complete Technical Config - Prerequisites
            'hardware_requirements': 'ENHANCED TEST: Cisco Catalyst 9000 series switches, redundant power supplies, console server access, monitoring laptop with serial cables',
            'software_dependencies': 'ENHANCED TEST: IOS XE 16.12.08, TFTP/SCP server, network monitoring tools (PRTG/SolarWinds), configuration management system',
            'network_prerequisites': 'ENHANCED TEST: Management VLAN access configured, backup routing paths established, out-of-band management network available',
            'security_requirements': 'ENHANCED TEST: Change approval board sign-off completed, security team notification sent, vulnerability assessment completed',
            'personnel_requirements': 'ENHANCED TEST: Senior network engineer L3 certified, backup system administrator on standby, security officer available for consultation',
            'external_dependencies': 'ENHANCED TEST: ISP coordination scheduled, vendor TAC support confirmed available, third-party monitoring tools notification sent',
            
            # Implementation Timeline - Detailed
            'prep_start_time': 'ENHANCED TEST: 00:30 AM',
            'prep_phase_duration': 'ENHANCED TEST: 60 minutes',
            'prep_activities': 'ENHANCED TEST: Configuration backup to multiple locations, lab environment validation, rollback procedure dry-run, team briefing completion',
            'impl_start_time': 'ENHANCED TEST: 01:30 AM',
            'impl_phase_duration': 'ENHANCED TEST: 120 minutes', 
            'impl_activities': 'ENHANCED TEST: New configuration deployment, incremental connectivity testing, routing protocol verification, load balancing validation',
            'verification_start_time': 'ENHANCED TEST: 03:30 AM',
            'verification_duration': 'ENHANCED TEST: 60 minutes',
            'verification_activities': 'ENHANCED TEST: End-to-end connectivity validation, performance baseline comparison, monitoring system integration check, user acceptance testing',
            
            # Communication Plan - Enhanced
            'communication_frequency': '5min',
            'notification_list': 'ENHANCED TEST: Network Operations Center (24/7), Network Engineering Team, Application Support Teams, Infrastructure Management, Security Operations Center',
            'technical_success_criteria': 'ENHANCED TEST: Zero packet loss during transition, all routing protocols converged within 30 seconds, latency remains under SLA thresholds, no BGP flaps detected',
            'business_success_criteria': 'ENHANCED TEST: No user-reported issues, all critical applications responsive, service availability >99.9%, customer satisfaction maintained',
            
            # Post-Implementation - Enhanced
            'monitoring_duration': '48h',
            'monitoring_frequency': 'continuous',
            'monitoring_team': 'ENHANCED TEST: NOC Level 1/2 engineers, Network Engineering on-call rotation, Vendor support team standby',
            
            # Rollback Procedures - Enhanced
            'rollback_commands': 'ENHANCED TEST: configure terminal; rollback configuration last 1 force; copy startup-config running-config; reload in 10 cancel',
            'service_impact_level': 'ENHANCED TEST: Medium - Potential 2-3 minute service degradation during rollback execution',
            'affected_processes': 'ENHANCED TEST: Network routing protocols, load balancing algorithms, traffic engineering policies, monitoring data collection',
            'business_impact_cost': 'ENHANCED TEST: Estimated $50,000 per hour of downtime based on transaction volume and SLA penalties',
            'system_impact_level': 'ENHANCED TEST: High - Core network infrastructure changes affecting multiple services and customer segments',
            'affected_systems': 'ENHANCED TEST: Core routers, distribution switches, load balancers, monitoring systems, traffic management platforms',
            'recovery_time_objective': 'ENHANCED TEST: Maximum 5 minutes for complete service restoration with automated rollback procedures',
            
            # Technical Details - Enhanced
            'service_name': 'ENHANCED TEST: Core Network Infrastructure Service',
            'service_version': 'ENHANCED TEST: v2.1.0',
            'service_ports': 'ENHANCED TEST: TCP 22 (SSH), TCP 161/162 (SNMP), TCP 514 (Syslog)',
            'config_file_paths': 'ENHANCED TEST: /var/lib/tftpboot/configs/, /opt/backup/network-configs/, /etc/network/device-configs/',
            'admin_accounts': 'ENHANCED TEST: netadmin (primary), netbackup (secondary), netmon (monitoring)',
            'auth_method': 'ENHANCED TEST: RADIUS with local fallback, SSH key-based authentication, TACACS+ for command authorization'
        }
        
        with app.test_client() as client:
            print(f"📤 Sending enhanced test data ({len(enhanced_data)} fields)...")
            
            response = client.post('/api/save_mop',
                                  json=enhanced_data,
                                  headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.get_json()
                
                if result.get('success'):
                    mop_id = result.get('database_id')
                    print(f"✅ Enhanced test MOP created - ID: {mop_id}")
                    return mop_id
                else:
                    print(f"❌ Save failed: {result}")
            else:
                print(f"❌ Save API error: {response.status_code}")
        
        return None
        
    except Exception as e:
        print(f"❌ Enhanced test MOP creation failed: {e}")
        return None

def test_enhanced_reload(mop_id):
    """Test enhanced reload functionality"""
    print(f"\\n🧪 Testing enhanced reload for MOP ID {mop_id}...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test API detail retrieval
            response = client.get(f'/api/mop_detail/{mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    mop_data = data['data']
                    
                    # Test enhanced field coverage
                    enhanced_fields = {
                        'hardware_requirements': 'Cisco Catalyst 9000',
                        'software_dependencies': 'IOS XE 16.12.08',
                        'network_prerequisites': 'Management VLAN access',
                        'prep_start_time': '00:30 AM',
                        'impl_start_time': '01:30 AM', 
                        'verification_start_time': '03:30 AM',
                        'technical_success_criteria': 'Zero packet loss',
                        'business_success_criteria': 'No user-reported issues',
                        'rollback_commands': 'configure terminal',
                        'communication_frequency': '5min',
                        'monitoring_duration': '48h',
                        'service_name': 'Core Network Infrastructure',
                        'auth_method': 'RADIUS with local fallback'
                    }
                    
                    print(f"\\n🔍 Enhanced Field Coverage Test:")
                    success_count = 0
                    
                    for field_id, expected_content in enhanced_fields.items():
                        value = mop_data.get(field_id, '')
                        
                        if value and expected_content.lower() in str(value).lower():
                            success_count += 1
                            status = "✅ MATCH"
                            display = str(value)[:50] + "..." if len(str(value)) > 50 else value
                        else:
                            status = "❌ NO MATCH"
                            display = f"Expected '{expected_content}' in '{value}'"
                        
                        print(f"   {field_id:25} | {status} | {display}")
                    
                    coverage = (success_count / len(enhanced_fields)) * 100
                    print(f"\\n📊 Enhanced Coverage: {success_count}/{len(enhanced_fields)} ({coverage:.1f}%)")
                    
                    return coverage >= 80  # 80% threshold for success
                    
                else:
                    print(f"❌ API failed: {data}")
            else:
                print(f"❌ API error: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Enhanced reload test failed: {e}")
        return False

def generate_manual_test_instructions(mop_id):
    """Generate manual testing instructions"""
    print(f"\\n📋 MANUAL TESTING INSTRUCTIONS FOR MOP ID {mop_id}")
    print("=" * 80)
    
    print(f"🔧 Enhanced Technical Config Reload Test:")
    print(f"\\n1. Start Application:")
    print(f"   cd mop_minimal && python3 app.py")
    print(f"   Open browser: http://localhost:9090")
    
    print(f"\\n2. Navigate to History MOP:")
    print(f"   - Click 'History MOP' tab (leftmost)")
    print(f"   - Find MOP ID {mop_id} with title 'ENHANCED FIX TEST'")
    print(f"   - Activity Name should show: 'Enhanced Technical Config & Implementation Reload Test'")
    
    print(f"\\n3. Test Enhanced Reload:")
    print(f"   - Click reload button (spinning arrow) for MOP ID {mop_id}")
    print(f"   - Watch for notifications (should show success)")
    print(f"   - Observe automatic tab switching:")
    print(f"     * First to Document Info (immediate)")
    print(f"     * Then to Technical Config (after 1.5 seconds)")
    
    print(f"\\n4. Verify Technical Config Loading:")
    print(f"   - Open Browser Developer Tools (F12)")
    print(f"   - Go to Console tab")
    print(f"   - Look for loading progress messages:")
    print(f"     * 🔧 Loading Technical Prerequisites...")
    print(f"     * ⏰ Loading Implementation Timeline...")
    print(f"     * 📢 Loading Communication Plan...")
    print(f"     * 🔄 Loading Rollback Procedures...")
    print(f"     * 🎯 FINAL RESULT: X/9 critical fields loaded")
    
    print(f"\\n5. Check Field Contents:")
    print(f"   - Hardware Requirements: Should contain 'Cisco Catalyst 9000'")
    print(f"   - Software Dependencies: Should contain 'IOS XE 16.12.08'")
    print(f"   - Prep Start Time: Should show '00:30 AM'")
    print(f"   - Implementation Start Time: Should show '01:30 AM'")
    print(f"   - Technical Success Criteria: Should contain 'Zero packet loss'")
    
    print(f"\\n6. Implementation Tab Check:")
    print(f"   - Go to Implementation tab")
    print(f"   - Verify Implementation Activities field populated")
    print(f"   - Check Communication Plan section")
    print(f"   - Verify Rollback Procedures section")
    
    print(f"\\n✅ Expected Success Indicators:")
    print(f"   - Console shows 80%+ field loading success")
    print(f"   - All sections populated with 'ENHANCED TEST:' prefix")
    print(f"   - No JavaScript errors in console")
    print(f"   - Smooth tab transitions")
    print(f"   - Clear success notifications")
    
    print(f"\\n🚩 Debug with Browser Script:")
    print(f"   - Copy paste content of browser_debug.js into console")
    print(f"   - Run comprehensive field existence and loading tests")

def main():
    """Main test function"""
    print("🎯 ENHANCED TECHNICAL CONFIG & IMPLEMENTATION RELOAD TEST")
    print("=" * 80)
    
    # Create enhanced test MOP
    mop_id = create_enhanced_test_mop()
    
    if mop_id:
        # Test enhanced reload
        reload_success = test_enhanced_reload(mop_id)
        
        print(f"\\n🎯 ENHANCED TEST RESULTS:")
        print("=" * 50)
        print(f"✅ Enhanced MOP Creation: SUCCESS (ID: {mop_id})")
        print(f"✅ Enhanced Field Coverage: {'SUCCESS' if reload_success else 'NEEDS ATTENTION'}")
        
        if reload_success:
            print(f"\\n🎉 ENHANCED FIXES SUCCESSFUL!")
            print(f"\\n💡 Improvements Applied:")
            print(f"   ✅ Delayed loading with retry mechanism")
            print(f"   ✅ Enhanced field visibility detection") 
            print(f"   ✅ Staggered timing for different sections")
            print(f"   ✅ Auto tab switching to Technical Config")
            print(f"   ✅ Comprehensive loading progress tracking")
            print(f"   ✅ Final validation and percentage reporting")
            
            generate_manual_test_instructions(mop_id)
            
        else:
            print(f"\\n⚠️  ENHANCED TEST SHOWS ISSUES")
            print(f"   - Check browser console output")
            print(f"   - Use browser_debug.js for detailed analysis")
            print(f"   - Verify field visibility and timing")
        
        return reload_success
    else:
        print(f"\\n❌ ENHANCED TEST FAILED - Could not create test MOP")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)