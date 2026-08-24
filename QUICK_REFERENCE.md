# 🚀 MOP Generator - Quick Reference

Quick reference card for common tasks and shortcuts in MOP Generator.

## 📋 Tab-by-Tab Checklist

### ✅ **Tab 1: Document Info**
- [ ] Document title and version
- [ ] Category and priority level  
- [ ] Execution date/time/duration
- [ ] Business justification

### ✅ **Tab 2: Executive Summary**  
- [ ] High-level change overview
- [ ] Key impacts and benefits
- [ ] Stakeholder communication

### ✅ **Tab 3: Technical Config**
- [ ] Add all devices involved
- [ ] Configure network IPs and zones
- [ ] Map VLANs to security zones

### ✅ **Tab 4: Risk Assessment**
- [ ] Technical risks identified
- [ ] Business risks documented  
- [ ] Mitigation plans defined
- [ ] Contingency procedures ready

### ✅ **Tab 5: Implementation**
- [ ] Click "Refresh Device List"
- [ ] Fill pre-implementation steps
- [ ] Detail implementation commands
- [ ] Define verification steps
- [ ] Document rollback procedures

### ✅ **Tab 6: Rollback**
- [ ] Rollback triggers defined
- [ ] Emergency procedures documented
- [ ] Verification steps included

### ✅ **Tab 7: Approvals**
- [ ] All required approvers added
- [ ] Approval levels configured
- [ ] Signatures obtained

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Paste image | `Ctrl + V` |
| Bold text | `Ctrl + B` |
| Italic text | `Ctrl + I` |
| Save (auto) | Every 30 seconds |
| Code block | Select text + Code button |

---

## 🖼️ Image Quick Tips

### **Upload Methods**
- **Drag & Drop**: Drag image files directly
- **Paste**: `Ctrl + V` for screenshots  
- **Click**: Use upload buttons
- **Rich Editor**: Insert directly in text

### **Image Borders**
1. Click on inserted image
2. Click border tool in toolbar
3. Choose style, width, color
4. Apply changes

---

## 🎯 Risk Scoring Guide

| Score | Impact | Probability |
|-------|---------|-------------|
| **1** | Minimal | Very unlikely |
| **2** | Minor | Unlikely |
| **3** | Moderate | Possible |
| **4** | Major | Likely |
| **5** | Severe | Very likely |

**Risk Level = Impact × Probability**
- **1-6**: Low risk (standard approval)
- **7-14**: Medium risk (manager approval)
- **15-25**: High risk (director approval)

---

## 🔧 Common Commands Examples

### **Pre-Implementation**
```bash
# System status check
show system info
show interface all  
show route summary
show session info
```

### **Implementation**
```bash
# Enter config mode
configure

# Make changes
set [configuration commands]

# Commit changes  
commit
exit
```

### **Verification**
```bash
# Verify changes
show [relevant commands]
test connectivity
ping source [ip] host [target]
```

### **Rollback**
```bash
# Emergency rollback
configure
rollback to running-config.backup
commit force
```

---

## 🚨 Emergency Checklist

### **If Something Goes Wrong:**
1. **Stop immediately** - Don't continue if unexpected behavior
2. **Check status** - Verify current system state  
3. **Rollback decision** - Use predefined triggers
4. **Execute rollback** - Follow documented procedures
5. **Verify restoration** - Confirm services are restored
6. **Notify stakeholders** - Communication is critical

### **Rollback Triggers**
- Service down > 5 minutes
- Critical application failure
- Security alerts triggered  
- Performance degradation > 50%
- Unexpected system behavior

---

## 📞 Quick Help

### **Browser Issues**
- **Rich editor not loading**: Refresh page
- **Images won't upload**: Check file size < 16MB
- **Form data lost**: Should auto-restore on refresh

### **Application Issues**  
- **Generate button not working**: Fill all required fields
- **Slow performance**: Try refreshing browser
- **Can't save**: Check browser local storage

### **Best Practices**
- ✅ Test in lab first
- ✅ Have rollback ready  
- ✅ Monitor during change
- ✅ Document everything
- ✅ Communicate status

---

## 🎨 Formatting Quick Guide

### **Rich Text Editor**
- **Headers**: Use H1, H2, H3 for structure
- **Code blocks**: Perfect for command sequences
- **Lists**: Bullet points and numbered steps  
- **Tables**: Organize data clearly
- **Links**: Reference documentation

### **Professional Writing**
- Use **bold** for important items
- Use *italic* for emphasis
- Use `code` for commands/filenames
- Use > blockquotes for warnings
- Use --- for section breaks

---

## 📊 File Export

### **Generate MOP**
1. Review all tabs for completeness
2. Click "Generate Complete MOP Document"
3. Download HTML file
4. Document includes:
   - Rich formatting preserved
   - Images embedded (no external files)
   - Professional styling  
   - Print-friendly layout

### **File Formats**
- **HTML**: Primary output format
- **Images**: Automatically embedded as base64
- **Styling**: Professional CSS included
- **Portability**: Self-contained file

---

**💡 Remember: Professional MOPs save time, reduce errors, and ensure successful changes!**

**📚 For detailed instructions: [USER_GUIDE.md](USER_GUIDE.md)**