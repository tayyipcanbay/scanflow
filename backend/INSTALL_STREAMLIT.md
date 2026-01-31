# Install Streamlit - Quick Fix

## The Error
```
streamlit: command not found
```

## Solution

In your WSL terminal (make sure you're in the venv), run:

```bash
cd backend
source venv/bin/activate
pip install streamlit plotly
```

## Or Use the Script

```bash
cd backend
chmod +x install_streamlit.sh
./install_streamlit.sh
```

## Verify Installation

```bash
streamlit --version
```

Should show: `Streamlit, version X.X.X`

## Then Run the App

```bash
streamlit run streamlit_app.py
```

The app will open at: **http://localhost:8501**

## Alternative: Install All Dependencies

If you want to install everything at once:

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

This will install streamlit, plotly, and all other dependencies.

