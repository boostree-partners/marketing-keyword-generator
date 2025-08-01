# 🚀 Keyword Generator - Installation Guide

A comprehensive guide for installing and using the Keyword Generator application.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Methods](#installation-methods)
4. [Usage Guide](#usage-guide)
5. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 🪟 **Windows Users**

1. Download `keyword_generator_windows_vX.X.X.zip`
2. Extract the ZIP file
3. Double-click `keyword_generator.exe`
4. Browser will open automatically → Upload Excel file

### 🍎 **macOS Users**

1. Download `keyword_generator_macos_vX.X.X.zip`
2. Extract the ZIP file
3. Double-click `keyword_generator.app`
4. Browser will open automatically → Upload Excel file

---

## System Requirements

### **Minimum Requirements**

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 (Mojave) or later
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Internet**: Not required (runs locally)

### **Supported File Formats**

- Excel files: `.xlsx`, `.xls`
- Browser: Chrome, Firefox, Safari, Edge

---

## Installation Methods

### Method 1: Download Pre-built Executable (Recommended)

#### **From GitHub Releases**

1. Go to [Releases page](https://github.com/your-repo/keyword-generator/releases)
2. Download the latest version for your OS:
   - Windows: `keyword_generator_windows_vX.X.X.zip`
   - macOS: `keyword_generator_macos_vX.X.X.zip`
3. Extract and run

#### **From GitHub Actions**

1. Go to [Actions tab](https://github.com/your-repo/keyword-generator/actions)
2. Click on latest "Build Cross-Platform Executables"
3. Download from Artifacts section

### Method 2: Build from Source

```bash
# Clone repository
git clone https://github.com/your-repo/keyword-generator.git
cd keyword-generator

# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run web application
make web
# Or: streamlit run src/streamlit_app.py

# Build executable (use GitHub Actions - recommended)
make build  # Shows GitHub Actions usage guide
```

---

## Usage Guide

### 🎯 **Step-by-Step Usage**

#### 1. **Launch Application**

- **Windows**: Double-click `keyword_generator.exe`
- **macOS**: Double-click `keyword_generator.app`
- Wait for browser to open automatically

#### 2. **Upload Excel File**

- Click "Browse files" or drag & drop
- Supported format: Excel file with keyword combination rules
- File should have this structure:
  ```
  Row 1: [Combination Rule] [Group] [2] [3] [4] ... [N]        ← Column numbers
  Row 2: [Combination Rule] [Group] [Brand] [General] ... [CategoryN] ← Category titles
  Row 3+: [2,3,4] [SEO] [keyword1] [keyword2] ... [keywordN]   ← Actual data
  ```

#### 3. **Generate Keywords**

- Click "🔥 Start Keyword Combination Generation"
- Wait for processing (may take a few minutes for large files)
- View statistics and preview results

#### 4. **Download Results**

- Use group filter to preview specific groups
- Adjust number of rows to display
- Click "📁 Download Excel File" to get results
- Results include:
  - **Dashboard sheet**: Statistics and summary
  - **Group sheets**: Keywords organized by group

### 🎮 **Example Usage**

```excel
Excel Input:
A1: "2,3,4"    B1: "SEO"      C1: 2    D1: 3    E1: 4
A2: "조합규칙"   B2: "그룹"     C2: "브랜드" D2: "일반" E2: "가격"
A3: "2,3,4"    B3: "SEO"      C3: "clinic" D3: "beauty" E3: "cheap"
A4: "2,3"      B4: "Main"     C4: "spa"    D4: "facial" E4: "premium"

Output:
- SEO group: "clinic beauty cheap", "spa beauty cheap", etc.
- Main group: "clinic beauty", "spa beauty", etc.
```

---

## Troubleshooting

### 🛠️ **Common Issues**

#### **1. Application won't start**

**Windows:**

```cmd
# Check if blocked by Windows Defender
Right-click exe → Properties → General → Unblock

# Run as Administrator
Right-click exe → Run as administrator
```

**macOS:**

```bash
# Allow unsigned application
System Preferences → Security & Privacy → General → Allow apps downloaded from: Anywhere

# Or use command line
sudo spctl --master-disable
```

#### **2. Browser doesn't open automatically**

- Manually open browser and go to: `http://localhost:8501`
- Check if port 8501 is available
- Try different browser

#### **3. File upload fails**

- Check file format (must be .xlsx or .xls)
- Ensure file is not corrupted
- Try with smaller file first

#### **4. "Out of memory" error**

- Close other applications
- Try smaller Excel file
- Restart application

#### **5. Generated file is empty**

- Check Excel file structure
- Ensure combination rules refer to existing column numbers
- Verify data rows have content

### 🔧 **Advanced Troubleshooting**

#### **Check Application Logs**

- **Windows**: Look for console window messages
- **macOS**: Check Console.app for error messages

#### **Port Conflicts**

```bash
# Check if port 8501 is in use
netstat -an | grep 8501

# Kill process using port (if needed)
# Windows: taskkill /PID [PID_NUMBER] /F
# macOS: kill -9 [PID_NUMBER]
```

#### **Permission Issues**

```bash
# Windows: Run Command Prompt as Administrator
# macOS: Grant Full Disk Access in System Preferences
```

---

## 📞 **Support**

### **Getting Help**

- 📧 **Issues**: [GitHub Issues](https://github.com/your-repo/keyword-generator/issues)
- 📖 **Documentation**: [README.md](README.md)
- 🔨 **Build Guide**: [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)

### **Reporting Bugs**

When reporting bugs, please include:

1. Operating system and version
2. Application version
3. Steps to reproduce
4. Error messages (screenshots helpful)
5. Sample Excel file (if relevant)

### **Feature Requests**

- Use GitHub Issues with "enhancement" label
- Describe use case and expected behavior
- Provide examples if applicable

---

## 🎉 **Tips for Best Experience**

### **Excel File Preparation**

- Keep column numbers consecutive (2, 3, 4, 5...)
- Use clear category names in row 2
- Avoid empty cells in data rows
- Test with small file first

### **Performance Optimization**

- Close unnecessary browser tabs
- Use smaller combination rules for large datasets
- Regularly restart application for large batches

### **Backup Recommendations**

- Keep original Excel files safe
- Save generated results with timestamp
- Use descriptive filenames for outputs

---

## 📊 **File Size Guidelines**

| File Size | Rows   | Expected Processing Time | Memory Usage |
| --------- | ------ | ------------------------ | ------------ |
| Small     | <50    | <30 seconds              | <100MB       |
| Medium    | 50-200 | 1-5 minutes              | 100-500MB    |
| Large     | >200   | 5+ minutes               | >500MB       |

---

## 🔄 **Updates**

### **Checking for Updates**

- Visit [Releases page](https://github.com/your-repo/keyword-generator/releases)
- Download latest version
- No automatic update mechanism (manual download required)

### **Changelog**

- See [CHANGELOG.md](CHANGELOG.md) for version history
- Check release notes for new features and bug fixes

---

**🎯 Ready to generate thousands of keyword combinations? Let's get started!**
