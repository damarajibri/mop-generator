"""
Database configuration and models for MOP Generator
Supports both file-based (development) and PostgreSQL (production)
"""

import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

class DatabaseConfig:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.use_database = self.database_url is not None
        
        if self.use_database:
            # Parse database URL for connection
            url = urlparse(self.database_url)
            self.connection_params = {
                'host': url.hostname,
                'port': url.port or 5432,
                'database': url.path[1:],  # Remove leading '/'
                'user': url.username,
                'password': url.password,
            }
            
            # Handle SSL for Heroku and other cloud providers
            if 'sslmode' not in self.database_url:
                self.connection_params['sslmode'] = 'require'

class MOPDatabase:
    def __init__(self):
        self.config = DatabaseConfig()
    
    def get_connection(self):
        """Get database connection"""
        if not self.config.use_database:
            raise Exception("Database not configured")
        return psycopg2.connect(**self.config.connection_params)
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a database query"""
        if not self.config.use_database:
            return None
            
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    if fetch:
                        if 'SELECT' in query.upper():
                            return cur.fetchall()
                        else:
                            return cur.fetchone()
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def save_mop_document(self, mop_data):
        """Save MOP document to database"""
        if not self.config.use_database:
            return self._save_mop_file(mop_data)
        
        try:
            # Insert main document
            insert_doc_query = """
            INSERT INTO mop_documents (title, version, category, priority, execution_date, 
                                     execution_time, duration_minutes, business_justification, 
                                     executive_summary, status)
            VALUES (%(title)s, %(version)s, %(category)s, %(priority)s, %(execution_date)s,
                    %(execution_time)s, %(duration_minutes)s, %(business_justification)s,
                    %(executive_summary)s, 'draft')
            RETURNING id
            """
            
            doc_params = {
                'title': mop_data.get('title', 'Untitled MOP'),
                'version': mop_data.get('version', '1.0'),
                'category': mop_data.get('category'),
                'priority': mop_data.get('priority'),
                'execution_date': mop_data.get('execution_date'),
                'execution_time': mop_data.get('execution_time'),
                'duration_minutes': mop_data.get('duration_minutes'),
                'business_justification': mop_data.get('business_justification'),
                'executive_summary': mop_data.get('executive_summary')
            }
            
            result = self.execute_query(insert_doc_query, doc_params, fetch=True)
            if not result:
                return None
                
            mop_id = result['id']
            
            # Save devices
            if 'devices' in mop_data:
                self._save_devices(mop_id, mop_data['devices'])
            
            # Save network configs
            if 'networkConfigs' in mop_data:
                self._save_network_configs(mop_id, mop_data['networkConfigs'])
            
            # Save risk assessments
            if 'risks' in mop_data:
                self._save_risk_assessments(mop_id, mop_data['risks'])
            
            return {'id': mop_id, 'status': 'success'}
            
        except Exception as e:
            print(f"Error saving MOP to database: {e}")
            return None
    
    def _save_devices(self, mop_id, devices):
        """Save devices to database"""
        for idx, device in enumerate(devices):
            query = """
            INSERT INTO devices (mop_id, device_name, management_ip, location, device_type, order_index)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (mop_id, device['name'], device.get('ip'), device.get('location'), 
                     device.get('type'), idx)
            self.execute_query(query, params)
    
    def _save_network_configs(self, mop_id, configs):
        """Save network configurations to database"""
        for config in configs:
            query = """
            INSERT INTO network_configs (mop_id, real_ip, nat_ip, palo_alto_zone, vlan_id, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (mop_id, config.get('realIp'), config.get('natIp'), 
                     config.get('paloAltoZone'), config.get('vlanId'), config.get('description'))
            self.execute_query(query, params)
    
    def _save_risk_assessments(self, mop_id, risks):
        """Save risk assessments to database"""
        for idx, risk in enumerate(risks):
            query = """
            INSERT INTO risk_assessments (mop_id, risk_type, risk_description, impact_score, 
                                        probability_score, mitigation_plan, contingency_plan, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (mop_id, risk.get('type'), risk.get('description'), 
                     risk.get('impact'), risk.get('probability'),
                     risk.get('mitigation'), risk.get('contingency'), idx)
            self.execute_query(query, params)
    
    def _save_mop_file(self, mop_data):
        """Fallback: Save to file if no database"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"MOP_{timestamp}_{os.urandom(4).hex()}.json"
        filepath = os.path.join('generated_mops', filename)
        
        os.makedirs('generated_mops', exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mop_data, f, indent=2, ensure_ascii=False, default=str)
            return {'id': filename, 'status': 'success', 'filepath': filepath}
        except Exception as e:
            print(f"Error saving MOP file: {e}")
            return None
    
    def get_mop_document(self, mop_id):
        """Get MOP document by ID"""
        if not self.config.use_database:
            return self._get_mop_file(mop_id)
        
        # Implementation for database retrieval
        # This would fetch the complete MOP with all related data
        pass
    
    def list_mop_documents(self, limit=50):
        """List MOP documents"""
        if not self.config.use_database:
            return self._list_mop_files(limit)
        
        query = """
        SELECT id, title, version, category, priority, execution_date, 
               created_at, updated_at, status
        FROM mop_documents
        ORDER BY created_at DESC
        LIMIT %s
        """
        return self.execute_query(query, (limit,), fetch=True)

# Global database instance
db = MOPDatabase()