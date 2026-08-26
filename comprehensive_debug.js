
// =============================================================================
// COMPREHENSIVE DEBUG: Network Configuration & Implementation Steps
// Copy dan paste ke browser console untuk debug kedua masalah
// =============================================================================

console.log('🔧 Comprehensive Debug Script Starting...');
console.log('Testing both Network Configuration reload and Implementation Steps refresh');

// ============= NETWORK CONFIGURATION DEBUG =============

console.log('\n📋 SECTION 1: Network Configuration Debug');

function debugNetworkConfiguration() {
    console.log('\n🌐 Testing Network Configuration...');
    
    // Check network config container
    const networkContainer = document.getElementById('ipZoneAddresses');
    if (networkContainer) {
        console.log('✅ Network container found');
        
        const networkItems = networkContainer.querySelectorAll('.ip-zone-item');
        console.log(`📊 Network items: ${networkItems.length}`);
        
        // Check field structure in first item
        if (networkItems.length > 0) {
            const firstItem = networkItems[0];
            const fields = [
                'real_ip_address[]',
                'real_ip_subnet[]', 
                'nat_ip_address[]',
                'nat_ip_subnet[]',
                'real_zone_name[]',
                'vlan_id[]',
                'ip_description[]'
            ];
            
            console.log('\n🔍 Network field availability:');
            fields.forEach(fieldName => {
                const field = firstItem.querySelector(`[name="${fieldName}"]`);
                if (field) {
                    console.log(`   ✅ ${fieldName}: found, value="${field.value}"`);
                } else {
                    console.log(`   ❌ ${fieldName}: NOT found`);
                }
            });
        }
        
        // Check addIPZoneConfiguration function
        if (typeof addIPZoneConfiguration === 'function') {
            console.log('✅ addIPZoneConfiguration function available');
        } else {
            console.log('❌ addIPZoneConfiguration function not found');
        }
        
    } else {
        console.log('❌ Network container (ipZoneAddresses) not found');
    }
}

// ============= IMPLEMENTATION STEPS DEBUG =============

console.log('\n📋 SECTION 2: Implementation Steps Debug');

function debugImplementationSteps() {
    console.log('\n🔧 Testing Implementation Steps...');
    
    // Check current tab
    const implTab = document.querySelector('[data-bs-target="#implementation-section"]');
    const isOnImplTab = implTab && implTab.classList.contains('active');
    console.log(`📋 Implementation tab active: ${isOnImplTab}`);
    
    // Check device collection
    console.log('\n🔍 Testing device collection...');
    if (typeof collectDeviceData === 'function') {
        console.log('✅ collectDeviceData function available');
        
        const devices = collectDeviceData();
        console.log(`📊 Devices collected: ${devices.length}`);
        
        if (devices.length > 0) {
            devices.forEach((device, i) => {
                console.log(`   Device ${i+1}: ${device.hostname} (${device.type}) - ${device.mgmt_ip}`);
            });
        } else {
            console.log('⚠️  No devices collected - checking Technical Config tab...');
            
            // Switch to Technical Config to check devices
            const techTab = document.querySelector('[data-bs-target="#technical-section"]');
            if (techTab) {
                console.log('📋 Switching to Technical Config to check devices...');
                const tab = new bootstrap.Tab(techTab);
                tab.show();
                
                setTimeout(() => {
                    const devicesAfterSwitch = collectDeviceData();
                    console.log(`📊 Devices after tab switch: ${devicesAfterSwitch.length}`);
                    
                    // Switch back to Implementation
                    if (implTab) {
                        const implTabInstance = new bootstrap.Tab(implTab);
                        implTabInstance.show();
                    }
                }, 500);
            }
        }
    } else {
        console.log('❌ collectDeviceData function not found');
    }
    
    // Check generateDeviceImplementation function
    if (typeof generateDeviceImplementation === 'function') {
        console.log('✅ generateDeviceImplementation function available');
    } else {
        console.log('❌ generateDeviceImplementation function not found');
    }
    
    // Check implementation container
    const implContainer = document.getElementById('deviceImplementationContainer');
    if (implContainer) {
        console.log('✅ Implementation container found');
        const implSections = implContainer.querySelectorAll('.device-implementation');
        console.log(`📊 Current implementation sections: ${implSections.length}`);
    } else {
        console.log('❌ Implementation container not found');
    }
}

// ============= COMPREHENSIVE TEST =============

console.log('\n📋 SECTION 3: Comprehensive Test');

