# 📤 How to Push to GitHub

## ✅ Remote is Now Set to HTTPS

The remote URL has been changed from SSH to HTTPS so you can use a Personal Access Token.

## 🚀 Push Command

```bash
git push -u origin feature/user-work
```

## 🔑 Authentication

When prompted, you'll need:

### Username
```
tayyipcanbay
```

### Password
**Use a Personal Access Token (NOT your GitHub password)**

## 📝 Create Personal Access Token

1. **Go to GitHub**: https://github.com/settings/tokens
2. **Click**: "Generate new token" → "Generate new token (classic)"
3. **Name**: "ScanFlow Integration" (or any name)
4. **Expiration**: Choose (90 days recommended)
5. **Select scopes**: Check `repo` (Full control of private repositories)
6. **Click**: "Generate token"
7. **Copy the token** (you won't see it again!)

## 💡 Quick Steps

```bash
# 1. Make sure you're in the project root
cd "/mnt/d/2025/02_Course/Semester 3/000001_Cursor"

# 2. Verify remote is HTTPS
git remote -v
# Should show: https://github.com/tayyipcanbay/scanflow.git

# 3. Push
git push -u origin feature/user-work

# 4. When prompted:
# Username: tayyipcanbay
# Password: [paste your Personal Access Token]
```

## ⚠️ Important Notes

- **Don't use your GitHub password** - it won't work
- **Use the Personal Access Token** as the password
- The token will be saved if you configure credential helper
- Keep your token secure - don't share it

## 🔒 Save Credentials (Optional)

To avoid entering token every time:

```bash
git config --global credential.helper store
git push -u origin feature/user-work
# Enter username and token once - it will be saved
```

## ✅ After Successful Push

You'll see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/tayyipcanbay/scanflow.git
 * [new branch]      feature/user-work -> feature/user-work
Branch 'feature/user-work' set up to track remote branch 'feature/user-work' from 'origin'.
```

---

*Ready to push!* 🚀

