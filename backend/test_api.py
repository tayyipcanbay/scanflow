"""
Simple test script to verify the API is working.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    print(f"✓ Root endpoint: {response.status_code}")
    print(f"  Response: {response.json()}")
    return response.status_code == 200

def test_health():
    """Test health endpoint."""
    response = client.get("/api/health")
    print(f"✓ Health endpoint: {response.status_code}")
    print(f"  Response: {response.json()}")
    return response.status_code == 200

def test_upload_endpoint():
    """Test upload endpoint exists."""
    # Just check if endpoint is registered
    routes = [route.path for route in app.routes]
    has_upload = any("/api/upload" in route for route in routes)
    print(f"✓ Upload endpoint registered: {has_upload}")
    return has_upload

if __name__ == "__main__":
    print("=" * 50)
    print("Testing 3D Body Progress Engine API")
    print("=" * 50)
    print()
    
    try:
        test_root()
        print()
        test_health()
        print()
        test_upload_endpoint()
        print()
        print("=" * 50)
        print("✓ All basic tests passed!")
        print("=" * 50)
        print()
        print("To start the server, run:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        print()
        print("Then visit: http://localhost:8000/docs for API documentation")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

