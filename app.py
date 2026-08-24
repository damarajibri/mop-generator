from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import uuid
from datetime import datetime
import socket
import base64
import mimetypes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mop-generator-secret-2026'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('generated_mops', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_free_port():
    """Find an available port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image file provided'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return jsonify({
                'success': True, 
                'image_url': f"/uploads/{filename}",
                'filename': filename
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid file type'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/api/save_mop', methods=['POST'])
def save_mop():
    try:
        data = request.json or {}
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MOP_{timestamp}_{uuid.uuid4().hex[:8]}"
        
        # Save JSON data
        json_path = os.path.join('generated_mops', f"{filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Generate HTML with safe error handling
        html_content = generate_safe_html(data)
        html_path = os.path.join('generated_mops', f"{filename}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return jsonify({
            'success': True,
            'message': 'MOP generated successfully!',
            'filename': filename,
            'download_urls': {
                'html': f"/download/{filename}.html",
                'json': f"/download/{filename}.json"
            }
        })
        
    except Exception as e:
        print(f"Error in save_mop: {e}")
        return jsonify({'success': False, 'message': f'Error generating MOP: {str(e)}'})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join('generated_mops', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return "File not found", 404
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

def process_rich_content(html_content):
    """Process HTML content from rich editor and embed images"""
    if not html_content:
        return ""
    
    try:
        import re
        
        # Find all image tags with local URLs
        img_pattern = r'<img[^>]+src=[\'"]([^\'">]+)[\'"][^>]*>'
        
        def replace_image(match):
            img_tag = match.group(0)
            img_src = match.group(1)
            
            if img_src.startswith('/uploads/'):
                # Convert to base64
                base64_img = safe_image_to_base64(img_src)
                if base64_img:
                    return img_tag.replace(img_src, f'data:image/png;base64,{base64_img}')
            
            return img_tag
        
        processed_html = re.sub(img_pattern, replace_image, html_content)
        return processed_html
        
    except Exception as e:
        print(f"Error processing rich content: {e}")
        return html_content or ""

def safe_image_to_base64(image_url):
    """Safely convert image to base64"""
    try:
        if not image_url:
            return ""
            
        if image_url.startswith('/uploads/'):
            filename = image_url.replace('/uploads/', '')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            filepath = image_url
            
        if os.path.exists(filepath):
            with open(filepath, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded_string
        return ""
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return ""

def generate_safe_html(data):
    """Generate HTML with comprehensive error handling"""
    try:
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Ensure data is not None and is a dictionary
        if not data or not isinstance(data, dict):
            data = {}
        
        def safe_get(key, default=''):
            """Safely get value from data with fallback"""
            value = data.get(key, default)
            return str(value) if value is not None else str(default)
        
        def safe_format_table(items, fields):
            """Safely format table with error handling"""
            try:
                if not items or not isinstance(items, list):
                    return "<p>No items specified</p>"
                
                html = "<table class='table table-bordered table-sm'><thead><tr>"
                for field, label in fields.items():
                    html += f"<th>{label or 'N/A'}</th>"
                html += "</tr></thead><tbody>"
                
                for item in items:
                    if not item or not isinstance(item, dict):
                        continue
                    html += "<tr>"
                    for field in fields.keys():
                        value = item.get(field, '') or ''
                        html += f"<td>{str(value) or 'N/A'}</td>"
                    html += "</tr>"
                html += "</tbody></table>"
                return html
            except Exception as e:
                print(f"Error in safe_format_table: {e}")
                return "<p>Error formatting table</p>"
        
        def safe_format_device_images(images, section_title):
            """Safely format device images"""
            try:
                if not images or not isinstance(images, list) or len(images) == 0:
                    return f"<p class='text-muted small'>No {section_title.lower()} images attached</p>"
                
                html = f"<div class='device-images mb-2'>"
                for img in images:
                    if not img or not isinstance(img, dict):
                        continue
                        
                    filename = img.get('filename', 'Unknown') or 'Unknown'
                    image_url = img.get('url', '') or ''
                    
                    if image_url:
                        # Convert image to base64 for embedding
                        base64_image = safe_image_to_base64(image_url)
                        
                        if base64_image:
                            html += f"""
                                <div class='image-item mb-2 p-2 border rounded' style='background: #f8f9fa;'>
                                    <img src='data:image/png;base64,{base64_image}' 
                                         style='max-width: 200px; max-height: 150px; object-fit: contain;' 
                                         class='img-thumbnail d-block mb-1'>
                                    <small class='text-muted'><strong>{section_title}:</strong> {filename}</small>
                                </div>
                            """
                        else:
                            html += f"""
                                <div class='image-item mb-2 p-2 border rounded' style='background: #fff3cd;'>
                                    <i class='fas fa-exclamation-triangle text-warning'></i>
                                    <small class='text-muted'>Image not accessible: {filename}</small>
                                </div>
                            """
                html += f"</div>"
                return html
            except Exception as e:
                print(f"Error in safe_format_device_images: {e}")
                return f"<p class='text-muted small'>Error loading {section_title.lower()} images</p>"
        
        def safe_image_to_base64(image_url):
            """Safely convert image to base64"""
            try:
                if not image_url:
                    return ""
                    
                if image_url.startswith('/uploads/'):
                    filename = image_url.replace('/uploads/', '')
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                else:
                    filepath = image_url
                    
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        return encoded_string
                return ""
            except Exception as e:
                print(f"Error converting image to base64: {e}")
                return ""

        # Generate HTML content safely
        html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_get('document_title', 'Method of Procedure')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 3px solid #2c3e50; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: #2c3e50; margin: 0; font-size: 2.2em; }}
        .header h2 {{ color: #34495e; margin: 10px 0; }}
        .section {{ margin-bottom: 40px; page-break-inside: avoid; }}
        .section h2 {{ background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 12px 20px; margin: 0 0 20px 0; border-radius: 5px; }}
        .section h3 {{ color: #2c3e50; border-left: 4px solid #3498db; padding-left: 15px; margin-top: 25px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        table th {{ background: #34495e; color: white; padding: 12px; text-align: left; font-weight: bold; }}
        table td {{ padding: 10px; border: 1px solid #ddd; vertical-align: top; }}
        table tr:nth-child(even) {{ background-color: #f8f9fa; }}
        .info-box {{ background: #e8f6f3; border-left: 5px solid #16a085; padding: 15px; margin: 15px 0; }}
        .warning-box {{ background: #fef9e7; border-left: 5px solid #f39c12; padding: 15px; margin: 15px 0; }}
        .danger-box {{ background: #fadbd8; border-left: 5px solid #e74c3c; padding: 15px; margin: 15px 0; }}
        .success-box {{ background: #d5f4e6; border-left: 5px solid #27ae60; padding: 15px; margin: 15px 0; }}
        .code-block {{ background: #2c3e50; color: #ecf0f1; padding: 20px; font-family: 'Courier New', monospace; margin: 15px 0; border-radius: 5px; overflow-x: auto; }}
        .image-item img {{ border: 1px solid #dee2e6; border-radius: 4px; }}
        .rich-content {{ padding: 10px; border-radius: 5px; }}
        .rich-content img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; margin: 10px 0; }}
        .rich-content pre {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .rich-content blockquote {{ background: #e8f6f3; border-left: 4px solid #16a085; padding: 10px; margin: 10px 0; }}
        .code-block {{ background: #2c3e50; color: #ecf0f1; padding: 20px; font-family: 'Courier New', monospace; margin: 15px 0; border-radius: 5px; overflow-x: auto; }}
        .implementation-subsection {{ background: rgba(248, 249, 250, 0.8); border-radius: 8px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #007bff; }}
        .implementation-subsection h5 {{ margin-bottom: 15px; }}
        .device-impl-section {{ background: rgba(255, 255, 255, 0.95); border: 2px solid #e9ecef; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        @media print {{ 
            body {{ font-size: 11px; margin: 20px; }} 
            .section {{ page-break-inside: avoid; }}
            .code-block {{ background: #f8f9fa !important; color: #333 !important; border: 1px solid #ddd; }}
            .rich-content pre {{ background: #f8f9fa !important; color: #333 !important; border: 1px solid #ddd; }}
            .implementation-subsection {{ background: #f8f9fa !important; border-left: 4px solid #007bff; }}
            .image-item img {{ max-width: 300px !important; height: auto !important; page-break-inside: avoid; }}
            .rich-content img {{ max-width: 250px !important; height: auto !important; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>METHOD OF PROCEDURE (MOP)</h1>
        <h2>{safe_get('document_title', 'Untitled MOP')}</h2>
        <p><strong>Version:</strong> {safe_get('version', '1.0')} | <strong>Generated:</strong> {current_time}</p>
    </div>

    <div class="section">
        <h2>1. DOCUMENT INFORMATION</h2>
        <table>
            <tr><th style="width: 30%">Field</th><th>Value</th></tr>
            <tr><td>Document Title</td><td>{safe_get('document_title')}</td></tr>
            <tr><td>Version</td><td>{safe_get('version', '1.0')}</td></tr>
            <tr><td>Category</td><td>{safe_get('category')}</td></tr>
            <tr><td>Activity Name</td><td>{safe_get('activity_name')}</td></tr>
            <tr><td>Work Type</td><td>{safe_get('work_type')}</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>2. EXECUTIVE SUMMARY</h2>
        <div class="info-box">
            <strong>Summary:</strong><br>
            {safe_get('summary', 'No summary provided')}
        </div>
        <table>
            <tr><th>Parameter</th><th>Detail</th></tr>
            <tr><td>Execution Time</td><td>{safe_get('execution_time')}</td></tr>
            <tr><td>Total Duration</td><td>{safe_get('total_duration')}</td></tr>
            <tr><td>Affected Services</td><td>{safe_get('affected_services')}</td></tr>
            <tr><td>Expected Downtime</td><td>{safe_get('downtime')}</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>3. TECHNICAL CONFIGURATION</h2>
        <h3>Device Information</h3>
        {safe_format_table(data.get('devices', []) or [], {
            'hostname': 'Hostname',
            'type': 'Type',
            'mgmt_ip': 'Management IP',
            'location': 'Location'
        })}
        
        <h3>Network Configuration</h3>
        {safe_format_table(data.get('ip_zone_configs', []) or [], {
            'real_ip_address': 'Real IP',
            'real_zone_name': 'Real Zone',
            'nat_ip_address': 'NAT IP',
            'nat_zone_name': 'NAT Zone'
        })}
    </div>

    <div class="section">
        <h2>4. RISK ASSESSMENT & ANALYSIS</h2>
        <div class="warning-box">
            <strong>Overall Risk Level:</strong> {safe_get('overall_risk_level', 'Not assessed')}<br>
            <strong>Risk Owner:</strong> {safe_get('risk_owner', 'Not specified')}
        </div>
        
        <h3>Technical Risks</h3>
        {safe_format_table(data.get('technical_risks', []) or [], {
            'desc': 'Risk Description',
            'impact': 'Impact (1-5)',
            'probability': 'Probability (1-5)', 
            'mitigation': 'Mitigation Strategy'
        })}

        <h3>Business Risks</h3>
        {safe_format_table(data.get('business_risks', []) or [], {
            'desc': 'Risk Description',
            'impact': 'Impact (1-5)',
            'probability': 'Probability (1-5)',
            'mitigation': 'Mitigation Strategy'
        })}

        <div class="info-box">
            <strong>Contingency Plan:</strong><br>
            {safe_get('contingency_plan', 'No contingency plan specified')}
        </div>
    </div>

    <div class="section">
        <h2>5. IMPLEMENTATION STEPS</h2>
        <h3>Implementation Commands</h3>
        <div class="rich-content">
{process_rich_content(data.get('general_implementation_commands_html', '')) or f"<div class='code-block'>{safe_get('general_implementation_commands', safe_get('implementation_commands', '# No commands specified'))}</div>"}
        </div>
        
        <!-- Device-specific implementations with images -->
        <h3>Device-Specific Implementation</h3>
        {generate_device_sections(data.get('device_implementations', []) or [], data.get('devices', []) or [], safe_format_device_images)}
    </div>

    <div class="section">
        <h2>6. ROLLBACK PROCEDURES</h2>
        <div class="danger-box">
            <strong>Rollback Commands:</strong>
        </div>
        <div class="code-block">
{safe_get('rollback_commands', '# No rollback commands specified')}
        </div>
    </div>

    <div class="section">
        <h2>7. APPROVAL SIGNATURES</h2>
        <table>
            <tr><th>Role</th><th>Name</th><th>Position</th><th>Date</th></tr>
            <tr><td>Technical Reviewer</td><td>{safe_get('tech_reviewer_name')}</td><td>{safe_get('tech_reviewer_position')}</td><td>{current_time}</td></tr>
            <tr><td>Manager</td><td>{safe_get('manager_name')}</td><td>{safe_get('manager_position')}</td><td>{current_time}</td></tr>
            <tr><td>Final Authority</td><td>{safe_get('final_approver_name')}</td><td>{safe_get('final_approver_title')}</td><td>{current_time}</td></tr>
        </table>
    </div>

    <div style="margin-top: 60px; padding-top: 20px; border-top: 2px solid #ccc; text-align: center; color: #666; font-size: 12px;">
        <p><strong>MOP Generator v2.0</strong> | Generated: {current_time}</p>
    </div>
</body>
</html>"""
        
        return html_content
        
    except Exception as e:
        print(f"Error in generate_safe_html: {e}")
        return f"<html><body><h1>Error generating MOP</h1><p>Error: {str(e)}</p></body></html>"

