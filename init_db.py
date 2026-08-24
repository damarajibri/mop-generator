#!/usr/bin/env python3
"""
Database initialization script for MOP Generator
Runs on deployment to set up database schema
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def init_database():
    """Initialize database with schema"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("No DATABASE_URL found, skipping database initialization")
        return
    
    print("Initializing database...")
    
    try:
        # Parse database URL
        url = urlparse(database_url)
        connection_params = {
            'host': url.hostname,
            'port': url.port or 5432,
            'database': url.path[1:],  # Remove leading '/'
            'user': url.username,
            'password': url.password,
        }
        
        # Handle SSL for cloud providers
        if 'sslmode' not in database_url:
            connection_params['sslmode'] = 'require'
        
        # Connect and execute schema
        conn = psycopg2.connect(**connection_params)
        
        with open('database_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        
        conn.commit()
        conn.close()
        
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't exit with error code - let app start anyway
        # sys.exit(1)

if __name__ == '__main__':
    init_database()