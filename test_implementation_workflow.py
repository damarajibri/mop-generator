#!/usr/bin/env python3
"""
Test Script: Implementation Steps Generation Simulation
Simulasi workflow dari device data sampai implementation generation
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

def test_device_to_implementation_workflow():
    """Test complete workflow dari device data ke implementation steps"""
    print("🔄 Testing Device to Implementation Workflow...")
    
    load_env()
    
    try:
        from app import app
        
        # Test dengan MOP ID 46 yang punya devices
        test_mop_id = 46
        
        with app.test_client() as client:
            print(f"📡 Getting device data for MOP ID {test_mop_id}...")
            
            response = client.get(f'/api/mop_detail/{test_mop_id}')
            
            if response.status_code == 200:
                data = response.get_json()
                
                if data.get('success'):
                    mop_data = data['data']
                    devices = mop_data.get('devices', [])
                    
                    print(f"✅ Found {len(devices)} devices in MOP data")
                    
                    if devices:
                        print(f"\\n🔍 Device Details for Implementation Generation:")
                        
                        # Simulate collectDeviceData() functionality
                        simulated_collect_result = []
                        
                        for i, device in enumerate(devices):
                            device_data = {
                                'hostname': device.get('hostname') or device.get('name', f'Device {i+1}'),
                                'type': device.get('type', ''),
                                'mgmt_ip': device.get('mgmt_ip') or device.get('ip', '')
                            }
                            
                            simulated_collect_result.append(device_data)
                            
                            print(f"   Device {i+1}:")
                            print(f"     Hostname: '{device_data['hostname']}'")
                            print(f"     Type: '{device_data['type']}'") 
                            print(f"     Management IP: '{device_data['mgmt_ip']}'")
                            
                            # Check if device data is sufficient for implementation generation
                            has_hostname = bool(device_data['hostname'].strip())
                            has_type = bool(device_data['type'].strip())
                            has_ip = bool(device_data['mgmt_ip'].strip())
                            
                            completeness = (has_hostname + has_type + has_ip) / 3 * 100
                            
                            print(f"     Data Completeness: {completeness:.1f}%")
                            print(f"     Ready for Implementation: {'YES' if completeness >= 67 else 'NO'}")
                        
                        print(f"\\n📊 Simulation Results:")
                        print(f"   Total devices: {len(simulated_collect_result)}")
                        
                        ready_devices = [d for d in simulated_collect_result if d['hostname'].strip()]
                        print(f"   Devices with hostname: {len(ready_devices)}")
                        
                        if ready_devices:
                            print(f"\\n🔧 Implementation Generation Simulation:")
                            
                            for device in ready_devices:
                                device_type = device['type'] or 'Device'
                                device_name = device['hostname']
                                is_palo_alto = device['type'] in ['palo_alto', 'firewall']
                                
                                print(f"\\n   Implementation for {device_type.upper()}: {device_name}")
                                print(f"     IP: {device['mgmt_ip'] or 'No IP'}")
                                print(f"     Type-specific templates: {'Palo Alto' if is_palo_alto else 'Generic'}")
                                
                                # Simulate template content
                                if device['type'] == 'router':
                                    print(f"     Pre-Implementation: show version, show running-config")
                                    print(f"     Implementation: configure terminal, interface config")
                                    print(f"     Verification: show interfaces, show ip route")
                                    print(f"     Rollback: rollback configuration")
                                elif device['type'] == 'switch':
                                    print(f"     Pre-Implementation: show version, show vlan")
                                    print(f"     Implementation: configure vlan, interface config") 
                                    print(f"     Verification: show vlan, show spanning-tree")
                                    print(f"     Rollback: no vlan, default interface")
                                elif device['type'] == 'firewall':
                                    print(f"     Pre-Implementation: show system info, show config")
                                    print(f"     Implementation: configure security policy")
                                    print(f"     Verification: show session, show policy")
                                    print(f"     Rollback: delete security policy")
                                else:
                                    print(f"     Pre-Implementation: Generic pre-check commands")
                                    print(f"     Implementation: Generic configuration commands")
                                    print(f"     Verification: Generic verification commands")
                                    print(f"     Rollback: Generic rollback commands")
                            
                            print(f"\\n✅ Implementation generation would be SUCCESSFUL")
                            return True
                        else:
                            print(f"\\n❌ No devices ready for implementation (no hostnames)")
                            return False
                    else:
                        print(f"\\n⚪ No devices found in MOP data - would show warning message")
                        return False
                else:
                    print(f"❌ API failed: {data}")
                    return False
            else:
                print(f"❌ API error: {response.status_code}")
                return False
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def analyze_potential_issues():
    """Analyze potential issues in the implementation workflow"""
    print(f"\\n🔍 POTENTIAL ISSUES ANALYSIS:")
    print("=" * 60)
    
    issues = [
        {
            'issue': 'Device form fields empty after reload',
            'cause': 'Device loading in loadDataIntoForm has timing issues',
            'solution': 'Add delay before collectDeviceData or check field visibility'
        },
        {
            'issue': 'collectDeviceData returns empty array',
            'cause': 'Device fields not populated when Refresh Device List clicked',
            'solution': 'Ensure device reload completes before implementation generation'
        },
        {
            'issue': 'Tab switching timing issues',
            'cause': 'User clicks Refresh Device List before devices are loaded',
            'solution': 'Add loading state or auto-refresh after device reload'
        },
        {
            'issue': 'Form field selectors not finding elements',
            'cause': 'DOM elements not ready or tab not active',
            'solution': 'Add element existence checks and tab visibility checks'
        }
    ]
    
    for i, issue in enumerate(issues, 1):
        print(f"\\n{i}. {issue['issue']}:")
        print(f"   Cause: {issue['cause']}")
        print(f"   Solution: {issue['solution']}")
    
    print(f"\\n💡 RECOMMENDED FIXES:")
    print(f"1. Add auto-refresh after device reload completes")
    print(f"2. Add device field validation before implementation generation")
    print(f"3. Improve timing coordination between tabs")
    print(f"4. Add visual feedback for device loading state")

def generate_fix_recommendations():
    """Generate specific fix recommendations"""
    print(f"\\n🔧 SPECIFIC FIX RECOMMENDATIONS:")
    print("=" * 60)
    
    fixes = [
        {
            'component': 'Device Loading (loadDataIntoForm)',
            'fix': 'Add callback after device population completes',
            'code': '''
// After device population in loadDataIntoForm
setTimeout(() => {
    // Trigger implementation refresh if on Implementation tab
    const implTab = document.querySelector('[data-bs-target="#implementation-section"]');
    if (implTab && implTab.classList.contains('active')) {
        generateDeviceImplementation();
    }
}, 1500);
'''
        },
        {
            'component': 'collectDeviceData Function',
            'fix': 'Add field validation and retry mechanism',
            'code': '''
function collectDeviceDataWithRetry(retryCount = 0) {
    const devices = collectDeviceData();
    
    if (devices.length === 0 && retryCount < 3) {
        console.log('No devices found, retrying in 300ms...');
        setTimeout(() => collectDeviceDataWithRetry(retryCount + 1), 300);
        return [];
    }
    
    return devices;
}
'''
        },
        {
            'component': 'Refresh Device List Button',
            'fix': 'Add loading state and validation',
            'code': '''
function generateDeviceImplementationWithValidation() {
    const btn = event.target;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    
    setTimeout(() => {
        const devices = collectDeviceData();
        
        if (devices.length === 0) {
            // Show helper message
            showNotification('No devices found. Please ensure devices are loaded in Technical Config tab.', 'warning');
        }
        
        generateDeviceImplementation();
        
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-sync"></i> Refresh Device List';
    }, 500);
}
'''
        }
    ]
    
    for fix in fixes:
        print(f"\\n{fix['component']}:")
        print(f"   Fix: {fix['fix']}")
        print(f"   Code: {fix['code']}")

def main():
    """Main test function"""
    print("🎯 IMPLEMENTATION STEPS & COMMANDS DEBUG")
    print("=" * 80)
    
    # Test device to implementation workflow
    workflow_success = test_device_to_implementation_workflow()
    
    # Analyze potential issues
    analyze_potential_issues()
    
    # Generate fix recommendations
    generate_fix_recommendations()
    
    print(f"\\n🎯 ANALYSIS RESULTS:")
    print("=" * 40)
    print(f"✅ Device Data Available: {'YES' if workflow_success else 'NO'}")
    print(f"✅ Implementation Generation: {'WOULD WORK' if workflow_success else 'NEEDS FIXING'}")
    
    if workflow_success:
        print(f"\\n🎉 DEVICE DATA IS READY!")
        print(f"\\nIssue is likely in JavaScript timing or form field access.")
        print(f"\\n📋 Next Steps:")
        print(f"1. Use browser debug script to check real-time field values")
        print(f"2. Verify timing between device reload and implementation generation")
        print(f"3. Check if user is on correct tab when clicking Refresh Device List")
        print(f"4. Implement recommended fixes for timing and validation")
    else:
        print(f"\\n⚠️  DEVICE DATA ISSUES DETECTED")
        print(f"\\nNeed to fix device data availability first.")
        print(f"\\n📋 Next Steps:")
        print(f"1. Test with MOP that has devices (MOP ID 46)")
        print(f"2. Verify device reload works in Technical Config tab")
        print(f"3. Check device save mechanism")
    
    return workflow_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)