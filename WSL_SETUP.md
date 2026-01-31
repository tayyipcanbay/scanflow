# WSL Setup Guide - 3D Body Progress Engine

## 🐧 Quick Setup for WSL (Windows Subsystem for Linux)

### Step 1: Create Virtual Environment

```bash
cd backend
chmod +x setup_venv.sh
./setup_venv.sh
```

Or manually:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Run the Demo

```bash
cd backend
source venv/bin/activate
./run_demo.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
python demo_services.py
```

### Step 3: Start the Server

```bash
cd backend
./start_server.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then visit: **http://localhost:8000/docs**

## 📋 Complete WSL Workflow

### Initial Setup (One Time)
```bash
# Navigate to backend
cd backend

# Make scripts executable
chmod +x setup_venv.sh start_server.sh run_demo.sh

# Run setup
./setup_venv.sh
```

### Daily Usage

**Option 1: Use the scripts**
```bash
# Run demo
./run_demo.sh

# Start server
./start_server.sh
```

**Option 2: Manual activation**
```bash
# Activate virtual environment
source venv/bin/activate

# Run commands
python demo_services.py
uvicorn app.main:app --reload
```

## 🔧 Troubleshooting

### Virtual Environment Not Found
```bash
# Create it manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Permission Denied
```bash
# Make scripts executable
chmod +x setup_venv.sh start_server.sh run_demo.sh
```

### Python Not Found
```bash
# Install Python 3
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 Quick Commands Reference

```bash
# Setup (first time only)
cd backend && ./setup_venv.sh

# Activate virtual environment
source backend/venv/bin/activate

# Run demo
cd backend && ./run_demo.sh

# Start server
cd backend && ./start_server.sh

# Deactivate virtual environment (when done)
deactivate
```

## 📝 Notes

- The virtual environment is created in `backend/venv/`
- Always activate the virtual environment before running Python commands
- The server binds to `0.0.0.0` so it's accessible from Windows host
- Use `Ctrl+C` to stop the server

## ✅ Verify Installation

After setup, test it:
```bash
cd backend
source venv/bin/activate
python -c "import fastapi, trimesh, numpy; print('✓ All packages installed!')"
```

If you see "✓ All packages installed!", you're ready to go! 🎉