function runComprehensiveTest() {
    console.log('\n🧪 Running comprehensive test...');
    
    // Test 1: Check if we have test data
    console.log('\n1️⃣ Checking for test data...');
    
    // Check for MOPs with network configs
    fetch('/api/mop_detail/49')
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const networkConfigs = data.data.networkConfigs || [];
                const devices = data.data.devices || [];
                
                console.log(`📊 MOP 49 data:`);
                console.log(`   Network configs: ${networkConfigs.length}`);
                console.log(`   Devices: ${devices.length}`);
                
                if (networkConfigs.length > 0) {
                    console.log('\n2️⃣ Testing network config reload...');
                    
                    // Simulate loading network configs
                    console.log('🌐 Simulating network config loading...');
                    if (typeof loadDataIntoForm === 'function') {
                        loadDataIntoForm(data.data);
                        console.log('✅ loadDataIntoForm called with network data');
                    } else {
                        console.log('❌ loadDataIntoForm function not found');
                    }
                } else {
                    console.log('⚠️  MOP 49 has no network configs, trying MOP 33...');
                    
                    fetch('/api/mop_detail/33')
                        .then(r => r.json())
                        .then(data33 => {
                            if (data33.success && data33.data.networkConfigs.length > 0) {
                                console.log(`📊 MOP 33 has ${data33.data.networkConfigs.length} network configs`);
                                if (typeof loadDataIntoForm === 'function') {
                                    loadDataIntoForm(data33.data);
                                }
                            }
                        });
                }
                
                if (devices.length > 0) {
                    console.log('\n3️⃣ Testing implementation steps...');
                    
                    // Simulate device implementation generation
                    setTimeout(() => {
                        console.log('🔧 Testing implementation generation...');
                        if (typeof generateDeviceImplementation === 'function') {
                            generateDeviceImplementation();
                            console.log('✅ generateDeviceImplementation called');
                        } else {
                            console.log('❌ generateDeviceImplementation not available');
                        }
                    }, 2000);
                }
            } else {
                console.log('❌ Could not fetch MOP 49 data');
            }
        })
        .catch(err => {
            console.log('❌ API fetch error:', err);
        });
}

// ============= MANUAL TESTING HELPERS =============

console.log('\n📋 SECTION 4: Manual Testing Helpers');

function testNetworkConfigManually() {
    console.log('\n🧪 Manual Network Config Test');
    console.log('1. Go to History MOP tab');
    console.log('2. Find MOP with network configs (ID 33 or 49)');
    console.log('3. Click reload button');
    console.log('4. Check Technical Config tab > Network Configuration section');
    console.log('5. Look for populated IP fields');
}

function testImplementationManually() {
    console.log('\n🧪 Manual Implementation Steps Test');
    console.log('1. Ensure you have devices in Technical Config tab');
    console.log('2. Go to Implementation tab');
    console.log('3. Click "Refresh Device List" button');
    console.log('4. Look for generated implementation sections');
    console.log('5. Check console for device collection logs');
}

function quickDeviceCheck() {
    console.log('\n🔍 Quick device check:');
    const devices = collectDeviceData();
    console.log(`Found ${devices.length} devices:`, devices);
    return devices;
}

function quickNetworkCheck() {
    console.log('\n🔍 Quick network container check:');
    const container = document.getElementById('ipZoneAddresses');
    if (container) {
        const items = container.querySelectorAll('.ip-zone-item');
        console.log(`Network container has ${items.length} items`);
        return items.length;
    } else {
        console.log('Network container not found');
        return 0;
    }
}

// ============= AUTO EXECUTION =============

// Run initial checks
debugNetworkConfiguration();
debugImplementationSteps();

// Run comprehensive test after delay
setTimeout(() => {
    console.log('\n🔄 Running comprehensive test in 3 seconds...');
    runComprehensiveTest();
}, 3000);

// Export helper functions to window for manual use
window.testNetworkConfigManually = testNetworkConfigManually;
window.testImplementationManually = testImplementationManually;
window.quickDeviceCheck = quickDeviceCheck;
window.quickNetworkCheck = quickNetworkCheck;
window.debugNetworkConfiguration = debugNetworkConfiguration;
window.debugImplementationSteps = debugImplementationSteps;

console.log('\n💡 Manual testing functions available:');
console.log('  - testNetworkConfigManually()');
console.log('  - testImplementationManually()');
console.log('  - quickDeviceCheck()');
console.log('  - quickNetworkCheck()');
console.log('  - debugNetworkConfiguration()');
console.log('  - debugImplementationSteps()');

console.log('\n🎯 Comprehensive Debug Script Ready!');
