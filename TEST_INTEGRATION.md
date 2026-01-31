# 🧪 Test the Integration

## Quick Start

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run Integration Test
```bash
cd backend
python test_integration.py
```

**Expected Output**:
- ✅ Firebase integration service works
- ⚠️ Firebase not available (OK - runs in mock mode)
- ✅ Auth middleware available

### Step 3: Test with Firebase Emulator (Optional)

**Terminal 1 - Start Firebase Emulator**:
```bash
# In project root
npx firebase emulators:start
```

**Terminal 2 - Start FastAPI**:
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 3 - Test Upload**:
```bash
# Without auth (backward compatible)
curl -X POST "http://localhost:8000/api/upload/" \
  -F "file=@before_fitness.glb" \
  -F "user_id=1"

# With Firebase token (if you have one)
curl -X POST "http://localhost:8000/api/upload/" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -F "file=@before_fitness.glb"
```

### Step 4: Check Firebase Emulator UI

1. Open: http://localhost:4000
2. Go to Firestore
3. Check `users/{uid}/digitalTwin/latest`
4. You should see synced mesh data

## What to Verify

✅ **Integration Service**:
- Can be imported
- Handles Firebase unavailability gracefully
- Syncs data when Firebase is available

✅ **Auth Middleware**:
- Works without Firebase (mock mode)
- Validates tokens when Firebase available

✅ **Routes**:
- Upload route accepts Firebase tokens
- Comparison route syncs to Firebase
- Backward compatible with user_id

✅ **Data Flow**:
- Mesh upload → Firebase Digital Twin
- Comparison → Firebase + AI trigger

## Troubleshooting

### "Firebase not available"
**This is OK!** The integration runs in mock mode. To use real Firebase:
1. Start Firebase emulator, OR
2. Set `FIREBASE_CREDENTIALS_PATH` environment variable

### "Module not found: firebase_admin"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "Token verification failed"
**Solution**: 
- In development, auth is optional
- For production, use valid Firebase ID tokens

## Next Steps

1. ✅ Integration is working
2. 🔄 Test with real Firebase emulator
3. 🔄 Connect frontend with Firebase Auth
4. 🔄 Test end-to-end flow

---

*Ready to test!* 🚀

