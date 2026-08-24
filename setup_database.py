#!/usr/bin/env python3
"""
Database setup and initialization script for MOP Generator
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
import subprocess
import time

def check_database_connection(database_url, max_retries=30, retry_interval=2):
    """Check if database is accessible"""
    print(f"🔍 Checking database connection...")
    
    url = urlparse(database_url)
    connection_params = {
        'host': url.hostname,
        'port': url.port or 5432,
        'database': url.path[1:],  # Remove leading '/'
        'user': url.username,
        'password': url.password,
    }
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**connection_params)
            conn.close()
            print(f"✅ Database connection successful!")
            return True
        except psycopg2.Error as e:
            if attempt < max_retries - 1:
                print(f"⏳ Attempt {attempt + 1}/{max_retries} - Waiting for database... ({e})")
                time.sleep(retry_interval)
            else:
                print(f"❌ Database connection failed after {max_retries} attempts: {e}")
                return False
    
    return False

def run_schema_setup(database_url):
    """Run database schema setup"""
    print(f"🏗️  Setting up database schema...")
    
    try:
        url = urlparse(database_url)
        connection_params = {
            'host': url.hostname,
            'port': url.port or 5432,
            'database': url.path[1:],
            'user': url.username,
            'password': url.password,
        }
        
        # Read schema file
        with open('database_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        conn = psycopg2.connect(**connection_params)
        cur = conn.cursor()
        
        # Split and execute statements
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
        
        for statement in statements:
            if statement:
                try:
                    cur.execute(statement)
                    print(f"✅ Executed: {statement[:50]}...")
                except psycopg2.Error as e:
                    if "already exists" in str(e).lower():
                        print(f"ℹ️  Skipped (already exists): {statement[:50]}...")
                    else:
                        print(f"⚠️  Warning: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Database schema setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Schema setup failed: {e}")
        return False

def verify_tables(database_url):
    """Verify that all required tables exist"""
    print(f"🔍 Verifying database tables...")
    
    expected_tables = [
        'users', 'mop_documents', 'devices', 'network_configs', 
        'risk_assessments', 'implementation_steps', 'file_uploads', 
        'approval_signatures'
    ]
    
    try:
        url = urlparse(database_url)
        connection_params = {
            'host': url.hostname,
            'port': url.port or 5432,
            'database': url.path[1:],
            'user': url.username,
            'password': url.password,
        }
        
        conn = psycopg2.connect(**connection_params)
        cur = conn.cursor()
        
        # Check tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        
        existing_tables = [row[0] for row in cur.fetchall()]
        
        print(f"📋 Found tables: {', '.join(existing_tables)}")
        
        missing_tables = [table for table in expected_tables if table not in existing_tables]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
            return False
        else:
            print(f"✅ All required tables exist!")
            return True
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Table verification failed: {e}")
        return False

def start_docker_services():
    """Start Docker services for the application"""
    print(f"🐳 Starting Docker services...")
    
    try:
        # Check if Docker is running
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Docker is not installed or not running")
            return False
        
        # Start services - try docker compose first (new), then docker-compose (old)
        try:
            result = subprocess.run(['docker', 'compose', 'up', '-d'], capture_output=True, text=True)
        except FileNotFoundError:
            result = subprocess.run(['docker-compose', 'up', '-d'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to start Docker services: {result.stderr}")
            return False
        
        print(f"✅ Docker services started successfully!")
        print(f"📊 Services status:")
        
        # Show services status - try docker compose first, then docker-compose
        try:
            subprocess.run(['docker', 'compose', 'ps'])
        except FileNotFoundError:
            subprocess.run(['docker-compose', 'ps'])
        
        return True
        
    except Exception as e:
        print(f"❌ Docker startup failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 MOP Generator Database Setup")
    print("=" * 50)
    
    # Default database URL for Docker setup
    database_url = "postgresql://mop_user:mop_password_2026@localhost:5432/mop_generator"
    
    # Check if DATABASE_URL is set in environment
    env_db_url = os.environ.get('DATABASE_URL')
    if env_db_url:
        database_url = env_db_url
        print(f"📌 Using DATABASE_URL from environment")
    else:
        print(f"📌 Using default Docker database configuration")
    
    print(f"🔗 Database URL: {database_url}")
    print()
    
    # Step 1: Start Docker services
    if not start_docker_services():
        print(f"❌ Failed to start Docker services. Please check Docker installation.")
        sys.exit(1)
    
    print()
    
    # Step 2: Wait for database to be ready
    if not check_database_connection(database_url):
        print(f"❌ Cannot connect to database. Please check configuration.")
        sys.exit(1)
    
    print()
    
    # Step 3: Setup database schema
    if not run_schema_setup(database_url):
        print(f"❌ Database schema setup failed.")
        sys.exit(1)
    
    print()
    
    # Step 4: Verify setup
    if not verify_tables(database_url):
        print(f"❌ Database verification failed.")
        sys.exit(1)
    
    print()
    print("🎉 Database setup completed successfully!")
    print(f"📊 You can now access the application at: http://localhost:8080")
    print(f"💾 Database: postgresql://localhost:5432/mop_generator")
    print()
    print("💡 Next steps:")
    print("   1. Set DATABASE_URL environment variable (optional)")
    print("   2. Run the application: python3 app.py")
    print("   3. Or use Docker: docker-compose up -d")

if __name__ == "__main__":
    main()