#!/usr/bin/env python3
"""
Migration script to import existing MOP documents from JSON files to database
"""

import os
import json
import glob
from datetime import datetime

def load_env_file():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

def migrate_existing_mops():
    """Migrate existing MOP JSON files to database"""
    print("📦 Starting migration of existing MOP documents...")
    
    # Load environment
    load_env_file()
    
    # Import database after setting environment
    from database import MOPDatabase
    
    db = MOPDatabase()
    
    if not db.config.use_database:
        print("❌ Database not configured. Please run setup_local_database.py first")
        return False
    
    # Find all JSON files in generated_mops directory
    json_files = glob.glob('generated_mops/*.json')
    
    if not json_files:
        print("ℹ️  No existing MOP JSON files found to migrate")
        return True
    
    print(f"📁 Found {len(json_files)} JSON files to migrate")
    
    migrated_count = 0
    failed_count = 0
    
    for json_file in sorted(json_files):
        try:
            print(f"📄 Processing: {os.path.basename(json_file)}")
            
            # Load JSON data
            with open(json_file, 'r', encoding='utf-8') as f:
                mop_data = json.load(f)
            
            # Map old field names to new format
            title = mop_data.get('document_title') or mop_data.get('title', '')
            
            # Skip if no title (invalid MOP)
            if not title:
                print(f"   ⚠️  Skipped - no title found")
                continue
            
            # Convert to database format
            db_data = {
                'title': title,
                'version': mop_data.get('version', '1.0'),
                'category': mop_data.get('category', 'Uncategorized'),
                'priority': 'Medium',  # Default priority
                'execution_date': None,
                'execution_time': None,
                'duration_minutes': None,
                'business_justification': mop_data.get('summary', ''),
                'executive_summary': mop_data.get('summary', ''),
                'devices': mop_data.get('devices', []),
                'networkConfigs': mop_data.get('networkConfigs', []),
                'risks': mop_data.get('risks', [])
            }
            
            # Add migration metadata
            db_data['migrated_from'] = os.path.basename(json_file)
            db_data['migrated_at'] = datetime.now().isoformat()
            
            print(f"   📝 Title: {title[:50]}{'...' if len(title) > 50 else ''}")
            
            # Save to database
            result = db.save_mop_document(db_data)
            
            if result:
                print(f"   ✅ Migrated successfully - Database ID: {result['id']}")
                migrated_count += 1
            else:
                print(f"   ❌ Migration failed")
                failed_count += 1
                
        except Exception as e:
            print(f"   ❌ Error processing {json_file}: {e}")
            failed_count += 1
    
    print(f"\n📊 Migration Summary:")
    print(f"   ✅ Successfully migrated: {migrated_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📁 Total files processed: {len(json_files)}")
    
    return failed_count == 0

def verify_migration():
    """Verify migration by checking database content"""
    print("\n🔍 Verifying migration...")
    
    load_env_file()
    from database import MOPDatabase
    
    db = MOPDatabase()
    
    try:
        conn = db.get_connection()
        
        if db.config.is_sqlite:
            cursor = conn.cursor()
            
            # Count total documents
            cursor.execute("SELECT COUNT(*) FROM mop_documents")
            total_count = cursor.fetchone()[0]
            
            # Get recent documents
            cursor.execute("""
                SELECT id, title, version, category, created_at 
                FROM mop_documents 
                ORDER BY id DESC 
                LIMIT 5
            """)
            recent_docs = cursor.fetchall()
            
            cursor.close()
        
        conn.close()
        
        print(f"📄 Total MOP documents in database: {total_count}")
        
        if recent_docs:
            print(f"📋 Recent documents:")
            for doc in recent_docs:
                print(f"   ID: {doc[0]} - {doc[1]} (v{doc[2]}) [{doc[3]}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main migration function"""
    print("🔄 MOP Generator Data Migration")
    print("=" * 50)
    
    # Check if database is setup
    if not os.path.exists('.env'):
        print("❌ Environment not configured. Please run setup_local_database.py first")
        return
    
    if not os.path.exists('mop_generator.sqlite'):
        print("❌ Database file not found. Please run setup_local_database.py first")
        return
    
    # Run migration
    success = migrate_existing_mops()
    
    if success:
        verify_migration()
        print("\n🎉 Migration completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Run the application: python3 app.py")
        print("   2. Create new MOP documents to test database functionality")
        print("   3. All existing MOPs are now available in the database")
    else:
        print("\n⚠️  Migration completed with some errors")
        print("   Check the output above for details")

if __name__ == "__main__":
    main()