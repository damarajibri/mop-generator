# MOP Generator - Professional Method of Procedure Builder

A comprehensive web-based application for creating professional Method of Procedure (MOP) documents with advanced text editing, image capture, and technical configuration management capabilities.

## 🚀 Features

### Core Functionality
- **Rich Text Editor**: Quill.js-powered editors with image support, code blocks, and formatting
- **Image Management**: Upload, paste (Ctrl+V), drag & drop with custom borders
- **Device-Based Implementation**: Dynamic forms based on configured devices
- **Professional Export**: Clean HTML documents with embedded images
- **Resizable Editors**: Flexible text areas for better user experience

### MOP Sections
1. **Document Information** - Basic document metadata
2. **Executive Summary** - High-level overview and parameters
3. **Technical Configuration** - Device inventory and network setup
4. **Risk Assessment** - Technical and business risk analysis
5. **Implementation Steps** - Device-specific commands with rich formatting
6. **Rollback Procedures** - Emergency rollback plans
7. **Approval Signatures** - Multi-level approval workflow

### Advanced Features
- **Palo Alto Zone Support** - Security zone configuration for firewalls
- **IP & Zone Management** - Real IP, NAT IP with zone mapping
- **Image Border Tool** - Custom borders for screenshots in editors
- **Auto-save** - Prevents data loss with local storage backup
- **Responsive Design** - Works on desktop and mobile devices

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Flask 2.3+
- Modern web browser

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/mop-generator.git
cd mop-generator

# Install dependencies
pip install Flask==2.3.2 Werkzeug==2.3.6 Pillow==10.0.1

# Run the application
python3 app.py
```

The application will automatically find an available port and display the access URL.

## 📁 Project Structure

```
mop-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
├── uploads/              # Image storage
└── generated_mops/       # Generated MOP documents
```

## 🎯 Usage

### 1. Document Configuration
- Fill in basic document information (title, version, category)
- Add executive summary with execution timeline

### 2. Technical Setup
- **Device Inventory**: Add devices with management IPs and locations
- **Network Configuration**: Configure IP addresses with Palo Alto zones
- **VLAN Setup**: Map VLANs to security zones

### 3. Risk Assessment
- Add technical and business risks with impact/probability scoring
- Define mitigation strategies and contingency plans

### 4. Implementation
- Click "Refresh Device List" to generate device-specific forms
- Use rich text editors to add formatted commands
- Upload screenshots directly or paste images (Ctrl+V)
- Add custom borders to images for better documentation

### 5. Generate MOP
- Click "Generate Complete MOP Document"
- Download professional HTML document with embedded images

## 🖼️ Image Features

### Upload Methods
- **Click to Browse**: Traditional file selection
- **Drag & Drop**: Drag images directly to upload areas
- **Paste (Ctrl+V)**: Copy and paste images from clipboard
- **Rich Editor**: Insert images directly in text editors

### Image Borders
1. Insert image in rich text editor
2. Click on the image to select it
3. Click the border tool in toolbar
4. Choose border style, width, color, and radius
5. Apply changes

## ⚙️ Configuration

### Environment Variables
```bash
FLASK_SECRET_KEY=your-secret-key
MAX_CONTENT_LENGTH=16777216  # 16MB default
UPLOAD_FOLDER=uploads
```

### Supported Image Formats
- PNG, JPG, JPEG, GIF, WebP
- Maximum file size: 16MB per image

## 🔒 Security Features

- Secure filename handling with UUID prefixes
- File type validation for uploads
- XSS protection in generated HTML
- Safe base64 image embedding

## 🚧 Troubleshooting

### Port Conflicts
The application automatically finds an available port. If you need a specific port:
```python
# Edit app.py, line ~480
app.run(debug=False, host='0.0.0.0', port=5000)  # Change port here
```

### Rich Editor Not Working After Refresh
This is a known issue that has been fixed in the latest version. The editor properly reinitializes with content preservation.

### Images Not Showing in Generated HTML
Images are automatically converted to base64 and embedded in the HTML for portability.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Quill.js** - Rich text editing capabilities
- **Bootstrap 5** - Modern UI framework
- **Font Awesome** - Professional icons
- **Flask** - Python web framework

## 📞 Support

For issues and questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/mop-generator/issues)
3. Create a new issue with detailed information

## 🎨 Screenshots

### Main Interface
![Main Interface](docs/screenshots/main-interface.png)

### Rich Text Editor
![Rich Text Editor](docs/screenshots/rich-editor.png)

### Generated MOP Document
![Generated MOP](docs/screenshots/generated-mop.png)

---

**Built with ❤️ for network engineers and system administrators**