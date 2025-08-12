#!/bin/bash
# Simple startup script that definitely exists in the container

echo "🚀 Container startup script running..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Directory contents:"
ls -la

echo "Looking for app.py..."
if [ -f "app.py" ]; then
    echo "✅ Found app.py, starting application..."
    python app.py
else
    echo "❌ app.py not found!"
    echo "Available files:"
    find . -name "*.py" -type f
    exit 1
fi
