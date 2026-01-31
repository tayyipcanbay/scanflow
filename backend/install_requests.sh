#!/bin/bash
# Install requests package

echo "Installing requests package..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

echo ""
echo "Installing requests..."
pip install requests

echo ""
echo "✓ Requests installed!"
echo ""
echo "You can now run:"
echo "  python upload_sample_data.py"

