#!/usr/bin/env python3
"""
Container entry point for the Zeep Backend application
This script ensures proper startup and error handling
"""

import os
import sys
import traceback

def main():
    print("🚀 Starting Zeep Backend Application...")
    
    # Print debug information
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # List current directory contents
    print("Directory contents:")
    try:
        files = os.listdir('.')
        for file in sorted(files):
            if os.path.isdir(file):
                print(f"  📁 {file}/")
            else:
                print(f"  📄 {file}")
    except Exception as e:
        print(f"Error listing directory: {e}")
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ ERROR: app.py not found in current directory!")
        sys.exit(1)
    
    print("✅ app.py found, importing application...")
    
    try:
        # Import the FastAPI app
        from app import app
        print("✅ FastAPI app imported successfully")
        
        # Import uvicorn
        import uvicorn
        print("✅ uvicorn imported successfully")
        
        # Get port from environment or use default
        port = int(os.getenv('PORT', 5050))
        
        print(f"🌟 Starting server on 0.0.0.0:{port}")
        
        # Start the server
        uvicorn.run(
            app, 
            host='0.0.0.0', 
            port=port, 
            log_level='info'
        )
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
