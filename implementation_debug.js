
// =============================================================================
// IMPLEMENTATION STEPS DEBUG: Refresh Device List Functionality
// Copy dan paste ke browser console untuk debug
// =============================================================================

console.log('🔧 Implementation Steps Debug Starting...');

// Test 1: Check Device Data Collection
console.log('\n📋 Test 1: Device Data Collection Check');

function testCollectDeviceData() {
    console.log('Testing collectDeviceData function...');
    
    // Check if collectDeviceData function exists
    if (typeof collectDeviceData === 'function') {
        console.log('✅ collectDeviceData function exists');
        
        try {
            const devices = collectDeviceData();
            console.log('✅ collectDeviceData executed successfully');
            console.log(`📊 Devices found: ${devices.length}`);
            
            if (devices.length > 0) {
                console.log('\n🔍 Device Details:');
                devices.forEach((device, index) => {
                    console.log(`   Device ${index + 1}:`);
                    console.log(`     Hostname: "${device.hostname}"`);
                    console.log(`     Type: "${device.type}"`);
                    console.log(`     Management IP: "${device.mgmt_ip}"`);
                });
            } else {
                console.log('⚠️  No devices collected - checking form fields...');
                
                // Check form fields
                const hostnames = document.querySelectorAll('[name="device_hostname[]"]');
                const types = document.querySelectorAll('[name="device_type[]"]');
                const ips = document.querySelectorAll('[name="device_mgmt_ip[]"]');
                
                console.log(`📋 Form fields found:`);
                console.log(`   Hostname fields: ${hostnames.length}`);
                console.log(`   Type fields: ${types.length}`);
                console.log(`   IP fields: ${ips.length}`);
                
                console.log('\n🔍 Field Values:');
                hostnames.forEach((field, index) => {
                    const typeField = types[index];
                    const ipField = ips[index];
                    
                    console.log(`   Field Set ${index + 1}:`);
                    console.log(`     Hostname: "${field.value}" (${field.value.trim() ? 'NOT EMPTY' : 'EMPTY'})`);
                    console.log(`     Type: "${typeField ? typeField.value : 'NO FIELD'}" `);
                    console.log(`     IP: "${ipField ? ipField.value : 'NO FIELD'}"`);
                });
            }
            
            return devices;
            
        } catch (error) {
            console.log('❌ collectDeviceData failed:', error);
            return [];
        }
    } else {
        console.log('❌ collectDeviceData function not found');
        return [];
    }
}

// Test 2: Check generateDeviceImplementation Function
console.log('\n🔄 Test 2: Generate Device Implementation Check');

function testGenerateDeviceImplementation() {
    console.log('Testing generateDeviceImplementation function...');
    
    if (typeof generateDeviceImplementation === 'function') {
        console.log('✅ generateDeviceImplementation function exists');
        
        try {
            console.log('🔄 Executing generateDeviceImplementation...');
            generateDeviceImplementation();
            console.log('✅ generateDeviceImplementation executed');
            
            // Check if implementation container was populated
            const container = document.getElementById('deviceImplementationContainer');
            if (container) {
                const deviceImplementations = container.querySelectorAll('.device-implementation');
                console.log(`📊 Device implementations generated: ${deviceImplementations.length}`);
                
                if (deviceImplementations.length > 0) {
                    console.log('\n🔍 Implementation Sections:');
                    deviceImplementations.forEach((impl, index) => {
                        const title = impl.querySelector('h6.text-primary');
                        const titleText = title ? title.textContent.trim() : 'No title';
                        console.log(`   Implementation ${index + 1}: ${titleText}`);
                    });
                } else {
                    console.log('⚠️  No implementation sections generated');
                    console.log('Container content:', container.innerHTML.substring(0, 200) + '...');
                }
            } else {
                console.log('❌ deviceImplementationContainer not found');
            }
            
        } catch (error) {
            console.log('❌ generateDeviceImplementation failed:', error);
        }
    } else {
        console.log('❌ generateDeviceImplementation function not found');
    }
}

// Test 3: Check Technical Config Tab Device Fields
console.log('\n📱 Test 3: Technical Config Device Fields Check');

