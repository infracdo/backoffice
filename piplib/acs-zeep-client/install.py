#!/usr/bin/env python3
"""
Installation and setup script for ACS ZEEP Client
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"⚡ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
    return True


def install_package():
    """Install the package"""
    print("🚀 Installing ACS ZEEP Client...")
    
    if not check_python_version():
        return False
    
    # Install in development mode
    if not run_command("pip install -e .", "Installing package in development mode"):
        return False
    
    # Install development dependencies
    if not run_command("pip install -e \".[dev]\"", "Installing development dependencies"):
        print("⚠️ Development dependencies failed to install, continuing...")
    
    return True


def create_env_file():
    """Create .env file from example"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from .env.example")
        print("📝 Please edit .env file with your configuration")
        return True
    else:
        print("⚠️ .env.example not found")
        return False


def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test import
    try:
        import acs_zeep_client
        print("✅ Package import successful")
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False
    
    # Test CLI
    if not run_command("acs-zeep-cli --help", "Testing CLI command"):
        print("⚠️ CLI test failed, but package might still work")
    
    return True


def main():
    """Main installation function"""
    print("=" * 50)
    print("🔧 ACS ZEEP Client Installation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("❌ setup.py not found. Please run this script from the package root directory.")
        sys.exit(1)
    
    # Install package
    if not install_package():
        print("❌ Installation failed")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Test installation
    if not test_installation():
        print("⚠️ Some tests failed, but installation might still be working")
    
    print("\n" + "=" * 50)
    print("🎉 Installation completed!")
    print("=" * 50)
    
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Keycloak configuration")
    print("2. Test connection: acs-zeep-cli test")
    print("3. List devices: acs-zeep-cli devices list")
    print("4. Check examples in the examples/ directory")
    
    print("\n📚 Documentation:")
    print("- README.md: Basic usage and setup")
    print("- examples/: Code examples")
    print("- Use acs-zeep-cli --help for CLI commands")
    

if __name__ == "__main__":
    main()
