#!/bin/bash
# Run demo script for WSL/Linux

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Run setup_venv.sh first."
    exit 1
fi

echo ""
echo "=========================================="
echo "3D Body Progress Engine - Service Demo"
echo "=========================================="
echo ""

python demo_services.py

echo ""
echo "=========================================="

