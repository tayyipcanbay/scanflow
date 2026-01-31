# Quick Fix for Virtual Environment

## The Problem
The virtual environment wasn't created properly because the command was cut off.

## Solution

Run this complete command in your WSL terminal:

```bash
cd backend
python3 -m venv venv
```

**Make sure you type the full command: `python3 -m venv venv`** (not just `ve`)

## Then Activate It

```bash
source venv/bin/activate
```

## Verify It Worked

You should see `(venv)` at the start of your prompt:
```bash
(venv) aishwarya@Aishwarya:/mnt/d/.../backend$
```

## Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Or Use the Fix Script

I've created a script that does everything:

```bash
cd backend
chmod +x fix_venv.sh
./fix_venv.sh
```

This will:
1. Remove any broken venv
2. Create a new one
3. Activate it
4. Install all dependencies

## Common Issues

### Issue: "python3-venv not found"
```bash
sudo apt update
sudo apt install python3-venv
```

### Issue: "Permission denied"
```bash
chmod +x fix_venv.sh
```

### Issue: "No such file or directory"
Make sure you're in the `backend` directory:
```bash
cd /mnt/d/2025/02_Course/Semester\ 3/000001_Cursor/backend
pwd  # Should show .../backend
```

