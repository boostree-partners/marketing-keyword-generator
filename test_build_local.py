#!/usr/bin/env python3
"""
Local test script to simulate GitHub Actions environment
"""

import os
import sys
import subprocess

def test_build_script():
    """Test build script in CI/CD environment simulation"""
    
    print("🧪 Testing build script in CI/CD environment simulation")
    print("=" * 60)
    
    # Set CI environment variables
    os.environ['CI'] = 'true'
    os.environ['GITHUB_ACTIONS'] = 'true'
    
    print("🔧 Environment variables set:")
    print(f"   CI: {os.environ.get('CI')}")
    print(f"   GITHUB_ACTIONS: {os.environ.get('GITHUB_ACTIONS')}")
    
    # Test build script import
    print("\n📦 Testing build script import...")
    try:
        import build_executable
        print("✅ Build script import successful")
    except Exception as e:
        print(f"❌ Build script import failed: {e}")
        return False
    
    # Test spec file creation
    print("\n📄 Testing spec file creation...")
    try:
        spec_file = build_executable.create_spec_file()
        print(f"✅ Spec file created: {spec_file}")
        
        # Check if spec file exists
        if os.path.exists(spec_file):
            print(f"✅ Spec file exists: {spec_file}")
        else:
            print(f"❌ Spec file not found: {spec_file}")
            return False
            
    except Exception as e:
        print(f"❌ Spec file creation failed: {e}")
        return False
    
    # Test cleanup function
    print("\n🧹 Testing cleanup function...")
    try:
        build_executable.cleanup_build()
        print("✅ Cleanup function executed successfully")
    except Exception as e:
        print(f"❌ Cleanup function failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! Build script is ready for GitHub Actions")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_build_script()
    sys.exit(0 if success else 1) 