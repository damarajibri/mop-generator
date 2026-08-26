#!/usr/bin/env python3
"""
Debug Script: Generate Browser JavaScript Test Code
Generate kode JavaScript untuk test manual di browser console
"""

def generate_browser_debug_code():
    """Generate JavaScript code untuk debug form loading di browser"""
    
    # Technical Config fields yang sering bermasalah
    tech_config_fields = {
        'hardware_requirements': 'Hardware Requirements',
        'software_dependencies': 'Software Dependencies', 
        'network_prerequisites': 'Network Prerequisites',
        'security_requirements': 'Security Requirements',
        'personnel_requirements': 'Personnel Requirements',
        'external_dependencies': 'External Dependencies',
        
        'prep_start_time': 'Prep Start Time',
        'prep_phase_duration': 'Prep Phase Duration',
        'prep_activities': 'Prep Activities',
        'impl_start_time': 'Implementation Start Time',
        'impl_phase_duration': 'Implementation Phase Duration', 
        'impl_activities': 'Implementation Activities',
        'verification_start_time': 'Verification Start Time',
        'verification_duration': 'Verification Duration',
        'verification_activities': 'Verification Activities',
        
        'communication_frequency': 'Communication Frequency',
        'notification_list': 'Notification List',
        'technical_success_criteria': 'Technical Success Criteria',
        'business_success_criteria': 'Business Success Criteria',
        
        'rollback_commands': 'Rollback Commands',
        'recovery_time_objective': 'Recovery Time Objective'
    }
    
    js_code = f"""
// =============================================================================
// MOP GENERATOR: Technical Config Debug Script
// Copy dan paste ke browser console untuk debug form loading
// =============================================================================

console.log('🔧 MOP Technical Config Debug Script Starting...');

// Test 1: Check if form fields exist in DOM
console.log('\\n📋 Test 1: Form Field Existence Check');
const techFields = {tech_config_fields};

let fieldsFound = 0;
let fieldsMissing = [];

for (const [fieldId, fieldName] of Object.entries(techFields)) {{
    const element = document.getElementById(fieldId);
    if (element) {{
        console.log(`✅ Found: ${{fieldId}} (${{fieldName}})`);
        fieldsFound++;
    }} else {{
        console.log(`❌ Missing: ${{fieldId}} (${{fieldName}})`);
        fieldsMissing.push(fieldId);
    }}
}}

console.log(`\\n📊 Field Existence: ${{fieldsFound}}/${{Object.keys(techFields).length}} found`);
if (fieldsMissing.length > 0) {{
    console.log('❌ Missing fields:', fieldsMissing);
}}

// Test 2: Fetch MOP data from API
console.log('\\n🌐 Test 2: API Data Fetch');
async function testAPIData() {{
    try {{
        const response = await fetch('/api/mop_detail/42');
        const data = await response.json();
        
        if (data.success) {{
            console.log('✅ API Response OK, got', Object.keys(data.data).length, 'fields');
            
            // Check Technical Config data availability
            let dataAvailable = 0;
            console.log('\\n📊 Technical Config Data Check:');
            
            for (const [fieldId, fieldName] of Object.entries(techFields)) {{
                const value = data.data[fieldId];
                if (value && String(value).trim() && value !== 'None') {{
                    console.log(`✅ ${{fieldId}}: "${{String(value).substring(0, 40)}}..."`);
                    dataAvailable++;
                }} else {{
                    console.log(`⚪ ${{fieldId}}: EMPTY (value: ${{JSON.stringify(value)}})`);
                }}
            }}
            
            console.log(`\\n📊 Data Coverage: ${{dataAvailable}}/${{Object.keys(techFields).length}} fields have data`);
            
            // Test 3: Manual Form Loading
            console.log('\\n📝 Test 3: Manual Form Loading');
            
            let fieldsLoaded = 0;
            let loadErrors = [];
            
            for (const [fieldId, fieldName] of Object.entries(techFields)) {{
                const element = document.getElementById(fieldId);
                const value = data.data[fieldId];
                
                if (element && value && String(value).trim() && value !== 'None') {{
                    try {{
                        element.value = value;
                        console.log(`✅ Loaded ${{fieldId}}: "${{String(value).substring(0, 30)}}..."`);
                        fieldsLoaded++;
                    }} catch (error) {{
                        console.log(`❌ Failed to load ${{fieldId}}:`, error);
                        loadErrors.push({{field: fieldId, error: error.message}});
                    }}
                }} else if (!element) {{
                    console.log(`⚠️  No element for ${{fieldId}}`);
                }} else {{
                    console.log(`🔸 No data for ${{fieldId}} (value: ${{JSON.stringify(value)}})`);
                }}
            }}
            
            console.log(`\\n📊 Loading Results: ${{fieldsLoaded}}/${{Object.keys(techFields).length}} fields loaded successfully`);
            
            if (loadErrors.length > 0) {{
                console.log('❌ Loading errors:', loadErrors);
            }}
            
            // Test 4: Check Current Tab
            console.log('\\n📑 Test 4: Current Tab Check');
            const activeTab = document.querySelector('.nav-link.active');
            const currentTabText = activeTab ? activeTab.textContent.trim() : 'Unknown';
            console.log(`Current active tab: "${{currentTabText}}"`);
            
            // Switch to Technical Config tab if not already there
            const techConfigTab = document.querySelector('[data-bs-target="#technical-config-section"]');
            if (techConfigTab && !techConfigTab.classList.contains('active')) {{
                console.log('📋 Switching to Technical Config tab...');
                const tab = new bootstrap.Tab(techConfigTab);
                tab.show();
                console.log('✅ Tab switched');
            }}
            
            return data.data;
            
        }} else {{
            console.log('❌ API Error:', data.message);
            return null;
        }}
    }} catch (error) {{
        console.log('❌ Fetch Error:', error);
        return null;
    }}
}}

// Test 5: Test existing loadDataIntoForm function
console.log('\\n🔄 Test 5: Existing Function Test');
console.log('Testing if loadDataIntoForm function exists...');
if (typeof loadDataIntoForm === 'function') {{
    console.log('✅ loadDataIntoForm function exists');
    
    testAPIData().then(mopData => {{
        if (mopData) {{
            console.log('\\n🧪 Testing loadDataIntoForm with API data...');
            try {{
                loadDataIntoForm(mopData);
                console.log('✅ loadDataIntoForm executed successfully');
            }} catch (error) {{
                console.log('❌ loadDataIntoForm failed:', error);
            }}
        }}
    }});
}} else {{
    console.log('❌ loadDataIntoForm function not found');
    console.log('Available functions:', Object.getOwnPropertyNames(window).filter(name => typeof window[name] === 'function'));
}}

// Run API test
testAPIData();

console.log('\\n🎯 Debug script completed. Check results above.');
console.log('\\n💡 Instructions:');
console.log('1. If fields are missing: Check HTML structure');
console.log('2. If API data is empty: Check backend save function');
console.log('3. If loading fails: Check field IDs and JavaScript function');
console.log('4. If tab is wrong: Check tab switching logic');

// Auto-run comprehensive test
setTimeout(() => {{
    console.log('\\n🔄 Running comprehensive reload test...');
    if (typeof reloadMOPData === 'function') {{
        reloadMOPData(42);
    }} else {{
        console.log('❌ reloadMOPData function not found');
    }}
}}, 2000);
"""
    
    print("🎯 BROWSER DEBUG CODE GENERATED")
    print("=" * 80)
    print("Copy kode JavaScript di bawah ini ke browser console:")
    print("=" * 80)
    print(js_code)
    print("=" * 80)
    print("\n📋 Manual Testing Steps:")
    print("1. Buka aplikasi di browser")
    print("2. Buka Developer Tools (F12)")
    print("3. Go to Console tab")
    print("4. Copy paste kode JavaScript di atas")
    print("5. Press Enter untuk menjalankan")
    print("6. Periksa hasil output untuk menemukan masalah")
    
    # Save to file juga
    with open('browser_debug.js', 'w') as f:
        f.write(js_code)
    
    print(f"\n💾 Kode juga disimpan ke: browser_debug.js")

if __name__ == "__main__":
    generate_browser_debug_code()