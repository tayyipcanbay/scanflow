#!/bin/bash
# Install Streamlit and Plotly

echo "Installing Streamlit and Plotly..."

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
echo "Installing streamlit and plotly..."
pip install streamlit plotly

echo ""
echo "✓ Installation complete!"
echo ""
echo "You can now run:"
echo "  streamlit run streamlit_app.py"
echo ""
echo "Or use the script:"
echo "  ./run_streamlit.sh"

