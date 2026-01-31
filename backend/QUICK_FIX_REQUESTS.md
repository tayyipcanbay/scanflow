# Quick Fix: Install Requests

## The Problem
```
ImportError: No module named 'requests'
```

## Solution

Run this in your WSL terminal:

```bash
cd backend
source venv/bin/activate
pip install requests
```

## Or Use the Script

```bash
cd backend
chmod +x install_requests.sh
./install_requests.sh
```

## Verify Installation

```bash
python -c "import requests; print('✓ Requests installed!')"
```

## Then Try Again

```bash
python upload_sample_data.py
```

## Alternative: Install All Dependencies

If you want to make sure everything is installed:

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

This will install all dependencies including requests.

