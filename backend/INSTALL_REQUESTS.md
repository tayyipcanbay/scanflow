# Install Requests - Quick Fix

## The Error
```
ModuleNotFoundError: No module named 'requests'
```

## Solution

In your WSL terminal (you're already in the venv), run:

```bash
pip install requests
```

That's it! Just one command.

## Verify

After installing, verify it works:

```bash
python -c "import requests; print('✓ Requests installed!')"
```

## Then Upload

```bash
python upload_sample_data.py
```

## Alternative: Install All Dependencies

If you want to make sure everything is up to date:

```bash
pip install -r requirements.txt
```

This will install/update all dependencies including requests.

