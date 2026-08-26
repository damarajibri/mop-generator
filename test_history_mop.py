#!/usr/bin/env python3
"""
Test script for History MOP functionality
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

def test_history_mop():
    """Test History MOP functionality"""
    print("🧪 Testing History MOP Functionality")
    print("=" * 50)
    
    # Load environment
    load_env()
    
    try:
        # Import app
        from app import app, DATABASE_AVAILABLE, db
        print("✅ App imported successfully")
        
        # Check database status
        if DATABASE_AVAILABLE and db and db.config.use_database:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mop_documents")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            print(f"📊 Database: {count} MOP documents available")
        else:
            import glob
            json_files = glob.glob('generated_mops/*.json')
            print(f"📁 File fallback: {len(json_files)} JSON files available")
        
        # Test with Flask test client
        with app.test_client() as client:
            print("\n🔍 Testing API Endpoints:")
            
            # Test 1: History API
            print("   1. Testing /api/mop_history...")
            response = client.get('/api/mop_history?page=1&page_size=3')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"      ✅ Status: {response.status_code}")
                print(f"      ✅ Success: {data['success']}")
                print(f"      ✅ Items: {len(data['data'])}")
                print(f"      ✅ Total: {data['pagination']['total_count']}")
                
                # Test 2: Detail API
                if data['data']:
                    test_id = data['data'][0]['id']
                    print(f"\n   2. Testing /api/mop_detail/{test_id}...")
                    
                    detail_response = client.get(f'/api/mop_detail/{test_id}')
                    
                    if detail_response.status_code == 200:
                        detail_data = detail_response.get_json()
                        print(f"      ✅ Status: {detail_response.status_code}")
                        print(f"      ✅ Success: {detail_data['success']}")
                        
                        if detail_data['success']:
                            mop_data = detail_data['data']
                            print(f"      ✅ Title: {mop_data.get('document_title', 'N/A')}")
                            print(f"      ✅ Version: {mop_data.get('version', 'N/A')}")
                            print(f"      ✅ Devices: {len(mop_data.get('devices', []))}")
                            print(f"      ✅ Networks: {len(mop_data.get('networkConfigs', []))}")
                            print(f"      ✅ Risks: {len(mop_data.get('risks', []))}")
                        else:
                            print(f"      ❌ Detail error: {detail_data.get('message', 'Unknown')}")
                    else:
                        print(f"      ❌ Detail API failed: {detail_response.status_code}")
                        try:
                            error_data = detail_response.get_json()
                            print(f"      ❌ Error: {error_data.get('message', 'Unknown error')}")
                        except:
                            print(f"      ❌ Response: {detail_response.data}")
                else:
                    print("   2. No data available for detail test")
                    
            else:
                print(f"      ❌ History API failed: {response.status_code}")
                try:
                    error_data = response.get_json()
                    print(f"      ❌ Error: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"      ❌ Response: {response.data}")
        
        print("\n🎉 All tests completed!")
        print("\n💡 To start the application:")
        print("   python3 app.py")
        print("\n🌐 Then access: http://localhost:8080")
        print("   Click 'History MOP' tab to test the new feature")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_history_mop()
    sys.exit(0 if success else 1)