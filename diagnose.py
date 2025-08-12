#!/usr/bin/env python3
"""
Diagnostic script to debug container issues
"""

import os
import sys
import subprocess

def main():
    print("=" * 50)
    print("🔍 CONTAINER DIAGNOSTIC INFORMATION")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"User ID: {os.getuid() if hasattr(os, 'getuid') else 'N/A'}")
    
    print("\n📁 Directory listing:")
    try:
        files = sorted(os.listdir('.'))
        for f in files:
            path = os.path.join('.', f)
            if os.path.isdir(path):
                print(f"  📁 {f}/")
            else:
                size = os.path.getsize(path)
                print(f"  📄 {f} ({size} bytes)")
    except Exception as e:
        print(f"Error listing directory: {e}")
    
    print("\n🔎 Looking for Python files:")
    try:
        result = subprocess.run(['find', '.', '-name', '*.py', '-type', 'f'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    print(f"  {line}")
        else:
            print("Find command failed")
    except Exception as e:
        print(f"Error running find: {e}")
    
    print("\n🐍 Python path:")
    for path in sys.path:
        print(f"  {path}")
    
    print("\n🌍 Environment variables:")
    for key in ['PYTHONPATH', 'PATH', 'PWD', 'HOME']:
        print(f"  {key}={os.environ.get(key, 'Not set')}")
    
    print("\n✅ Checking if app.py exists:")
    if os.path.exists('app.py'):
        print("  ✅ app.py found!")
        try:
            with open('app.py', 'r') as f:
                first_line = f.readline().strip()
                print(f"  First line: {first_line}")
        except Exception as e:
            print(f"  Error reading app.py: {e}")
    else:
        print("  ❌ app.py NOT found!")
    
    print("\n" + "=" * 50)
    print("END DIAGNOSTIC")
    print("=" * 50)

if __name__ == "__main__":
    main()
