#!/bin/bash
# Startup script for the FastAPI application
# This ensures proper Python path and module resolution

set -e

echo "🚀 Starting Zeep Backend..."

# Set Python path to include the current directory
export PYTHONPATH="${PYTHONPATH}:/app"

# Print debug information
echo "Python path: $PYTHONPATH"
echo "Working directory: $(pwd)"
echo "Contents:"
ls -la

# Check if the main modules can be imported
echo "🔍 Testing module imports..."
python -c "import app; print('✅ app module imported successfully')" || {
    echo "❌ Failed to import app module"
    echo "Available Python modules:"
    python -c "import sys; print(sys.path)"
    exit 1
}

python -c "from main.modules import api_router; print('✅ main.modules imported successfully')" || {
    echo "❌ Failed to import main.modules"
    exit 1
}

echo "✅ All imports successful, starting the application..."

# Start the application with gunicorn
exec gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5050 app:app --timeout 10800
