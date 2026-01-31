"""
Firebase Authentication middleware for FastAPI.
"""
import os
import logging
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

try:
    import firebase_admin
    from firebase_admin import auth
    FIREBASE_AUTH_AVAILABLE = True
except ImportError:
    FIREBASE_AUTH_AVAILABLE = False
    logging.warning("Firebase Admin SDK not installed. Auth will be disabled.")

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Verify Firebase ID token and return user info.
    
    Args:
        credentials: HTTP Bearer token from request header
        
    Returns:
        Decoded token with user information
        
    Raises:
        HTTPException: If token is invalid
    """
    if not FIREBASE_AUTH_AVAILABLE:
        # Development mode: return mock user
        logger.warning("Firebase Auth not available. Using mock authentication.")
        return {
            "uid": "mock_user_1",
            "email": "dev@example.com",
            "name": "Development User"
        }
    
    token = credentials.credentials
    
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture")
        }
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Get current user UID from Firebase token.
    
    Args:
        credentials: HTTP Bearer token
        
    Returns:
        User UID string
    """
    user_info = await verify_firebase_token(credentials)
    return user_info["uid"]


# Optional: Allow requests without auth in development
async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(
        HTTPBearer(auto_error=False)
    )
) -> Optional[str]:
    """
    Get user UID if token provided, otherwise return None.
    Useful for endpoints that work with or without auth.
    """
    if not credentials:
        return None
    
    try:
        user_info = await verify_firebase_token(credentials)
        return user_info["uid"]
    except HTTPException:
        return None

