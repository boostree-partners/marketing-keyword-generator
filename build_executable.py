#!/usr/bin/env python3
"""
Keyword Generator Executable Build Script
Build executables for both macOS and Windows platforms

🚀 **Primary Usage: GitHub Actions**
This script is primarily designed to run in GitHub Actions for automated 
cross-platform builds. For manual builds, use GitHub Actions instead:

📍 Automatic builds:
   git tag v1.0.0 && git push origin v1.0.0

📍 Manual builds:
   GitHub → Actions → "Build Cross-Platform Executables" → Run workflow

🛠️ Local development testing only:
   python build_executable.py
"""

import os
import sys
import shutil
import platform
import subprocess
from datetime import datetime

def run_command(cmd, description):
    """Execute command and output results"""
    print(f"\n🔧 {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def cleanup_build():
    """Clean up previous build files"""
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            print(f"🧹 Cleaning {folder} folder...")
            shutil.rmtree(folder)

def create_spec_file():
    """Create platform-specific spec file"""
    current_platform = platform.system()
    
    if current_platform == "Darwin":  # macOS
        app_name = "KeywordGenerator"
        console_mode = True
        create_bundle = True
    else:  # Windows
        app_name = "KeywordGenerator"
        console_mode = True
        create_bundle = False
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
"""
Keyword Generator PyInstaller Configuration File ({current_platform})
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files

# Application configuration
app_name = "{app_name}"
main_script = "src/launcher.py"

# Collect Streamlit data files
streamlit_data = collect_data_files('streamlit')

# Additional data files
datas = [
    ('src/resources', 'resources'),
    ('src/streamlit_app.py', 'src'),
    ('src/keyword_generator.py', 'src'),
] + streamlit_data

# Add output directory only if it exists
if os.path.exists('src/output'):
    datas.append(('src/output', 'output'))

# Hidden imports for Streamlit
hiddenimports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.state',
    'streamlit.components.v1',
    'pandas',
    'openpyxl',
    'xlrd',
    'numpy',
    'itertools',
    'io',
    'datetime',
    'os',
    'sys',
    'subprocess',
    'time',
    'threading',
    'psutil',
    'webbrowser'
]

# Binary excludes
excludes = [
    'matplotlib',
    'scipy',
    'sklearn',
    'tensorflow',
    'torch',
    'cv2'
]

block_cipher = None

a = Analysis(
    [main_script],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={str(console_mode)},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)'''

    # Add macOS app bundle configuration
    if create_bundle:
        spec_content += f'''

app = BUNDLE(
    exe,
    name='{app_name}.app',
    icon=None,
    bundle_identifier=None,
    info_plist={{
        'CFBundleDisplayName': '{app_name}',
        'CFBundleName': '{app_name}',
        'NSHumanReadableCopyright': '© 2024 Keyword Generator',
        'LSUIElement': True  # Hide from dock and menu bar
    }}
)'''

    # Write spec file
    spec_filename = f"{app_name.lower()}.spec"
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Created spec file: {spec_filename}")
    return spec_filename

def main():
    """Main build function"""
    print("=" * 70)
    print("🚀 Keyword Generator Executable Build")
    print("=" * 70)
    
    # Check platform
    current_platform = platform.system()
    print(f"📱 Platform: {current_platform}")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return 1
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"📦 PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller is not installed!")
        print("   Please run: pip install pyinstaller")
        return 1
    
    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    cleanup_build()
    
    # Create spec file
    spec_file = create_spec_file()
    
    # Build command
    build_cmd = ['pyinstaller', '--clean', '--noconfirm', spec_file]
    
    if not run_command(build_cmd, "Building executable"):
        return 1
    
    # Check build results
    print("\n📊 Build Results:")
    
    if os.path.exists('dist'):
        for item in os.listdir('dist'):
            item_path = os.path.join('dist', item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path) / 1024 / 1024  # MB
                print(f"   📄 {item}: {size:.1f} MB")
            elif os.path.isdir(item_path):
                print(f"   📁 {item}/")
    
    # Check if running in CI/CD environment
    is_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'
    
    if not is_ci:
        # Test execution option (only in interactive environment)
        print("\n🧪 Would you like to test the built executable?")
        try:
            test_choice = input("   y/n (default: n): ").strip().lower()
            
            if test_choice == 'y':
                current_platform = platform.system()
                if current_platform == "Darwin":
                    test_cmd = ['open', 'dist/KeywordGenerator.app']
                else:
                    test_cmd = ['dist/KeywordGenerator.exe']
                
                run_command(test_cmd, "Testing execution")
                print("   Please return to terminal after testing to continue")
        except (EOFError, KeyboardInterrupt):
            print("   Skipping test (non-interactive environment)")
        
        # Distribution package creation option (only in interactive environment)
        print("\n📦 Would you like to create a distribution package?")
        try:
            package_choice = input("   y/n (default: n): ").strip().lower()
            
            if package_choice == 'y':
                create_distribution_package()
        except (EOFError, KeyboardInterrupt):
            print("   Skipping package creation (non-interactive environment)")
    else:
        print("\n🤖 CI/CD environment detected - skipping interactive prompts")
    
    print("\n" + "=" * 70)
    print("🎉 Build Complete!")
    print("=" * 70)
    print(f"📁 Results location: {os.path.abspath('dist')}")
    
    if is_ci:
        print("🤖 CI/CD Build Summary:")
        print("   ✅ Executable built successfully")
        print("   📦 Ready for GitHub Actions artifact upload")
        print("   🚀 Will be packaged in GitHub Release")
    else:
        print("📋 Next steps:")
        print("   1. Test executable in dist/ folder")
        print("   2. Distribute to users")
        print("   3. Provide INSTALLATION_GUIDE.md document")
    
    print("=" * 70)
    
    return 0

def create_distribution_package():
    """Create distribution package"""
    print("\n📦 Creating distribution package...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"keyword_generator_{platform.system().lower()}_{timestamp}"
    package_dir = f"package/{package_name}"
    
    # Create package directory
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy executable
    if platform.system() == "Darwin":
        shutil.copytree('dist/KeywordGenerator.app', f'{package_dir}/KeywordGenerator.app')
        shutil.copy('dist/KeywordGenerator', f'{package_dir}/')
    else:
        shutil.copy('dist/KeywordGenerator.exe', f'{package_dir}/')
    
    # Copy documentation
    shutil.copy('INSTALLATION_GUIDE.md', f'{package_dir}/')
    
    # Copy sample files
    if os.path.exists('src/resources'):
        shutil.copytree('src/resources', f'{package_dir}/sample_files')
    
    print(f"✅ Distribution package created: {package_dir}")

if __name__ == "__main__":
    sys.exit(main())