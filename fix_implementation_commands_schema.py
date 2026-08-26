#!/usr/bin/env python3
"""
Fix Implementation Commands Schema
Menambahkan field yang hilang untuk Implementation Steps & Commands
"""

import os
import sqlite3
from database import MOPDatabase

def add_missing_fields():
    """Add missing implementation commands fields to mop_documents table"""
    
    # Load environment
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass
    
    db = MOPDatabase()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor() if hasattr(conn, 'cursor') else conn
        
        print("🔧 Adding missing Implementation Commands fields...")
        
        # Field yang perlu ditambahkan
        missing_fields = [
            ('general_implementation_commands', 'TEXT'),
            ('general_implementation_commands_html', 'TEXT'),
            ('pre_implementation_commands', 'TEXT'),
            ('pre_implementation_commands_html', 'TEXT'),
            ('implementation_commands', 'TEXT'),
            ('implementation_commands_html', 'TEXT'),
            ('verification_commands', 'TEXT'),
            ('verification_commands_html', 'TEXT')
        ]
        
        # Check existing columns
        if db.config.is_sqlite:
            cursor.execute('PRAGMA table_info(mop_documents)')
            existing_columns = [row[1] for row in cursor.fetchall()]
        else:
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'mop_documents'
            """)
            existing_columns = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Existing columns: {len(existing_columns)}")
        
        # Add missing fields
        added_count = 0
        for field_name, field_type in missing_fields:
            if field_name not in existing_columns:
                try:
                    alter_query = f"ALTER TABLE mop_documents ADD COLUMN {field_name} {field_type}"
                    cursor.execute(alter_query)
                    print(f"   ✅ Added: {field_name} ({field_type})")
                    added_count += 1
                except Exception as e:
                    print(f"   ❌ Failed to add {field_name}: {e}")
            else:
                print(f"   🔸 Already exists: {field_name}")
        
        # Commit changes
        conn.commit()
        print(f"\n✅ Schema update complete! Added {added_count} new fields.")
        
        # Verify new schema
        if db.config.is_sqlite:
            cursor.execute('PRAGMA table_info(mop_documents)')
            all_columns = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT column_name, data_type FROM information_schema.columns 
                WHERE table_name = 'mop_documents' ORDER BY ordinal_position
            """)
            all_columns = cursor.fetchall()
        
        print(f"\n📋 Updated schema - Total columns: {len(all_columns)}")
        
        # Show command-related fields
        command_fields = [col for col in all_columns if 'command' in col[1].lower()]
        if command_fields:
            print("\n🔧 Command-related fields:")
            for col in command_fields:
                print(f"   {col[1]} ({col[2] if len(col) > 2 else 'TEXT'})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def test_new_fields():
    """Test that new fields can be written and read"""
    
    print("\n🧪 Testing new fields...")
    
    db = MOPDatabase()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor() if hasattr(conn, 'cursor') else conn
        
        # Test data
        test_data = {
            'general_implementation_commands': '# Test general implementation\necho "Starting implementation"',
            'general_implementation_commands_html': '<div class="code-block"># Test general implementation<br>echo "Starting implementation"</div>',
            'pre_implementation_commands': '# Test pre-implementation\nshow version',
            'pre_implementation_commands_html': '<div class="code-block"># Test pre-implementation<br>show version</div>',
            'implementation_commands': '# Test implementation\nconfigure terminal',
            'implementation_commands_html': '<div class="code-block"># Test implementation<br>configure terminal</div>',
            'verification_commands': '# Test verification\nshow running-config',
            'verification_commands_html': '<div class="code-block"># Test verification<br>show running-config</div>'
        }
        
        # Create a test MOP
        insert_query = """
            INSERT INTO mop_documents (
                document_title, version, activity_name,
                general_implementation_commands, general_implementation_commands_html,
                pre_implementation_commands, pre_implementation_commands_html,
                implementation_commands, implementation_commands_html,
                verification_commands, verification_commands_html,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """
        
        cursor.execute(insert_query, (
            'TEST Implementation Commands',
            'v1.0',
            'Test Implementation Commands Schema',
            test_data['general_implementation_commands'],
            test_data['general_implementation_commands_html'],
            test_data['pre_implementation_commands'],
            test_data['pre_implementation_commands_html'],
            test_data['implementation_commands'],
            test_data['implementation_commands_html'],
            test_data['verification_commands'],
            test_data['verification_commands_html']
        ))
        
        # Get the test MOP ID
        test_mop_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ Test MOP created with ID: {test_mop_id}")
        
        # Read back the data
        select_query = """
            SELECT general_implementation_commands, pre_implementation_commands,
                   implementation_commands, verification_commands
            FROM mop_documents WHERE id = ?
        """
        
        cursor.execute(select_query, (test_mop_id,))
        row = cursor.fetchone()
        
        if row:
            print("✅ Successfully read test data:")
            print(f"   General Implementation: {row[0][:50]}...")
            print(f"   Pre-Implementation: {row[1][:50]}...")
            print(f"   Implementation: {row[2][:50]}...")
            print(f"   Verification: {row[3][:50]}...")
        
        # Clean up test data
        cursor.execute("DELETE FROM mop_documents WHERE id = ?", (test_mop_id,))
        conn.commit()
        print("🗑️  Test data cleaned up")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 IMPLEMENTATION COMMANDS SCHEMA FIX")
    print("="*50)
    
    if add_missing_fields():
        if test_new_fields():
            print("\n🎉 Schema fix completed successfully!")
            print("✅ All Implementation Commands fields are now available")
        else:
            print("\n⚠️  Schema updated but testing failed")
    else:
        print("\n❌ Schema update failed")