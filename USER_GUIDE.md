# 📖 MOP Generator User Guide

Complete step-by-step guide for using the MOP Generator application to create professional Method of Procedure documents.

## 🎯 Getting Started

### **Step 1: Access the Application**
1. Open your web browser
2. Navigate to: **http://localhost:8080** (or your deployed URL)
3. You'll see the MOP Generator interface with multiple tabs

---

## 📋 Creating Your First MOP

### **Tab 1: Document Information**

1. **Document Title**: Enter a descriptive title
   ```
   Example: "Palo Alto Firewall Configuration Update"
   ```

2. **Version**: Document version (default: 1.0)

3. **Category**: Select from dropdown or enter custom
   - Network Change
   - Security Update  
   - System Maintenance
   - Emergency Fix

4. **Priority**: Choose impact level
   - Low, Medium, High, Critical

5. **Execution Details**:
   - **Date**: When the change will be executed
   - **Time**: Start time (24-hour format)
   - **Duration**: Expected duration in minutes

6. **Business Justification**: Explain why this change is needed
   ```
   Example: "Update firewall rules to enhance security posture 
   and comply with new regulatory requirements."
   ```

---

### **Tab 2: Executive Summary**

Write a high-level overview of the change:

```markdown
This MOP outlines the procedure for updating Palo Alto firewall 
configurations to implement new security policies. The change 
affects 3 firewalls in the production environment and will 
improve network security while maintaining service availability.

Key Changes:
• Update security policies for new application access
• Implement enhanced logging for compliance
• Configure NAT rules for new service deployment
```

**💡 Tip**: Use the rich text editor to format your summary with:
- **Bold** for important points
- *Italic* for emphasis  
- Bullet points for lists
- Code blocks for technical details

---

### **Tab 3: Technical Configuration**

#### **Device Inventory**
1. Click **"Add Device"** to add each device involved
2. Fill in device details:
   - **Device Name**: `FW-01-Primary`
   - **Management IP**: `192.168.1.10`
   - **Location**: `Data Center A - Rack 15`
   - **Device Type**: `Palo Alto PA-5220`

3. Repeat for all devices involved in the change

#### **Network Configuration**  
1. Click **"Add Network Config"** for each IP/zone mapping
2. Configure network details:
   - **Real IP**: `10.10.10.100`
   - **NAT IP**: `203.0.113.100` 
   - **Palo Alto Zone**: `DMZ-Web-Servers`
   - **VLAN ID**: `100`
   - **Description**: Purpose of this network segment

**💡 Tip**: Add all networks that will be affected by the change

---

### **Tab 4: Risk Assessment**

#### **Adding Technical Risks**
1. Click **"Add Technical Risk"**
2. Fill in risk details:
   - **Risk Description**: 
     ```
     Configuration error could block legitimate traffic
     ```
   - **Impact Score**: 1-5 (5 = Severe impact)
   - **Probability**: 1-5 (5 = Very likely)
   - **Risk Score**: Automatically calculated (Impact × Probability)
   - **Mitigation Plan**: 
     ```
     • Test configuration in lab environment first
     • Have rollback configuration ready
     • Monitor traffic during implementation
     ```
   - **Contingency Plan**:
     ```
     • Immediately rollback to previous configuration
     • Contact network team for emergency support
     • Activate backup network path if needed
     ```

#### **Adding Business Risks**
1. Click **"Add Business Risk"**
2. Consider business impacts:
   - Service downtime
   - Data availability
   - Compliance issues
   - Customer impact

**💡 Tip**: Higher risk scores (15+) require additional approvals

---

### **Tab 5: Implementation Steps**

#### **Auto-Generate Device Forms**
1. After adding devices in Tab 3, click **"Refresh Device List"**
2. The system generates implementation forms for each device

#### **For Each Device, Fill In:**

**Pre-Implementation Steps**:
```bash
# Example commands
show system info
show interface all
show route
```
- Use rich text editor for formatting
- Add screenshots of current state
- Upload network diagrams

**Implementation Commands**:
```bash
# Enter configuration mode
configure

# Add new security policy
set rulebase security rules "Allow-Web-Traffic" from DMZ-Web-Servers
set rulebase security rules "Allow-Web-Traffic" to Internet-Zone  
set rulebase security rules "Allow-Web-Traffic" source 10.10.10.0/24
set rulebase security rules "Allow-Web-Traffic" destination any
set rulebase security rules "Allow-Web-Traffic" application web-browsing
set rulebase security rules "Allow-Web-Traffic" action allow

# Commit changes
commit
```

**Verification Steps**:
```bash
# Verify new rule is active
show rulebase security rules "Allow-Web-Traffic"

# Test connectivity
ping source 10.10.10.100 host 8.8.8.8

# Check logs
show log traffic recent
```

**Rollback Procedures**:
```bash
# If issues occur, rollback immediately
configure
delete rulebase security rules "Allow-Web-Traffic"
commit
```

