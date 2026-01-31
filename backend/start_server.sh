#!/bin/bash
# Start server script for WSL/Linux

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
echo "Starting 3D Body Progress Engine API"
echo "=========================================="
echo ""
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