def generate_device_sections(device_impls, devices_info, image_formatter):
    """Generate device-specific sections safely"""
    try:
        if not device_impls or not devices_info:
            return "<p>No device implementations specified</p>"
        
        html = ""
        for i, (impl, device) in enumerate(zip(device_impls, devices_info)):
            if not impl or not device:
                continue
                
            device_name = device.get('hostname', f'Device {i+1}') or f'Device {i+1}'
            device_type = (device.get('type', 'Unknown') or 'Unknown').title()
            
            html += f"""
            <div class="device-impl-section mb-5 p-4 border rounded" style="page-break-inside: avoid;">
                <h4 class="text-primary">
                    <i class="fas fa-server"></i> {device_type}: {device_name}
                </h4>
                <div class="info-box mb-3">
                    <strong>Device Details:</strong> {device.get('mgmt_ip', 'No IP')} | 
                    {device.get('location', 'No Location')} | 
                    Risk: {(impl.get('risk_level', 'Medium') or 'Medium').title()}
                </div>
                
                <div class="implementation-subsection">
                    <h5 class="text-secondary">
                        <i class="fas fa-clipboard-list"></i> Pre-Implementation Commands
                    </h5>
                    <div class="rich-content">
                        {process_rich_content(impl.get('pre_commands_html', '')) or f"<div class='code-block'>{impl.get('pre_commands', 'No pre-implementation commands specified') or 'No pre-implementation commands specified'}</div>"}
                    </div>
                    <div class="mt-3">
                        <strong>Screenshots & Evidence:</strong>
                        {image_formatter(impl.get('images', {}).get('pre', []) if impl.get('images') else [], 'Pre-Implementation')}
                    </div>
                </div>
                
                <div class="implementation-subsection">
                    <h5 class="text-warning">
                        <i class="fas fa-cogs"></i> Implementation Commands
                    </h5>
                    <div class="rich-content">
                        {process_rich_content(impl.get('impl_commands_html', '')) or f"<div class='code-block'>{impl.get('impl_commands', 'No implementation commands specified') or 'No implementation commands specified'}</div>"}
                    </div>
                    <div class="mt-3">
                        <strong>Screenshots & Evidence:</strong>
                        {image_formatter(impl.get('images', {}).get('impl', []) if impl.get('images') else [], 'Implementation')}
                    </div>
                </div>
                
                <div class="implementation-subsection">
                    <h5 class="text-success">
                        <i class="fas fa-check-circle"></i> Verification Commands
                    </h5>
                    <div class="rich-content">
                        {process_rich_content(impl.get('verify_commands_html', '')) or f"<div class='code-block'>{impl.get('verify_commands', 'No verification commands specified') or 'No verification commands specified'}</div>"}
                    </div>
                    <div class="mt-3">
                        <strong>Verification Results:</strong>
                        {image_formatter(impl.get('images', {}).get('verify', []) if impl.get('images') else [], 'Verification')}
                    </div>
                </div>
                
                <div class="implementation-subsection">
                    <h5 class="text-danger">
                        <i class="fas fa-undo"></i> Rollback Commands
                    </h5>
                    <div class="rich-content">
                        {process_rich_content(impl.get('rollback_commands_html', '')) or f"<div class='code-block'>{impl.get('rollback_commands', 'No rollback commands specified') or 'No rollback commands specified'}</div>"}
                    </div>
                    <div class="mt-3">
                        <strong>Rollback Evidence:</strong>
                        {image_formatter(impl.get('images', {}).get('rollback', []) if impl.get('images') else [], 'Rollback')}
                    </div>
                </div>
                
                <div class="success-box mt-4">
                    <strong><i class="fas fa-info-circle"></i> Implementation Summary:</strong><br>
                    <strong>Duration:</strong> {impl.get('duration', 'Not specified') or 'Not specified'} | 
                    <strong>Engineer:</strong> {impl.get('engineer', 'Not assigned') or 'Not assigned'} | 
                    <strong>Window:</strong> {impl.get('change_window', 'Not specified') or 'Not specified'}<br>
                    <strong>Notes:</strong> {impl.get('implementation_notes', 'No additional notes') or 'No additional notes'}
                </div>
            </div>
            """
        
        return html or "<p>No device implementation data available</p>"
    except Exception as e:
        print(f"Error in generate_device_sections: {e}")
        return "<p>Error formatting device sections</p>"

if __name__ == '__main__':
    port = find_free_port()
    print(f"🚀 MOP Generator starting on port {port}")
    print(f"📱 Access at: http://localhost:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)