#### **Image Upload Tips**:
- **Drag & Drop**: Drag images directly into text areas
- **Paste**: Copy screenshots and press Ctrl+V
- **Click Upload**: Use the upload button for file selection
- **Add Borders**: Click on inserted images to add professional borders

---

### **Tab 6: Rollback Procedures**

#### **Rollback Triggers**
Define what conditions trigger a rollback:
- Service unavailable for > 5 minutes
- Critical applications cannot connect
- Security alerts indicate compromise
- Performance degradation > 50%

#### **Rollback Steps**
1. **Immediate Actions** (0-5 minutes):
   ```bash
   # Emergency rollback
   configure
   load config saved "pre-change-backup.xml"
   commit force
   ```

2. **Verification** (5-10 minutes):
   - Test critical services
   - Verify network connectivity
   - Check application functionality

3. **Notification** (10-15 minutes):
   - Notify change management team
   - Update incident ticket
   - Communicate to stakeholders

---

### **Tab 7: Approval Signatures**

#### **Add Approvers**
1. Click **"Add Approval Signature"**
2. Configure approval levels:
   - **Level 1**: Technical Lead
   - **Level 2**: Network Manager  
   - **Level 3**: IT Director (for high-risk changes)

3. For each approver:
   - **Name**: John Smith
   - **Role**: Senior Network Engineer
   - **Level**: 1 (Primary approval)
   - **Status**: Pending/Approved/Rejected

**💡 Tip**: Higher risk scores automatically require additional approval levels

---

## 🎨 Advanced Features

### **Rich Text Editing**
- **Formatting**: Use toolbar for bold, italic, underline
- **Code Blocks**: Perfect for command sequences  
- **Lists**: Bullet points and numbered lists
- **Links**: Add references to documentation
- **Tables**: Structure data clearly

### **Image Management**
- **Professional Screenshots**: Add borders and shadows
- **Network Diagrams**: Upload topology diagrams
- **Before/After Shots**: Document the change visually
- **Error Screenshots**: Include for troubleshooting

### **Auto-Save Feature**
- Your work is automatically saved every 30 seconds
- Data persists even if browser is closed
- No need to manually save while working

---

## 📄 Generating the Final MOP

### **Step 1: Review All Tabs**
Go through each tab and ensure all information is complete:
- ✅ Document information filled
- ✅ Executive summary written  
- ✅ Technical configuration complete
- ✅ Risks assessed and mitigated
- ✅ Implementation steps detailed
- ✅ Rollback procedures defined
- ✅ Approvals configured

### **Step 2: Generate Document**
1. Click **"Generate Complete MOP Document"**
2. Wait for processing (usually 5-10 seconds)
3. Review the success message

### **Step 3: Download**
1. Click the **HTML download link**
2. Save the professional MOP document
3. The document includes:
   - All your content with rich formatting
   - Embedded images (no external dependencies)
   - Professional styling for presentations
   - Print-friendly layout

---

## 💡 Best Practices

### **Documentation**
- ✅ **Be Specific**: Include exact commands and expected outputs
- ✅ **Add Context**: Explain why each step is necessary  
- ✅ **Include Screenshots**: Visual confirmation of steps
- ✅ **Test Procedures**: Verify all steps in lab first

### **Risk Management**
- ✅ **Identify All Risks**: Technical, business, operational
- ✅ **Realistic Scoring**: Don't underestimate impact/probability
- ✅ **Detailed Mitigation**: Specific steps to reduce risks
- ✅ **Clear Triggers**: Define exactly when to rollback

### **Implementation**
- ✅ **Logical Order**: Steps should flow naturally
- ✅ **Checkpoint Verification**: Verify success at each major step
- ✅ **Time Estimates**: Include realistic time for each phase
- ✅ **Resource Requirements**: List all tools/access needed

### **Quality Assurance**
- ✅ **Peer Review**: Have colleagues review before execution
- ✅ **Lab Testing**: Test all procedures in non-production
- ✅ **Backup Plans**: Always have a way back
- ✅ **Communication Plan**: Keep stakeholders informed

---

## 🔧 Troubleshooting

### **Common Issues**

**Rich Editor Not Loading**:
- Refresh the page
- Check browser console for errors
- Try a different browser

**Images Not Uploading**:
- Check file size (max 16MB)
- Ensure file format is supported (PNG, JPG, GIF)
- Try refreshing the page

**Form Data Lost**:
- Check browser local storage
- Data should auto-restore on page refresh
- Use latest browser version

**Generate Button Not Working**:
- Ensure all required fields are filled
- Check browser console for errors
- Try generating again after a few seconds

---

## 📞 Need Help?

- **Documentation**: Check [README.md](README.md) for setup help
- **Docker Issues**: See [DOCKER.md](DOCKER.md) for container problems  
- **Deployment**: Review [DEPLOYMENT.md](DEPLOYMENT.md) for hosting options
- **Issues**: Report bugs on [GitHub Issues](https://github.com/damarajibri/mop-generator/issues)

**🎯 You're now ready to create professional MOP documents with confidence!**