"""
Quick test to verify all components are working.
"""
import sys
from pathlib import Path

print("🧪 Quick Component Test\n")
print("=" * 60)

# Test imports
tests = [
    ("FastAPI App", "from app.main import app"),
    ("Firebase Integration", "from app.services.firebase_integration import firebase_integration"),
    ("Firebase Auth", "from app.middleware.firebase_auth import verify_firebase_token"),
    ("Mesh Processor", "from app.services.mesh_processor import MeshProcessor"),
    ("Mesh Comparator", "from app.services.mesh_comparator import MeshComparator"),
    ("Upload Route", "from app.api.routes.upload import router"),
    ("Comparison Route", "from app.api.routes.comparison import router"),
]

passed = 0
failed = 0

for name, import_stmt in tests:
    try:
        exec(import_stmt)
        print(f"✅ {name}: OK")
        passed += 1
    except Exception as e:
        print(f"❌ {name}: FAILED - {str(e)[:50]}")
        failed += 1

print("=" * 60)
print(f"\n✅ Passed: {passed}/{len(tests)}")
if failed > 0:
    print(f"❌ Failed: {failed}/{len(tests)}")
else:
    print("🎉 All components working!")

print("\n💡 Next: Start the server with 'uvicorn app.main:app --reload'")

