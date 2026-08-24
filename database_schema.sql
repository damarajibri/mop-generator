-- MOP Generator Database Schema
-- PostgreSQL version

-- Users table for authentication (optional)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MOP Documents table
CREATE TABLE mop_documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    version VARCHAR(20) DEFAULT '1.0',
    category VARCHAR(50),
    priority VARCHAR(20),
    execution_date DATE,
    execution_time TIME,
    duration_minutes INTEGER,
    business_justification TEXT,
    executive_summary TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'draft'
);

-- Devices table
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
    device_name VARCHAR(100) NOT NULL,
    management_ip INET,
    location VARCHAR(100),
    device_type VARCHAR(50),
    order_index INTEGER DEFAULT 0
);

-- Network Configuration table
CREATE TABLE network_configs (
    id SERIAL PRIMARY KEY,
    mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
    real_ip INET,
    nat_ip INET,
    palo_alto_zone VARCHAR(50),
    vlan_id INTEGER,
    description TEXT
);

-- Risk Assessment table
CREATE TABLE risk_assessments (
    id SERIAL PRIMARY KEY,
    mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
    risk_type VARCHAR(20) CHECK (risk_type IN ('technical', 'business')),
    risk_description TEXT NOT NULL,
    impact_score INTEGER CHECK (impact_score BETWEEN 1 AND 5),
    probability_score INTEGER CHECK (probability_score BETWEEN 1 AND 5),
    risk_score INTEGER GENERATED ALWAYS AS (impact_score * probability_score) STORED,
    mitigation_plan TEXT,
    contingency_plan TEXT,
    order_index INTEGER DEFAULT 0
);

-- Implementation Steps table
CREATE TABLE implementation_steps (
    id SERIAL PRIMARY KEY,
    device_id INTEGER REFERENCES devices(id) ON DELETE CASCADE,
    step_type VARCHAR(20) CHECK (step_type IN ('pre', 'implementation', 'verification', 'rollback')),
    content_html TEXT,
    content_text TEXT,
    order_index INTEGER DEFAULT 0
);

-- File Uploads table
CREATE TABLE file_uploads (
    id SERIAL PRIMARY KEY,
    mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approval Signatures table
CREATE TABLE approval_signatures (
    id SERIAL PRIMARY KEY,
    mop_id INTEGER REFERENCES mop_documents(id) ON DELETE CASCADE,
    approver_name VARCHAR(100) NOT NULL,
    approver_role VARCHAR(100) NOT NULL,
    approval_level INTEGER NOT NULL,
    signature_date DATE,
    approval_status VARCHAR(20) DEFAULT 'pending',
    comments TEXT,
    order_index INTEGER DEFAULT 0
);

-- Indexes for performance
CREATE INDEX idx_mop_documents_created_by ON mop_documents(created_by);
CREATE INDEX idx_mop_documents_status ON mop_documents(status);
CREATE INDEX idx_devices_mop_id ON devices(mop_id);
CREATE INDEX idx_network_configs_mop_id ON network_configs(mop_id);
CREATE INDEX idx_risk_assessments_mop_id ON risk_assessments(mop_id);
CREATE INDEX idx_implementation_steps_device_id ON implementation_steps(device_id);
CREATE INDEX idx_file_uploads_mop_id ON file_uploads(mop_id);
CREATE INDEX idx_approval_signatures_mop_id ON approval_signatures(mop_id);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_mop_documents_updated_at BEFORE UPDATE ON mop_documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();