# 📤 Commands to Push to GitHub (User---Aish Branch)

## 🎯 Quick Push Commands

### Step 1: Make sure you're on the right branch
```bash
cd "/mnt/d/2025/02_Course/Semester 3/000001_Cursor"
git checkout User---Aish
```

### Step 2: Check what needs to be committed
```bash
git status
```

### Step 3: Add all changes (if any new files)
```bash
# Add all modified and new files
git add .

# Or add specific files
git add backend/app/services/firebase_integration.py
git add backend/app/middleware/
git add backend/app/api/routes/
git add *.md
```

### Step 4: Commit changes (if needed)
```bash
git commit -m "feat: Add Firebase integration and test results"
```

### Step 5: Push to GitHub
```bash
git push origin User---Aish
```

---

## 🔑 Authentication

When you run `git push`, you'll be asked for:

**Username**: `Aish-1999` (or `tayyipcanbay` if you have access)

**Password**: Use a **Personal Access Token** (NOT your GitHub password)

### Create Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "ScanFlow Push"
4. Select scope: `repo` (check the box)
5. Generate and **copy the token**
6. Use this token as your password

---

## 📋 Complete Command Sequence

```bash
# 1. Navigate to project
cd "/mnt/d/2025/02_Course/Semester 3/000001_Cursor"

# 2. Check current branch
git branch

# 3. Switch to your branch (if not already)
git checkout User---Aish

# 4. Check status
git status

# 5. Add files (if needed)
git add .

# 6. Commit (if needed)
git commit -m "feat: Complete Firebase-FastAPI integration with tests"

# 7. Push to GitHub
git push origin User---Aish
```

---

## ⚠️ If You Get Permission Error

If you get "Permission denied", you have 2 options:

### Option 1: Fork the Repository
```bash
# 1. Fork on GitHub (click Fork button)
# 2. Change remote to your fork
git remote set-url origin https://github.com/Aish-1999/scanflow.git
# 3. Push
git push origin User---Aish
```

### Option 2: Get Collaborator Access
Ask `tayyipcanbay` to add you as collaborator, then push.

---

## ✅ After Successful Push

You'll see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/tayyipcanbay/scanflow.git
 * [new branch]      User---Aish -> User---Aish
```

Then you can:
- View on GitHub: https://github.com/tayyipcanbay/scanflow/tree/User---Aish
- Create Pull Request to merge into main

---

*Ready to push!* 🚀

