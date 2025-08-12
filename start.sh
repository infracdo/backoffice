#!/bin/bash
# Startup script for the FastAPI application

set -e

echo "🚀 Starting Zeep Backend..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# List directory contents
echo "Directory contents:"
ls -la

# Set Python path to include the current directory
export PYTHONPATH="${PYTHONPATH}:/app"

echo "Python path: $PYTHONPATH"

# Check if app.py exists
if [ -f "app.py" ]; then
    echo "✅ Found app.py"
else
    echo "❌ app.py not found!"
    echo "Looking for Python files:"
    find . -name "*.py" -type f | head -10
    exit 1
fi

# Test basic imports
echo "🔍 Testing Python imports..."
python -c "import sys; print('Python executable:', sys.executable)" || exit 1
python -c "import fastapi; print('✅ FastAPI imported')" || exit 1

echo "✅ Starting application with Python directly..."

# Start the application
exec python app.py
