#!/usr/bin/env python3
"""
GitLab repository initialization script
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"⚡ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout.strip())
        if e.stderr:
            print("STDERR:", e.stderr.strip())
        return False

def main():
    """Initialize git repository for GitLab"""
    print("🚀 Initializing ACS ZEEP Client for GitLab")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("❌ setup.py not found. Please run this script from the package root directory.")
        sys.exit(1)
    
    # Initialize git if not already done
    if not Path(".git").exists():
        if not run_command("git init", "Initializing git repository"):
            sys.exit(1)
    
    # Add all files
    if not run_command("git add .", "Adding all files to git"):
        sys.exit(1)
    
    # Create initial commit
    if not run_command('git commit -m "Initial commit: ACS ZEEP Client Python library"', "Creating initial commit"):
        print("⚠️ Commit may have failed, but continuing...")
    
    print("\n" + "=" * 50)
    print("🎉 Repository initialized!")
    print("=" * 50)
    
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitLab")
    print("2. Add the remote origin:")
    print("   git remote add origin https://gitlab.com/your-org/acs-zeep-client.git")
    print("3. Push to GitLab:")
    print("   git push -u origin main")
    print("\n4. After pushing, you can install the package with:")
    print("   pip install git+https://gitlab.com/your-org/acs-zeep-client.git@main")
    print("\n5. Or add to requirements.txt:")
    print("   git+https://gitlab.com/your-org/acs-zeep-client.git@main")
    
    print("\n📚 Files created:")
    files_created = [
        ".gitignore - Comprehensive ignore rules",
        ".gitlab-ci.yml - CI/CD pipeline configuration", 
        "README.md - Updated with GitLab instructions",
        "setup.py - Updated with GitLab URLs"
    ]
    
    for file_info in files_created:
        print(f"  ✅ {file_info}")

if __name__ == "__main__":
    main()
