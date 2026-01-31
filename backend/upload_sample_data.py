"""
Script to upload sample data to the API.
"""
import requests
import json
from pathlib import Path
import time

API_BASE = "http://localhost:8000/api"

def upload_mesh(file_path, user_id=1):
    """Upload a mesh file to the API."""
    url = f"{API_BASE}/upload"
    
    with open(file_path, 'rb') as f:
        files = {'file': (Path(file_path).name, f, 'application/octet-stream')}
        data = {'user_id': user_id}
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error uploading {file_path}: {response.status_code}")
            print(response.text)
            return None

def upload_bia_data(user_id, mesh_upload_id, bia_data):
    """Upload BIA data (this would need a BIA endpoint - for now just print)"""
    print(f"  BIA data for mesh {mesh_upload_id}:")
    print(f"    Weight: {bia_data['weight']}kg")
    print(f"    BMI: {bia_data['bmi']}")
    print(f"    Fat: {bia_data['fat_percentage']}%")
    print(f"    Muscle: {bia_data['muscle_percentage']}%")
    print(f"    Water: {bia_data['water_percentage']}%")
    # TODO: Add BIA upload endpoint if needed

def upload_all_sample_data():
    """Upload all sample data to the API."""
    print("=" * 60)
    print("Uploading Sample Data to API")
    print("=" * 60)
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE.replace('/api', '')}/api/health")
        if response.status_code != 200:
            print("❌ API is not running. Please start the server first:")
            print("   uvicorn app.main:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Please start the server first:")
        print("   uvicorn app.main:app --reload")
        return
    
    print("✓ API is running")
    print()
    
    # Load upload mapping (try realistic first, then fallback to regular)
    mapping_file = Path("sample_data/realistic_upload_mapping.json")
    if not mapping_file.exists():
        mapping_file = Path("sample_data/upload_mapping.json")
        if not mapping_file.exists():
            print("❌ Sample data not found. Please run generate_realistic_body.py or generate_sample_data.py first")
            return
    
    with open(mapping_file) as f:
        mapping = json.load(f)
    
    user_id = mapping['user_id']
    uploads = mapping['uploads']
    
    print(f"Uploading data for user {user_id}...")
    print()
    
    uploaded_meshes = []
    
    for upload_info in uploads:
        week = upload_info['week']
        file_path = upload_info['file']
        bia_data = upload_info.get('bia_data', {})
        
        print(f"Week {week}: Uploading {Path(file_path).name}...")
        
        result = upload_mesh(file_path, user_id)
        
        if result:
            mesh_id = result['id']
            uploaded_meshes.append({
                'week': week,
                'mesh_id': mesh_id,
                'is_baseline': upload_info['is_baseline'],
                'bia_data': bia_data
            })
            print(f"  ✓ Uploaded successfully (ID: {mesh_id})")
            
            if bia_data:
                upload_bia_data(user_id, mesh_id, bia_data)
            
            time.sleep(0.5)  # Small delay between uploads
        else:
            print(f"  ✗ Upload failed")
        
        print()
    
    print("=" * 60)
    print("✓ Upload complete!")
    print("=" * 60)
    print()
    
    if len(uploaded_meshes) >= 2:
        baseline = next(m for m in uploaded_meshes if m['is_baseline'])
        latest = uploaded_meshes[-1]
        
        print("You can now test comparisons:")
        print(f"  GET {API_BASE}/comparison/{baseline['mesh_id']}/{latest['mesh_id']}")
        print()
        print("Or get latest comparison:")
        print(f"  GET {API_BASE}/comparison/user/{user_id}/latest")
        print()
    
    # Save upload results
    results_file = Path("sample_data/upload_results.json")
    with open(results_file, 'w') as f:
        json.dump(uploaded_meshes, f, indent=2)
    print(f"Upload results saved to: {results_file}")

if __name__ == "__main__":
    try:
        upload_all_sample_data()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

