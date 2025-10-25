#!/bin/bash
# Quick setup script for Lyra demo

echo "========================================="
echo "  Lyra Demo - Quick Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

echo "✓ Python found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies (rich, typer)..."
pip install -q -r requirements_demo.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating output directories..."
mkdir -p demo/outputs

echo "✓ Directories created"
echo ""

# Test the demo
echo "Testing demo..."
python src/main.py version

if [ $? -ne 0 ]; then
    echo "❌ Demo test failed"
    exit 1
fi

echo "✓ Demo test passed"
echo ""

echo "========================================="
echo "  ✨ Setup Complete!"
echo "========================================="
echo ""
echo "Run the demo with:"
echo "  python src/main.py create-release-notes v2.1"
echo ""
echo "Or with explanation of what's hardcoded:"
echo "  python src/main.py create-release-notes v2.1 --show-hardcoded"
echo ""
echo "For demo info:"
echo "  python src/main.py info"
echo ""
echo "For presentation guide:"
echo "  cat demo/PRESENTATION_SCRIPT.md"
echo ""