function checkTechnicalConfigDevices() {
    console.log('Checking device fields in Technical Config tab...');
    
    // Check if we're on Technical Config tab
    const techConfigTab = document.querySelector('[data-bs-target="#technical-section"]');
    const isActive = techConfigTab ? techConfigTab.classList.contains('active') : false;
    
    console.log(`Technical Config tab active: ${isActive}`);
    
    // Find device inventory container
    const deviceInventory = document.getElementById('deviceInventory');
    if (deviceInventory) {
        console.log('✅ Device inventory container found');
        
        const deviceItems = deviceInventory.querySelectorAll('.device-item');
        console.log(`📊 Device items found: ${deviceItems.length}`);
        
        deviceItems.forEach((item, index) => {
            const hostname = item.querySelector('[name="device_hostname[]"]');
            const type = item.querySelector('[name="device_type[]"]');
            const ip = item.querySelector('[name="device_mgmt_ip[]"]');
            
            console.log(`\n   Device Item ${index + 1}:`);
            console.log(`     Hostname: "${hostname ? hostname.value : 'NO FIELD'}"`);
            console.log(`     Type: "${type ? type.value : 'NO FIELD'}"`);
            console.log(`     IP: "${ip ? ip.value : 'NO FIELD'}"`);
            console.log(`     Visibility: ${item.offsetParent !== null ? 'VISIBLE' : 'HIDDEN'}`);
        });
    } else {
        console.log('❌ Device inventory container not found');
    }
}

// Test 4: Manual Implementation Generation
console.log('\n🧪 Test 4: Manual Implementation Generation');

function manualImplementationTest() {
    console.log('Manual implementation generation test...');
    
    // Switch to Technical Config tab first
    const techTab = document.querySelector('[data-bs-target="#technical-section"]');
    if (techTab && !techTab.classList.contains('active')) {
        console.log('📋 Switching to Technical Config tab...');
        const tab = new bootstrap.Tab(techTab);
        tab.show();
        
        // Wait a bit then switch to Implementation
        setTimeout(() => {
            const implTab = document.querySelector('[data-bs-target="#implementation-section"]');
            if (implTab) {
                console.log('📋 Switching to Implementation tab...');
                const implTabInstance = new bootstrap.Tab(implTab);
                implTabInstance.show();
                
                // Wait a bit then run generation
                setTimeout(() => {
                    console.log('🔄 Running device implementation generation...');
                    testGenerateDeviceImplementation();
                }, 500);
            }
        }, 500);
    } else {
        // Already on tech config, switch to implementation
        const implTab = document.querySelector('[data-bs-target="#implementation-section"]');
        if (implTab) {
            console.log('📋 Switching to Implementation tab...');
            const implTabInstance = new bootstrap.Tab(implTab);
            implTabInstance.show();
            
            setTimeout(() => {
                console.log('🔄 Running device implementation generation...');
                testGenerateDeviceImplementation();
            }, 500);
        }
    }
}

// Run all tests
console.log('\n🏃 Running all tests...');

// 1. Test device data collection
const devices = testCollectDeviceData();

// 2. Check technical config devices
checkTechnicalConfigDevices();

// 3. Test implementation generation
testGenerateDeviceImplementation();

// 4. Instructions
console.log('\n💡 Manual Test Instructions:');
console.log('1. Go to Technical Config tab');
console.log('2. Verify devices are populated in Device Inventory section');
console.log('3. Go to Implementation tab');
console.log('4. Click "Refresh Device List" button');
console.log('5. Check if Implementation Steps are generated');

console.log('\n🔧 If devices not showing:');
console.log('1. Go to History MOP tab');
console.log('2. Click reload on a MOP with devices (e.g., MOP ID 46)');
console.log('3. Wait for auto-switch to Technical Config');
console.log('4. Verify devices populated');
console.log('5. Then go to Implementation tab and click Refresh Device List');

// Auto-test with delay
setTimeout(() => {
    console.log('\n🔄 Running automated test sequence...');
    manualImplementationTest();
}, 2000);
