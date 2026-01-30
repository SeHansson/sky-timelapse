#!/bin/bash

# TIMESHIFT Quick Start Script
# This script sets up and runs the RTSP Timelapse application

echo "======================================"
echo "  TIMESHIFT - RTSP Timelapse Studio"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/frames
mkdir -p data/timelapses

echo "✓ Directories created"

# Start the application
echo ""
echo "🚀 Starting TIMESHIFT..."
echo ""
echo "Access the web interface at:"
echo "  Local:   http://localhost:5000"
echo "  Network: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
