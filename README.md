# Keyword Generator 🚀

A CLI tool that automatically generates keyword combinations based on rules defined in Excel files.

## 📖 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Excel File Format](#excel-file-format)
- [Output Format](#output-format)
- [Build & Distribution](#build--distribution)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- 🔥 **Excel-based keyword generation**: Generate thousands of keyword combinations from Excel files
- 🌐 **Browser-based UI**: User-friendly web interface using Streamlit
- 📊 **Real-time statistics**: View generation progress and results
- 📁 **Group-based organization**: Organize keywords by groups with separate Excel sheets
- 🔄 **Flexible file sizes**: Support for various Excel file sizes (3+ rows, 3+ columns)
- 📦 **Cross-platform executables**: Available for both Windows and macOS
- 🚀 **Multiple interfaces**: CLI, web app, and standalone executable options

## 🚀 Quick Start

### Method 1: Download Executable (Recommended)

1. Download the latest release for your platform:
   - **Windows**: `keyword_generator_windows_vX.X.X.zip`
   - **macOS**: `keyword_generator_macos_vX.X.X.zip`
2. Extract and double-click the executable
3. Upload your Excel file in the browser
4. Generate and download keyword combinations

### Method 2: Run from Source

```bash
# Clone repository
git clone https://github.com/your-repo/keyword-generator.git
cd keyword-generator

# Setup environment
make setup

# Run web application
make web
```

## 📁 Project Structure

```
keyword-generator/
├── src/
│   ├── resources/
│   │   ├── sample_keywords.xlsx           # Sample data file
│   │   └── test.xlsx                      # Test file
│   ├── output/                            # Generated keyword files
│   ├── keyword_generator.py               # Main script
│   ├── streamlit_app.py                   # Web UI
│   └── launcher.py                        # Executable launcher
├── .github/workflows/
│   └── build-executables.yml             # Auto-build configuration
├── venv/                                  # Python virtual environment
├── Makefile                               # CLI commands
├── build_executable.py                    # Build script
├── requirements.txt                       # Dependencies
├── INSTALLATION_GUIDE.md                 # User guide
├── WINDOWS_BUILD_GUIDE.md                # Build guide
└── README.md                             # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Commands

```bash
# Basic setup
make setup

# Development setup
make dev-setup

# Clean install
make clean && make setup
```

## 📖 Usage

### Web Application (Recommended)

```bash
# Start web application
make web

# Or manually
streamlit run src/streamlit_app.py
```

### Command Line Interface

```bash
# Basic usage with default files
make run

# Specify input file
make file FILE=path/to/your/file.xlsx

# Specify output directory
make output DIR=path/to/output

# Custom input and output
make custom INPUT=data.xlsx OUTPUT=results/
```

### Available Commands

```bash
make help        # Show all available commands
make examples    # Show usage examples
make test        # Run basic tests
make clean       # Clean temporary files
make build       # Build executable
make build-info  # Show build environment info
```

## 📊 Excel File Format

Your Excel file should follow this structure:

### Required Format

```
Row 1: [Rule] [Group] [2] [3] [4] ... [N]           ← Column numbers
Row 2: [Rule] [Group] [Brand] [General] ... [Cat]   ← Category titles
Row 3: [2,3,4] [SEO] [clinic] [beauty] [cheap]      ← Actual data
Row 4: [2,3] [Main] [spa] [facial] [premium]        ← More data
...
```

### Example

| A (Rule) | B (Group) | C (Brand) | D (General) | E (Price)  |
| -------- | --------- | --------- | ----------- | ---------- |
| 2,3,4    | SEO       | clinic    | beauty      | cheap      |
| 2,3      | Main      | spa       | facial      | premium    |
| 2,4      | Budget    | center    | treatment   | affordable |

### Rules

- **Column A**: Combination rules (e.g., "2,3,4" means combine columns C, D, E)
- **Column B**: Group names for organization
- **Columns C+**: Keyword categories and values
- **Row 1**: Column reference numbers (2, 3, 4, ...)
- **Row 2**: Category names (Brand, General, Price, ...)
- **Row 3+**: Actual keyword data

## 📋 Output Format

### Generated Files

The tool creates Excel files with multiple sheets:

#### Dashboard Sheet

- Total keyword count
- Group statistics
- Generation timestamp
- Rule summaries

#### Group Sheets

- Separate sheet for each group (SEO, Main, Budget, etc.)
- Columns: Rule, Group, Categories, Keyword, Components
- Filtered data for easy analysis

### Example Output

```
keyword_combinations_20241201_143022.xlsx
├── Dashboard          # Statistics and summary
├── SEO               # SEO group keywords
├── Main              # Main group keywords
└── Budget            # Budget group keywords
```

## 🔨 Build & Distribution

### 🚀 GitHub Actions (Recommended)

All builds are handled by GitHub Actions for consistency across platforms:

#### **Automatic Release Builds**

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# 1. Build Windows .exe and macOS .app
# 2. Create release packages
# 3. Publish to GitHub Releases
```

#### **Manual Builds**

```bash
# Go to GitHub repository
# → Actions tab
# → "Build Cross-Platform Executables"
# → "Run workflow" button
# → Download from Artifacts section
```

#### **Local Build Info**

```bash
# Check build environment and get GitHub Actions guidance
make build-info

# Show GitHub Actions usage instructions
make build
```

### Build Results

- **Windows**: `KeywordGenerator.exe` (standalone executable)
- **macOS**: `KeywordGenerator.app` (application bundle)
- **Packages**: `keyword_generator_windows_vX.X.X.zip` and `keyword_generator_macos_vX.X.X.zip`
- **Documentation**: Included installation guides and sample files

## 🔧 System Requirements

### Minimum Requirements

- **OS**: Windows 10+ or macOS 10.14+
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge

### Performance Guidelines

| File Size | Rows   | Processing Time | Memory Usage |
| --------- | ------ | --------------- | ------------ |
| Small     | <50    | <30 seconds     | <100MB       |
| Medium    | 50-200 | 1-5 minutes     | 100-500MB    |
| Large     | >200   | 5+ minutes      | >500MB       |

## 🛠️ Troubleshooting

### Common Issues

#### "File not found" error

```bash
# Check file path
ls -la path/to/file.xlsx

# Use absolute path
make file FILE=/absolute/path/to/file.xlsx
```

#### Empty output

- Verify Excel file format
- Check combination rules reference existing columns
- Ensure data rows have content

#### Memory issues

- Close other applications
- Use smaller files for testing
- Restart application between large files

#### Permission errors (macOS)

```bash
# Allow unsigned applications
sudo spctl --master-disable

# Or right-click app → Open
```

#### Antivirus false positive (Windows)

- Add executable to antivirus exceptions
- Windows Defender → Virus & threat protection → Exclusions

### Getting Help

- 📧 [GitHub Issues](https://github.com/your-repo/keyword-generator/issues)
- 📖 [Installation Guide](INSTALLATION_GUIDE.md)
- 🔨 [Build Guide](WINDOWS_BUILD_GUIDE.md)

## 🔄 Development

### Contributing

```bash
# Fork repository
# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
make test

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Create Pull Request
```

### Testing

```bash
# Run basic tests
make test

# Test with sample file
make file FILE=src/resources/sample_keywords.xlsx

# Clean and test
make clean && make setup && make test
```

## 📝 Changelog

### Latest Changes

- ✨ Cross-platform executable support
- 🌐 Browser-based user interface
- 📊 Real-time statistics and preview
- 🔄 Flexible file size support
- 📁 Group-based Excel organization

### Version History

See [GitHub Releases](https://github.com/your-repo/keyword-generator/releases) for detailed version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Usage Examples

### Business Use Cases

- **SEO keyword research**: Generate variations for search optimization
- **Ad campaign creation**: Create keyword combinations for advertising
- **Content planning**: Generate topic variations for content creation
- **Market research**: Analyze keyword combinations for different segments

### Sample Workflow

1. **Prepare Excel file** with your keyword categories
2. **Define combination rules** (which categories to combine)
3. **Run the generator** via web interface or CLI
4. **Download results** organized by groups
5. **Use generated keywords** in your projects

---

**🚀 Ready to generate thousands of keyword combinations? Get started with the [Quick Start](#quick-start) guide!**
