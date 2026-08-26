"""
Database configuration and models for MOP Generator
Supports PostgreSQL (production), SQLite (development), and file-based (fallback)
"""

import os
import sqlite3
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

class DatabaseConfig:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.use_database = self.database_url is not None
        self.is_sqlite = self.database_url and self.database_url.startswith('sqlite:///')
        
        if self.use_database and not self.is_sqlite:
            # Parse PostgreSQL database URL for connection
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
    
    def get_sqlite_connection(self):
        """Get SQLite connection"""
        db_path = self.config.database_url.replace('sqlite:///', '')
        return sqlite3.connect(db_path)
    
    def get_connection(self):
        """Get database connection - supports both PostgreSQL and SQLite"""
        if not self.config.use_database:
            raise Exception("Database not configured")
        
        if self.config.is_sqlite:
            return self.get_sqlite_connection()
        else:
            return psycopg2.connect(**self.config.connection_params)
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a database query - supports both PostgreSQL and SQLite"""
        if not self.config.use_database:
            return None
            
        try:
            conn = self.get_connection()
            
            if self.config.is_sqlite:
                # SQLite execution
                cur = conn.cursor()
                
                # Convert PostgreSQL-style %(name)s parameters to SQLite ? style
                if params and isinstance(params, dict):
                    # Convert named parameters to positional for SQLite
                    sqlite_query = query
                    sqlite_params = []
                    
                    # Replace %(name)s with ? and collect values in order
                    import re
                    param_matches = re.findall(r'%\((\w+)\)s', query)
                    for param_name in param_matches:
                        sqlite_query = sqlite_query.replace(f'%({param_name})s', '?', 1)
                        sqlite_params.append(params.get(param_name))
                    
                    cur.execute(sqlite_query, sqlite_params)
                elif params:
                    # Positional parameters
                    sqlite_query = query.replace('%s', '?')  # Convert %s to ?
                    cur.execute(sqlite_query, params)
                else:
                    cur.execute(query)
                
                if fetch:
                    if query.strip().upper().startswith('SELECT'):
                        # Return list of dicts for compatibility
                        columns = [description[0] for description in cur.description]
                        rows = cur.fetchall()
                        result = [dict(zip(columns, row)) for row in rows]
                        cur.close()
                        conn.commit()
                        conn.close()
                        return result
                    else:
                        last_id = cur.lastrowid
                        cur.close()
                        conn.commit()
                        result = {'id': last_id} if last_id else True
                        conn.close()
                        return result
                
                last_id = cur.lastrowid
                cur.close()
                conn.commit()
                result = {'id': last_id} if last_id else True
                conn.close()
                return result
                
            else:
                # PostgreSQL execution
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
        """Save MOP document with comprehensive field mapping - ULTIMATE VERSION"""
        if not self.config.use_database:
            return self._save_mop_file(mop_data)
        
        try:
            print(f"🔍 Saving MOP with {len(mop_data)} input fields...")
            
            if self.config.is_sqlite:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                # Step 1: Insert basic required fields first
                basic_query = """
                INSERT INTO mop_documents (title, version, category, priority, 
                                         business_justification, executive_summary)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                
                basic_values = [
                    mop_data.get('title') or mop_data.get('document_title', 'Untitled MOP'),
                    mop_data.get('version', '1.0'),
                    mop_data.get('category'),
                    mop_data.get('priority'),
                    mop_data.get('business_justification'),
                    mop_data.get('executive_summary')
                ]
                
                cursor.execute(basic_query, basic_values)
                mop_id = cursor.lastrowid
                print(f"✅ Basic MOP created with ID: {mop_id}")
                
                # Step 2: Update with all extended fields individually
                update_fields = {
                    # Document fields
                    'document_title': mop_data.get('document_title') or mop_data.get('title'),
                    'activity_name': mop_data.get('activity_name'),
                    'work_type': mop_data.get('work_type'),
                    'issue_date': mop_data.get('issue_date'),
                    'execution_time': mop_data.get('execution_time'),
                    'total_duration': mop_data.get('total_duration'),
                    'affected_services': mop_data.get('affected_services'),
                    'downtime': mop_data.get('downtime'),
                    'summary': mop_data.get('summary') or mop_data.get('executive_summary'),
                    
                    # Technical Prerequisites
                    'hardware_requirements': mop_data.get('hardware_requirements'),
                    'software_dependencies': mop_data.get('software_dependencies'),
                    'network_prerequisites': mop_data.get('network_prerequisites'),
                    'security_requirements': mop_data.get('security_requirements'),
                    'personnel_requirements': mop_data.get('personnel_requirements'),
                    'external_dependencies': mop_data.get('external_dependencies'),
                    
                    # Risk Assessment
                    'overall_risk_level': mop_data.get('overall_risk_level'),
                    'risk_owner': mop_data.get('risk_owner'),
                    'contingency_plan': mop_data.get('contingency_plan'),
                    
                    # Implementation Timeline
                    'prep_start_time': mop_data.get('prep_start_time'),
                    'prep_phase_duration': mop_data.get('prep_phase_duration'),
                    'prep_activities': mop_data.get('prep_activities'),
                    'impl_start_time': mop_data.get('impl_start_time'),
                    'impl_phase_duration': mop_data.get('impl_phase_duration'),
                    'impl_activities': mop_data.get('impl_activities'),
                    'verification_start_time': mop_data.get('verification_start_time'),
                    'verification_duration': mop_data.get('verification_duration'),
                    'verification_activities': mop_data.get('verification_activities'),
                    
                    # Communication Plan
                    'communication_frequency': mop_data.get('communication_frequency', '15min'),
                    'notification_list': mop_data.get('notification_list'),
                    'technical_success_criteria': mop_data.get('technical_success_criteria'),
                    'business_success_criteria': mop_data.get('business_success_criteria'),
                    
                    # Post-Implementation
                    'monitoring_duration': mop_data.get('monitoring_duration', '24h'),
                    'monitoring_frequency': mop_data.get('monitoring_frequency', 'continuous'),
                    'monitoring_team': mop_data.get('monitoring_team'),
                    
                    # Rollback Procedures
                    'rollback_commands': mop_data.get('rollback_commands'),
                    'service_impact_level': mop_data.get('service_impact_level'),
                    'affected_processes': mop_data.get('affected_processes'),
                    'business_impact_cost': mop_data.get('business_impact_cost'),
                    'system_impact_level': mop_data.get('system_impact_level'),
                    'affected_systems': mop_data.get('affected_systems'),
                    'recovery_time_objective': mop_data.get('recovery_time_objective'),
                    'rollback_technical_validation': mop_data.get('rollback_technical_validation'),
                    'rollback_business_validation': mop_data.get('rollback_business_validation'),
                    
                    # Approval Signatures
                    'tech_reviewer_name': mop_data.get('tech_reviewer_name'),
                    'tech_reviewer_position': mop_data.get('tech_reviewer_position'),
                    'tech_reviewer_contact': mop_data.get('tech_reviewer_contact'),
                    'tech_review_date': mop_data.get('tech_review_date'),
                    'manager_name': mop_data.get('manager_name'),
                    'manager_position': mop_data.get('manager_position'),
                    'manager_contact': mop_data.get('manager_contact'),
                    'manager_approval_date': mop_data.get('manager_approval_date'),
                    'final_approver_name': mop_data.get('final_approver_name'),
                    'final_approver_title': mop_data.get('final_approver_title'),
                    'final_approver_contact': mop_data.get('final_approver_contact'),
                    'final_approval_date': mop_data.get('final_approval_date'),
                    
                    # Implementation Status
                    'implementation_status': mop_data.get('implementation_status', 'planned'),
                    'actual_start_time': mop_data.get('actual_start_time'),
                    'actual_end_time': mop_data.get('actual_end_time'),
                    'implementation_notes': mop_data.get('implementation_notes'),
                    
                    # Technical Details
                    'service_name': mop_data.get('service_name'),
                    'service_version': mop_data.get('service_version'),
                    'service_ports': mop_data.get('service_ports'),
                    'config_file_paths': mop_data.get('config_file_paths'),
                    'database_connections': mop_data.get('database_connections'),
                    'admin_accounts': mop_data.get('admin_accounts'),
                    'auth_method': mop_data.get('auth_method'),
                    'firewall_rules': mop_data.get('firewall_rules'),
                    'ssl_certificates': mop_data.get('ssl_certificates'),
                    
                    # Backup & Recovery
                    'backup_locations': mop_data.get('backup_locations'),
                    'backup_commands': mop_data.get('backup_commands'),
                    'rpo_target': mop_data.get('rpo_target'),
                    'rto_target': mop_data.get('rto_target'),
                    'environment_type': mop_data.get('environment_type', 'production'),
                    'datacenter_location': mop_data.get('datacenter_location'),
                    'maintenance_window': mop_data.get('maintenance_window')
                }
                
                # Update fields that have values - one by one for reliability
                updated_count = 0
                for field_name, field_value in update_fields.items():
                    if field_value is not None and field_value != '':
                        try:
                            cursor.execute(f"UPDATE mop_documents SET {field_name} = ? WHERE id = ?", 
                                         (field_value, mop_id))
                            updated_count += 1
                        except Exception as e:
                            print(f"⚠️  Failed to update {field_name}: {e}")
                
                print(f"✅ Updated {updated_count} extended fields")
                
                # Handle boolean fields separately
                bool_fields = {
                    'cert_technical': mop_data.get('cert_technical', False),
                    'cert_testing': mop_data.get('cert_testing', False),
                    'cert_documentation': mop_data.get('cert_documentation', False),
                    'cert_stakeholder': mop_data.get('cert_stakeholder', False)
                }
                
                for bool_field, bool_value in bool_fields.items():
                    try:
                        cursor.execute(f"UPDATE mop_documents SET {bool_field} = ? WHERE id = ?",
                                     (1 if bool_value else 0, mop_id))
                    except Exception as e:
                        print(f"⚠️  Failed to update {bool_field}: {e}")
                
                conn.commit()
                cursor.close()
                conn.close()
                
                # Save related data
                if mop_id:
                    if 'devices' in mop_data and mop_data['devices']:
                        self._save_devices(mop_id, mop_data['devices'])
                    
                    if 'networkConfigs' in mop_data and mop_data['networkConfigs']:
                        self._save_network_configs(mop_id, mop_data['networkConfigs'])
                    
                    if 'risks' in mop_data and mop_data['risks']:
                        self._save_risk_assessments(mop_id, mop_data['risks'])
                
                print(f"✅ MOP {mop_id} saved successfully with comprehensive field mapping")
                return {'id': mop_id, 'status': 'success'}
            
            return None
            
        except Exception as e:
            print(f"❌ Error saving MOP to database: {e}")
            import traceback
            traceback.print_exc()
            return None
    def _save_devices(self, mop_id, devices):
        """Save devices to database"""
        for idx, device in enumerate(devices):
            # Handle different field names from different data sources
            device_name = (device.get('name') or 
                          device.get('hostname') or 
                          device.get('device_name') or 
                          f'Device {idx + 1}')
            
            management_ip = (device.get('ip') or 
                           device.get('mgmt_ip') or 
                           device.get('management_ip'))
            
            device_type = (device.get('type') or 
                          device.get('device_type'))
            
            location = device.get('location')
            
            query = """
            INSERT INTO devices (mop_id, device_name, management_ip, location, device_type, order_index)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (mop_id, device_name, management_ip, location, device_type, idx)
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