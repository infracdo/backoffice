#!/usr/bin/env python3
"""
Simple test script to verify the application can be imported correctly
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, '/app')
os.chdir('/app')

print("🔍 Testing application imports...")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")

try:
    print("Testing FastAPI import...")
    import fastapi
    print("✅ FastAPI imported successfully")
    
    print("Testing app module import...")
    import app
    print("✅ app module imported successfully")
    print(f"app instance: {app.app}")
    
    print("Testing main.modules import...")
    from main.modules import api_router
    print("✅ main.modules imported successfully")
    
    print("Testing database imports...")
    from main.core.config import settings
    print("✅ settings imported successfully")
    
    from main.db.dbpostgres.session import SessionLocal
    print("✅ database session imported successfully")
    
    print("🎉 All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Available modules in current directory:")
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.'):
            print(f"  📁 {item}/")
        elif item.endswith('.py'):
            print(f"  📄 {item}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
