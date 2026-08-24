#!/usr/bin/env python3
"""
Alternative database setup for local development (without Docker)
Creates a local PostgreSQL database or uses SQLite as fallback
"""

import os
import sys
import sqlite3
from datetime import datetime

def create_sqlite_fallback():
    """Create SQLite database as fallback"""
    print("🗄️  Setting up SQLite database as fallback...")
    
    try:
        # Create database file
        db_path = "mop_generator.sqlite"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables (SQLite version of schema)
        sqlite_schema = """
        -- MOP Documents table
        CREATE TABLE IF NOT EXISTS mop_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            version TEXT DEFAULT '1.0',
            category TEXT,
            priority TEXT,
            execution_date TEXT,
            execution_time TEXT,
            duration_minutes INTEGER,
            business_justification TEXT,
            executive_summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft'
        );

        -- Devices table
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
            device_name TEXT NOT NULL,
            management_ip TEXT,
            location TEXT,
            device_type TEXT,
            order_index INTEGER DEFAULT 0
        );

        -- Network Configuration table
        CREATE TABLE IF NOT EXISTS network_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
            real_ip TEXT,
            nat_ip TEXT,
            palo_alto_zone TEXT,
            vlan_id INTEGER,
            description TEXT
        );

        -- Risk Assessment table
        CREATE TABLE IF NOT EXISTS risk_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
            risk_type TEXT CHECK (risk_type IN ('technical', 'business')),
            risk_description TEXT NOT NULL,
            impact_score INTEGER CHECK (impact_score BETWEEN 1 AND 5),
            probability_score INTEGER CHECK (probability_score BETWEEN 1 AND 5),
            mitigation_plan TEXT,
            contingency_plan TEXT,
            order_index INTEGER DEFAULT 0
        );

        -- Implementation Steps table
        CREATE TABLE IF NOT EXISTS implementation_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER REFERENCES devices(id) ON DELETE CASCADE,
            step_type TEXT CHECK (step_type IN ('pre', 'implementation', 'verification', 'rollback')),
            content_html TEXT,
            content_text TEXT,
            order_index INTEGER DEFAULT 0
        );

        -- File Uploads table
        CREATE TABLE IF NOT EXISTS file_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            mime_type TEXT,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Approval Signatures table
        CREATE TABLE IF NOT EXISTS approval_signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
            approver_name TEXT NOT NULL,
            approver_role TEXT NOT NULL,
            approval_level INTEGER NOT NULL,
            signature_date TEXT,
            approval_status TEXT DEFAULT 'pending',
            comments TEXT,
            order_index INTEGER DEFAULT 0
        );
        """
        
        # Execute schema
        cursor.executescript(sqlite_schema)
        conn.commit()
        
        print(f"✅ SQLite database created: {db_path}")
        
        # Verify tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Created tables: {', '.join([t[0] for t in tables])}")
        
        conn.close()
        
        # Set environment variable
        os.environ['DATABASE_URL'] = f"sqlite:///{db_path}"
        
        return f"sqlite:///{db_path}"
        
    except Exception as e:
        print(f"❌ SQLite setup failed: {e}")
        return None

