#!/bin/bash
# Fix virtual environment creation

echo "=========================================="
echo "Creating Virtual Environment"
echo "=========================================="
echo ""

# Check current directory
echo "Current directory: $(pwd)"
echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing it..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment with python3..."
python3 -m venv venv

# Check if creation was successful
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    echo "✓ Virtual environment created successfully!"
    echo ""
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo ""
    echo "✓ Virtual environment activated!"
    echo "Python location: $(which python)"
    echo "Python version: $(python --version)"
    echo ""
    
    echo "Upgrading pip..."
    pip install --upgrade pip
    
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo ""
    echo "=========================================="
    echo "✓ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Virtual environment is ready!"
    echo ""
    echo "To activate in the future, run:"
    echo "  source venv/bin/activate"
    echo ""
else
    echo "❌ Failed to create virtual environment"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if python3 is installed: python3 --version"
    echo "2. Check if python3-venv is installed: apt list --installed | grep python3-venv"
    echo "3. If not installed, run: sudo apt install python3-venv"
    exit 1
fi

