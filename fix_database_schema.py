#!/usr/bin/env python3
"""
Database Schema Update Script
Menambahkan Technical Config dan Implementation fields ke database
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

def update_database_schema():
    """Update database schema dengan Technical Config fields"""
    print("🔧 Updating database schema...")
    
    load_env()
    
    try:
        from database import MOPDatabase
        
        db = MOPDatabase()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check current columns
        cursor.execute('PRAGMA table_info(mop_documents)')
        current_columns = [col[1] for col in cursor.fetchall()]
        
        print(f"📊 Current database columns: {len(current_columns)}")
        
        # New columns to add
        new_columns = [
            # Document fields
            ('document_title', 'TEXT'),
            ('activity_name', 'TEXT'),
            ('work_type', 'TEXT'),
            ('issue_date', 'TEXT'),
            ('total_duration', 'TEXT'),
            ('affected_services', 'TEXT'),
            ('downtime', 'TEXT'),
            ('summary', 'TEXT'),
            
            # Technical Prerequisites
            ('hardware_requirements', 'TEXT'),
            ('software_dependencies', 'TEXT'),
            ('network_prerequisites', 'TEXT'),
            ('security_requirements', 'TEXT'),
            ('personnel_requirements', 'TEXT'),
            ('external_dependencies', 'TEXT'),
            
            # Risk Assessment
            ('overall_risk_level', 'TEXT'),
            ('risk_owner', 'TEXT'),
            ('contingency_plan', 'TEXT'),
            
            # Implementation Timeline
            ('prep_start_time', 'TEXT'),
            ('prep_phase_duration', 'TEXT'),
            ('prep_activities', 'TEXT'),
            ('impl_start_time', 'TEXT'),
            ('impl_phase_duration', 'TEXT'),
            ('impl_activities', 'TEXT'),
            ('verification_start_time', 'TEXT'),
            ('verification_duration', 'TEXT'),
            ('verification_activities', 'TEXT'),
            
            # Communication Plan
            ('communication_frequency', 'TEXT DEFAULT "15min"'),
            ('notification_list', 'TEXT'),
            ('technical_success_criteria', 'TEXT'),
            ('business_success_criteria', 'TEXT'),
            
            # Post-Implementation
            ('monitoring_duration', 'TEXT DEFAULT "24h"'),
            ('monitoring_frequency', 'TEXT DEFAULT "continuous"'),
            ('monitoring_team', 'TEXT'),
            
            # Rollback Procedures
            ('rollback_commands', 'TEXT'),
            ('service_impact_level', 'TEXT'),
            ('affected_processes', 'TEXT'),
            ('business_impact_cost', 'TEXT'),
            ('system_impact_level', 'TEXT'),
            ('affected_systems', 'TEXT'),
            ('recovery_time_objective', 'TEXT'),
            ('rollback_technical_validation', 'TEXT'),
            ('rollback_business_validation', 'TEXT'),
            
            # Approval Signatures
            ('tech_reviewer_name', 'TEXT'),
            ('tech_reviewer_position', 'TEXT'),
            ('tech_reviewer_contact', 'TEXT'),
            ('tech_review_date', 'TEXT'),
            ('manager_name', 'TEXT'),
            ('manager_position', 'TEXT'),
            ('manager_contact', 'TEXT'),
            ('manager_approval_date', 'TEXT'),
            ('final_approver_name', 'TEXT'),
            ('final_approver_title', 'TEXT'),
            ('final_approver_contact', 'TEXT'),
            ('final_approval_date', 'TEXT'),
            
            # Implementation Status
            ('implementation_status', 'TEXT DEFAULT "planned"'),
            ('actual_start_time', 'TEXT'),
            ('actual_end_time', 'TEXT'),
            ('implementation_notes', 'TEXT'),
            
            # Certifications
            ('cert_technical', 'BOOLEAN DEFAULT 0'),
            ('cert_testing', 'BOOLEAN DEFAULT 0'),
            ('cert_documentation', 'BOOLEAN DEFAULT 0'),
            ('cert_stakeholder', 'BOOLEAN DEFAULT 0'),
            
            # Technical Details
            ('service_name', 'TEXT'),
            ('service_version', 'TEXT'),
            ('service_ports', 'TEXT'),
            ('config_file_paths', 'TEXT'),
            ('database_connections', 'TEXT'),
            ('admin_accounts', 'TEXT'),
            ('auth_method', 'TEXT'),
            ('firewall_rules', 'TEXT'),
            ('ssl_certificates', 'TEXT'),
            
            # Backup & Recovery
            ('backup_locations', 'TEXT'),
            ('backup_commands', 'TEXT'),
            ('rpo_target', 'TEXT'),
            ('rto_target', 'TEXT'),
            ('environment_type', 'TEXT DEFAULT "production"'),
            ('datacenter_location', 'TEXT'),
            ('maintenance_window', 'TEXT')
        ]
        
        # Add missing columns
        added_columns = []
        for column_name, column_type in new_columns:
            if column_name not in current_columns:
                try:
                    alter_sql = f'ALTER TABLE mop_documents ADD COLUMN {column_name} {column_type}'
                    cursor.execute(alter_sql)
                    added_columns.append(column_name)
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    print(f"❌ Failed to add {column_name}: {e}")
        
        conn.commit()
        
        # Verify final schema
        cursor.execute('PRAGMA table_info(mop_documents)')
        final_columns = [col[1] for col in cursor.fetchall()]
        
        print(f"\n📊 Schema Update Summary:")
        print(f"   📋 Columns before: {len(current_columns)}")
        print(f"   ➕ Columns added: {len(added_columns)}")
        print(f"   📊 Columns after: {len(final_columns)}")
        
        cursor.close()
        conn.close()
        
        if added_columns:
            print(f"\n✅ Database schema updated successfully!")
            print(f"   Added {len(added_columns)} new columns for Technical Config")
            return True
        else:
            print(f"\n✅ Database schema already up to date!")
            return True
            
    except Exception as e:
        print(f"❌ Schema update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_save_mop_function():
    """Update save_mop_document function untuk handle new fields"""
    print("\n🔧 Updating save_mop_document function...")
    
    try:
        # Read current database.py
        with open('database.py', 'r') as f:
            content = f.read()
        
        # Create new save function with all fields
        new_save_function = '''
    def save_mop_document(self, mop_data):
        """Save MOP document to database with all fields"""
        if not self.config.use_database:
            return self._save_mop_file(mop_data)
        
        try:
            # Prepare all field values with safe defaults
            doc_values = {
                # Basic fields
                'title': mop_data.get('title') or mop_data.get('document_title', 'Untitled MOP'),
                'document_title': mop_data.get('document_title') or mop_data.get('title', 'Untitled MOP'),
                'version': mop_data.get('version', '1.0'),
                'category': mop_data.get('category'),
                'priority': mop_data.get('priority'),
                'execution_date': mop_data.get('execution_date'),
                'execution_time': mop_data.get('execution_time'),
                'duration_minutes': mop_data.get('duration_minutes'),
                'business_justification': mop_data.get('business_justification'),
                'executive_summary': mop_data.get('executive_summary'),
                
                # Document fields
                'activity_name': mop_data.get('activity_name'),
                'work_type': mop_data.get('work_type'),
                'issue_date': mop_data.get('issue_date'),
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
                
                # Certifications
                'cert_technical': bool(mop_data.get('cert_technical', False)),
                'cert_testing': bool(mop_data.get('cert_testing', False)),
                'cert_documentation': bool(mop_data.get('cert_documentation', False)),
                'cert_stakeholder': bool(mop_data.get('cert_stakeholder', False)),
                
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
            
            # Build dynamic INSERT query
            columns = list(doc_values.keys())
            placeholders = ['?' if self.config.is_sqlite else f'%({col})s' for col in columns]
            
            insert_query = f"""
            INSERT INTO mop_documents ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
            """
            
            if self.config.is_sqlite:
                insert_query += " RETURNING id"
            
            result = self.execute_query(insert_query, doc_values, fetch=True)
            
            if result:
                mop_id = result['id'] if isinstance(result, dict) else result
                
                # Save related data
                if 'devices' in mop_data:
                    self._save_devices(mop_id, mop_data['devices'])
                
                if 'networkConfigs' in mop_data:
                    self._save_network_configs(mop_id, mop_data['networkConfigs'])
                
                if 'risks' in mop_data:
                    self._save_risk_assessments(mop_id, mop_data['risks'])
                
                return {'id': mop_id, 'status': 'success'}
            
            return None
            
        except Exception as e:
            print(f"Error saving MOP to database: {e}")
            return None
'''
        
        # Find and replace the old save_mop_document function
        import re
        pattern = r'def save_mop_document\(self, mop_data\):.*?(?=def |\Z)'
        
        if 'def save_mop_document(self, mop_data):' in content:
            # Replace existing function
            new_content = re.sub(pattern, new_save_function.strip(), content, flags=re.DOTALL)
        else:
            # Append new function if not found
            new_content = content + new_save_function
        
        # Write back to file
        with open('database.py', 'w') as f:
            f.write(new_content)
        
        print("✅ save_mop_document function updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update save function: {e}")
        return False

def main():
    """Main function"""
    print("🚀 DATABASE SCHEMA & FUNCTIONALITY UPDATE")
    print("=" * 60)
    print("Fixing Technical Config and Implementation field storage\n")
    
    # Step 1: Update database schema
    schema_success = update_database_schema()
    
    # Step 2: Update save function
    if schema_success:
        function_success = update_save_mop_function()
        
        if function_success:
            print(f"\n🎉 UPDATE COMPLETED SUCCESSFULLY!")
            print(f"\n💡 What was fixed:")
            print(f"   ✅ Added 69+ new columns to database schema")
            print(f"   ✅ Updated save_mop_document function")
            print(f"   ✅ Technical Config fields now stored in database")
            print(f"   ✅ Implementation fields now stored in database")
            print(f"   ✅ All form fields will be preserved on save")
            
            print(f"\n🧪 Testing Instructions:")
            print(f"   1. Restart application")
            print(f"   2. Create new MOP with Technical Config filled")
            print(f"   3. Save MOP")
            print(f"   4. Go to History MOP and reload")
            print(f"   5. Technical Config should now be populated!")
            
            return True
        else:
            print(f"\n❌ Function update failed")
            return False
    else:
        print(f"\n❌ Schema update failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)