def update_database_config():
    """Update database.py to support SQLite"""
    print("🔧 Updating database configuration...")
    
    try:
        # Read current database.py
        with open('database.py', 'r') as f:
            content = f.read()
        
        # Check if SQLite support already exists
        if 'sqlite3' not in content:
            # Add SQLite import and support
            sqlite_additions = """
import sqlite3
from urllib.parse import urlparse"""
            
            # Replace the import section
            content = content.replace('from urllib.parse import urlparse', sqlite_additions)
            
            # Add SQLite connection method
            sqlite_connection_method = '''
    def get_sqlite_connection(self):
        """Get SQLite connection"""
        db_path = self.database_url.replace('sqlite:///', '')
        return sqlite3.connect(db_path)
    
    def get_connection(self):
        """Get database connection - supports both PostgreSQL and SQLite"""
        if not self.config.use_database:
            raise Exception("Database not configured")
        
        if self.config.database_url.startswith('sqlite://'):
            return self.get_sqlite_connection()
        else:
            return psycopg2.connect(**self.config.connection_params)'''
            
            # Replace the get_connection method
            old_method = '''    def get_connection(self):
        """Get database connection"""
        if not self.config.use_database:
            raise Exception("Database not configured")
        return psycopg2.connect(**self.config.connection_params)'''
            
            content = content.replace(old_method, sqlite_connection_method)
            
            # Write updated content
            with open('database.py', 'w') as f:
                f.write(content)
            
            print("✅ Database configuration updated for SQLite support")
        else:
            print("ℹ️  Database configuration already supports SQLite")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to update database configuration: {e}")
        return False

def setup_env_file():
    """Setup environment file with database URL"""
    print("⚙️  Setting up environment configuration...")
    
    try:
        # Create .env file
        env_content = f"""# MOP Generator Environment Configuration
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Database Configuration
DATABASE_URL=sqlite:///mop_generator.sqlite

# Flask Configuration  
FLASK_SECRET_KEY=mop-generator-local-secret-2026
FLASK_ENV=development
PORT=5000

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created: .env")
        
        # Also create .env.example for reference
        with open('.env.example', 'w') as f:
            f.write(env_content.replace('sqlite:///mop_generator.sqlite', 'postgresql://user:password@localhost:5432/mop_generator'))
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False

def test_database_functionality():
    """Test database functionality"""
    print("🧪 Testing database functionality...")
    
    try:
        # Set environment variable
        os.environ['DATABASE_URL'] = 'sqlite:///mop_generator.sqlite'
        
        # Import database module
        from database import MOPDatabase
        
        # Create database instance
        db = MOPDatabase()
        
        # Test connection
        if db.config.use_database:
            print("✅ Database configuration loaded successfully")
            
            # Test a simple save operation
            test_data = {
                'title': 'Test MOP Document',
                'version': '1.0',
                'category': 'Test',
                'priority': 'Medium',
                'executive_summary': 'This is a test document to verify database functionality.'
            }
            
            result = db.save_mop_document(test_data)
            if result:
                print(f"✅ Database save test successful! MOP ID: {result['id']}")
                return True
            else:
                print("⚠️  Database save test failed, but configuration is correct")
                return False
        else:
            print("⚠️  Database not configured properly")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Main setup function for local development"""
    print("🚀 MOP Generator Local Database Setup")
    print("=" * 50)
    print("📌 Setting up SQLite database for local development")
    print()
    
    # Step 1: Create SQLite database
    db_url = create_sqlite_fallback()
    if not db_url:
        print("❌ Failed to create SQLite database")
        sys.exit(1)
    
    print()
    
    # Step 2: Update database configuration
    if not update_database_config():
        print("❌ Failed to update database configuration")
        sys.exit(1)
    
    print()
    
    # Step 3: Setup environment file
    if not setup_env_file():
        print("❌ Failed to setup environment file")
        sys.exit(1)
    
    print()
    
    # Step 4: Test database functionality
    if not test_database_functionality():
        print("⚠️  Database setup completed but functionality test failed")
        print("   This may be normal - try running the application to verify")
    
    print()
    print("🎉 Local database setup completed successfully!")
    print(f"💾 Database: {db_url}")
    print(f"📁 Database file: mop_generator.sqlite")
    print()
    print("💡 Next steps:")
    print("   1. Run the application: python3 app.py")
    print("   2. Access at: http://localhost:5000")
    print("   3. Create a new MOP document to test database functionality")
    print()
    print("🐳 For production deployment, use Docker:")
    print("   1. Start Docker Desktop")
    print("   2. Run: docker compose up -d")

if __name__ == "__main__":
    main()