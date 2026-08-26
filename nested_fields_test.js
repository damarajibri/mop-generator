
// =============================================================================  
// NESTED FIELDS TEST: Implementation Steps Structure Verification
// Copy dan paste ke browser console untuk test
// =============================================================================

console.log('🔧 Nested Fields Test Starting...');

// Test 1: Check for nested device-implementation divs
console.log('\n📋 Test 1: Nested Structure Check');

function checkForNestedImplementations() {
    // First check if any implementation sections exist
    const implementations = document.querySelectorAll('.device-implementation');
    console.log(`Found ${implementations.length} device implementation sections`);
    
    if (implementations.length === 0) {
        console.log('⚪ No implementation sections found - run Refresh Device List first');
        return false;
    }
    
    let nestingFound = false;
    let structureIssues = [];
    
    implementations.forEach((impl, index) => {
        // Check for nested device-implementation divs within this implementation
        const nestedImpls = impl.querySelectorAll('.device-implementation');
        
        if (nestedImpls.length > 0) {
            nestingFound = true;
            structureIssues.push(`Implementation ${index + 1} has ${nestedImpls.length} nested implementation(s)`);
        }
        
        // Check for proper section structure
        const sections = {
            'Pre-Implementation': impl.querySelectorAll('h6:contains("Pre-Implementation")').length,
            'Implementation': impl.querySelectorAll('h6:contains("Implementation Commands")').length,
            'Verification': impl.querySelectorAll('h6:contains("Verification")').length,
            'Rollback': impl.querySelectorAll('h6:contains("Rollback")').length
        };
        
        console.log(`\n   Implementation ${index + 1} sections:`);
        for (const [name, count] of Object.entries(sections)) {
            if (count === 1) {
                console.log(`     ✅ ${name}: ${count} section`);
            } else if (count > 1) {
                console.log(`     ⚠️  ${name}: ${count} sections (duplicate)`);
                structureIssues.push(`Implementation ${index + 1} has duplicate ${name} sections`);
            } else {
                console.log(`     ❌ ${name}: Missing`);
                structureIssues.push(`Implementation ${index + 1} missing ${name} section`);
            }
        }
    });
    
    console.log(`\n📊 Structure Analysis Results:`);
    console.log(`   Nested implementation divs: ${nestingFound ? 'FOUND (BAD)' : 'NONE (GOOD)'}`);
    console.log(`   Structure issues: ${structureIssues.length}`);
    
    if (structureIssues.length > 0) {
        console.log('\n⚠️  Structure Issues Detected:');
        structureIssues.forEach(issue => console.log(`   - ${issue}`));
    }
    
    return !nestingFound && structureIssues.length === 0;
}

// Test 2: Check editor initialization
console.log('\n🔄 Test 2: Editor Initialization Check');

function checkEditorStructure() {
    const implementations = document.querySelectorAll('.device-implementation');
    let editorIssues = [];
    
    implementations.forEach((impl, index) => {
        const editorTypes = ['preEditor', 'implEditor', 'verifyEditor', 'rollbackEditor'];
        
        editorTypes.forEach(type => {
            const editorId = `${type}_${index}`;
            const editor = document.getElementById(editorId);
            
            if (editor) {
                console.log(`     ✅ ${editorId}: Found`);
            } else {
                console.log(`     ❌ ${editorId}: Missing`);
                editorIssues.push(`Missing editor: ${editorId}`);
            }
        });
    });
    
    console.log(`\n📊 Editor Check: ${editorIssues.length} issues found`);
    return editorIssues.length === 0;
}

// Test 3: Manual structure trigger
console.log('\n🚀 Test 3: Manual Structure Test');

function runCompleteStructureTest() {
    console.log('Running complete structure test...');
    
    // Switch to Implementation tab first
    const implTab = document.querySelector('[data-bs-target="#implementation-section"]');
    if (implTab && !implTab.classList.contains('active')) {
        console.log('📋 Switching to Implementation tab...');
        const tab = new bootstrap.Tab(implTab);
        tab.show();
    }
    
    setTimeout(() => {
        console.log('🔄 Running Refresh Device List...');
        
        // Trigger device implementation generation
        if (typeof generateDeviceImplementation === 'function') {
            generateDeviceImplementation();
            
            setTimeout(() => {
                console.log('\n📊 Final Structure Check:');
                const structureOK = checkForNestedImplementations();
                const editorsOK = checkEditorStructure();
                
                console.log(`\n🎯 NESTED FIELDS TEST RESULTS:`);
                console.log(`   Structure: ${structureOK ? 'PASS' : 'FAIL'}`);
                console.log(`   Editors: ${editorsOK ? 'PASS' : 'FAIL'}`);
                console.log(`   Overall: ${structureOK && editorsOK ? 'SUCCESS' : 'NEEDS ATTENTION'}`);
                
            }, 1000);
        } else {
            console.log('❌ generateDeviceImplementation function not found');
        }
    }, 500);
}

// Auto-run tests
const structureResult = checkForNestedImplementations();
const editorResult = checkEditorStructure();

console.log('\n💡 Manual Instructions:');
console.log('1. Ensure you have devices loaded (go to Technical Config, check Device Inventory)');
console.log('2. Go to Implementation tab');
console.log('3. Click "Refresh Device List"');
console.log('4. Check console output for structure analysis');
console.log('5. Look for any nested <div class="device-implementation"> elements');

console.log('\n🔧 To run complete test:');
console.log('runCompleteStructureTest();');

// Auto-run complete test after delay
setTimeout(() => {
    console.log('\n🔄 Running automated complete test...');
    runCompleteStructureTest();
}, 3000);
