# 🔗 Firebase-FastAPI Integration Guide

## Overview

This guide explains how the Firebase and FastAPI backends are integrated to create a unified platform.

## Architecture

```
User Uploads Mesh (FastAPI)
    ↓
Process & Store (FastAPI + SQLite)
    ↓
Sync to Firebase Digital Twin
    ↓
Trigger AI Plan Generation (Firebase)
    ↓
User Gets Personalized Plan
```

## Components

### 1. Firebase Integration Service
**Location**: `backend/app/services/firebase_integration.py`

**Purpose**: Syncs FastAPI mesh data to Firebase Digital Twin

**Key Methods**:
- `sync_mesh_to_digital_twin()` - Syncs mesh upload to Firebase
- `trigger_ai_plan_regeneration()` - Triggers AI plan update
- `get_user_profile()` - Gets user data from Firebase

### 2. Firebase Auth Middleware
**Location**: `backend/app/middleware/firebase_auth.py`

**Purpose**: Validates Firebase tokens in FastAPI requests

**Usage**:
```python
from app.middleware.firebase_auth import get_current_user

@router.get("/protected")
async def protected_route(uid: str = Depends(get_current_user)):
    # uid is the Firebase user UID
    pass
```

### 3. Updated Routes
- **Upload Route**: Now syncs to Firebase after upload
- **Comparison Route**: Syncs comparison data and triggers AI regeneration

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Firebase Configuration

**Option A: Use Firebase Emulator (Development)**
```bash
# Start Firebase Emulator
npx firebase emulators:start

# The integration will automatically use the emulator
```

**Option B: Use Production Firebase**
```bash
# Set environment variable
export FIREBASE_CREDENTIALS_PATH="/path/to/service-account-key.json"
```

### 3. Environment Variables
Create `.env` file:
```env
FIREBASE_CREDENTIALS_PATH=/path/to/service-account-key.json
# Or leave empty to use default credentials/emulator
```

## Usage

### Upload Mesh with Firebase Auth
```bash
# Get Firebase token (from frontend or Firebase SDK)
TOKEN="your-firebase-id-token"

# Upload mesh
curl -X POST "http://localhost:8000/api/upload/" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@mesh.glb"
```

### Without Auth (Backward Compatible)
```bash
# Still works for testing
curl -X POST "http://localhost:8000/api/upload/" \
  -F "file=@mesh.glb" \
  -F "user_id=1"
```

## Data Flow

### 1. Mesh Upload Flow
```
1. User uploads mesh → FastAPI
2. FastAPI processes & stores in SQLite
3. FastAPI syncs to Firebase Digital Twin
4. Firebase stores in users/{uid}/digitalTwin/latest
```

### 2. Comparison Flow
```
1. User compares two meshes → FastAPI
2. FastAPI calculates differences
3. FastAPI syncs comparison data to Firebase
4. Firebase triggers AI plan regeneration
5. AI generates new plan based on body changes
```

## Testing

### Test Firebase Integration
```python
from app.services.firebase_integration import firebase_integration

# Test sync
result = firebase_integration.sync_mesh_to_digital_twin(
    user_id="test_user_123",
    mesh_data={"file_path": "/path/to/mesh.glb", "weight": 75.0}
)
print(f"Sync successful: {result}")
```

### Test Auth Middleware
```python
from app.middleware.firebase_auth import verify_firebase_token

# In development, returns mock user
user_info = await verify_firebase_token(credentials)
print(user_info["uid"])
```

## Troubleshooting

### Firebase Not Initialized
**Error**: "Firebase not available. Skipping sync."

**Solution**: 
- Check if Firebase emulator is running
- Or set `FIREBASE_CREDENTIALS_PATH` environment variable

### Auth Token Invalid
**Error**: "Invalid authentication token"

**Solution**:
- Ensure token is a valid Firebase ID token
- Check token expiration
- In development, auth is optional (returns mock user)

### Sync Fails Silently
**Note**: Sync failures are logged but don't fail the request. Check logs for details.

## Next Steps

1. **User Mapping**: Create proper mapping between Firebase UID and FastAPI user_id
2. **Metrics Extraction**: Extract actual body metrics from mesh files
3. **Real-time Updates**: Use Firestore listeners for real-time sync
4. **Error Handling**: Add retry logic for Firebase operations

## Production Considerations

1. **Service Account**: Use Firebase service account key in production
2. **Error Handling**: Implement proper error handling and retries
3. **Rate Limiting**: Add rate limiting for Firebase API calls
4. **Monitoring**: Add logging and monitoring for sync operations
5. **Security**: Validate all Firebase tokens properly

