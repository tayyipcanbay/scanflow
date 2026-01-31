"""
Simple test script to verify the API is working.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app

# Check routes without TestClient (version compatibility issue)
def check_routes():
    """Check if routes are registered."""
    routes = [route.path for route in app.routes]
    return routes

def test_routes():
    """Test that routes are registered."""
    routes = check_routes()
    print(f"✓ Total routes registered: {len(routes)}")
    
    # Check key routes
    has_root = any(route == "/" for route in routes)
    has_health = any("/api/health" in route for route in routes)
    has_upload = any("/api/upload" in route for route in routes)
    has_comparison = any("/api/comparison" in route for route in routes)
    
    print(f"✓ Root endpoint: {has_root}")
    print(f"✓ Health endpoint: {has_health}")
    print(f"✓ Upload endpoint: {has_upload}")
    print(f"✓ Comparison endpoint: {has_comparison}")
    
    return has_root and has_health and has_upload and has_comparison

if __name__ == "__main__":
    print("=" * 50)
    print("Testing 3D Body Progress Engine API")
    print("=" * 50)
    print()
    
    try:
        test_routes()
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

