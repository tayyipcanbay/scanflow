"""
Generate sample 3D mesh files and metadata for testing.
"""
import numpy as np
import trimesh
from pathlib import Path
import json
import random
from datetime import datetime, timedelta

def generate_body_mesh(version=1, changes=None):
    """
    Generate a synthetic 3D body mesh.
    
    Args:
        version: Version number (1 = baseline, 2+ = with changes)
        changes: Dictionary with region changes (optional)
    
    Returns:
        trimesh.Trimesh object
    """
    # Create a basic humanoid shape (simplified)
    # This is a synthetic mesh representing a body
    
    # Generate vertices for a body-like shape
    num_vertices = 2000
    
    # Base body shape (ellipsoid-like)
    theta = np.linspace(0, 2 * np.pi, 50)
    phi = np.linspace(0, np.pi, 40)
    theta, phi = np.meshgrid(theta, phi)
    
    # Body proportions
    x_scale = 0.4  # Width
    y_scale = 1.0  # Height (vertical)
    z_scale = 0.3  # Depth
    
    # Generate vertices
    x = x_scale * np.sin(phi) * np.cos(theta)
    y = y_scale * np.cos(phi)
    z = z_scale * np.sin(phi) * np.sin(theta)
    
    # Flatten and combine
    vertices = np.column_stack([x.ravel(), y.ravel(), z.ravel()])
    
    # Add some variation to make it more body-like
    noise = np.random.randn(len(vertices), 3) * 0.05
    vertices += noise
    
    # Apply changes if this is not baseline
    if version > 1 and changes:
        # Simulate body changes in different regions
        for i, vertex in enumerate(vertices):
            y_pos = vertex[1]  # Vertical position
            
            # Waist region (middle)
            if -0.2 < y_pos < 0.2:
                if 'waist' in changes:
                    change = changes['waist']
                    # Move vertices inward (decrease) or outward (increase)
                    direction = np.array([1, 0, 1])  # Horizontal direction
                    direction = direction / np.linalg.norm(direction)
                    vertices[i] += direction * change * 0.1
            
            # Chest region (upper)
            elif 0.2 < y_pos < 0.6:
                if 'chest' in changes:
                    change = changes['chest']
                    direction = np.array([1, 0, 1])
                    direction = direction / np.linalg.norm(direction)
                    vertices[i] += direction * change * 0.1
            
            # Thighs region (lower)
            elif -0.8 < y_pos < -0.3:
                if 'thighs' in changes:
                    change = changes['thighs']
                    direction = np.array([1, 0, 1])
                    direction = direction / np.linalg.norm(direction)
                    vertices[i] += direction * change * 0.1
    
    # Create a proper mesh structure
    # Use icosphere as base and modify it
    try:
        # Create an icosphere and scale it to body proportions
        mesh = trimesh.creation.icosphere(subdivisions=2, radius=1.0)
        
        # Scale to body proportions
        mesh.vertices[:, 0] *= x_scale  # Width
        mesh.vertices[:, 1] *= y_scale  # Height
        mesh.vertices[:, 2] *= z_scale  # Depth
        
        # Add noise for variation
        noise = np.random.randn(len(mesh.vertices), 3) * 0.03
        mesh.vertices += noise
        
        # Apply changes if this is not baseline
        if version > 1 and changes:
            # Simulate body changes in different regions
            for i, vertex in enumerate(mesh.vertices):
                y_pos = vertex[1]  # Vertical position
                
                # Waist region (middle)
                if -0.2 < y_pos < 0.2:
                    if 'waist' in changes:
                        change = changes['waist']
                        # Move vertices inward (decrease) or outward (increase)
                        direction = mesh.vertices[i].copy()
                        direction[1] = 0  # Horizontal only
                        if np.linalg.norm(direction) > 0:
                            direction = direction / np.linalg.norm(direction)
                            mesh.vertices[i] += direction * change * 0.15
                
                # Chest region (upper)
                elif 0.2 < y_pos < 0.6:
                    if 'chest' in changes:
                        change = changes['chest']
                        direction = mesh.vertices[i].copy()
                        direction[1] = 0
                        if np.linalg.norm(direction) > 0:
                            direction = direction / np.linalg.norm(direction)
                            mesh.vertices[i] += direction * change * 0.15
                
                # Arms region (sides, upper)
                elif 0.1 < y_pos < 0.5 and abs(vertex[0]) > 0.25:
                    if 'arms' in changes:
                        change = changes['arms']
                        direction = np.array([1 if vertex[0] > 0 else -1, 0, 0])
                        mesh.vertices[i] += direction * change * 0.1
                
                # Thighs region (lower)
                elif -0.8 < y_pos < -0.3:
                    if 'thighs' in changes:
                        change = changes['thighs']
                        direction = mesh.vertices[i].copy()
                        direction[1] = 0
                        if np.linalg.norm(direction) > 0:
                            direction = direction / np.linalg.norm(direction)
                            mesh.vertices[i] += direction * change * 0.15
        
        # Ensure mesh is valid
        mesh.fix_normals()
        mesh.remove_duplicate_faces()
        
    except Exception as e:
        # Fallback: create simple mesh from vertices
        print(f"Warning: Using fallback mesh generation: {e}")
        # Create a simple sphere as fallback
        mesh = trimesh.creation.icosphere(subdivisions=1, radius=1.0)
        mesh.vertices[:, 0] *= x_scale
        mesh.vertices[:, 1] *= y_scale
        mesh.vertices[:, 2] *= z_scale
    
    return mesh

def generate_sample_meshes(output_dir="sample_data/meshes"):
    """Generate sample mesh files for different time points."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Generating sample 3D mesh files...")
    
    # Baseline mesh (Week 0)
    print("  Creating baseline mesh (Week 0)...")
    baseline_mesh = generate_body_mesh(version=1)
    baseline_path = output_path / "user1_week0.obj"
    baseline_mesh.export(str(baseline_path))
    print(f"    ✓ Saved: {baseline_path}")
    
    # Week 4 - Some fat loss in waist
    print("  Creating Week 4 mesh (fat loss in waist)...")
    week4_mesh = generate_body_mesh(version=2, changes={'waist': -0.3, 'thighs': -0.2})
    week4_path = output_path / "user1_week4.obj"
    week4_mesh.export(str(week4_path))
    print(f"    ✓ Saved: {week4_path}")
    
    # Week 8 - More fat loss, some muscle gain in chest/arms
    print("  Creating Week 8 mesh (fat loss + muscle gain)...")
    week8_mesh = generate_body_mesh(version=3, changes={
        'waist': -0.5,
        'thighs': -0.3,
        'chest': 0.2,
        'arms': 0.15
    })
    week8_path = output_path / "user1_week8.obj"
    week8_mesh.export(str(week8_path))
    print(f"    ✓ Saved: {week8_path}")
    
    # Week 12 - Continued progress
    print("  Creating Week 12 mesh (continued progress)...")
    week12_mesh = generate_body_mesh(version=4, changes={
        'waist': -0.6,
        'thighs': -0.4,
        'chest': 0.3,
        'arms': 0.25
    })
    week12_path = output_path / "user1_week12.obj"
    week12_mesh.export(str(week12_path))
    print(f"    ✓ Saved: {week12_path}")
    
    return {
        'baseline': str(baseline_path),
        'week4': str(week4_path),
        'week8': str(week8_path),
        'week12': str(week12_path)
    }

def generate_bia_data(user_id=1, week=0):
    """Generate sample BIA (Bioelectrical Impedance Analysis) data."""
    # Simulate realistic BIA data that changes over time
    base_weight = 75.0  # kg
    base_fat = 25.0  # %
    base_muscle = 35.0  # %
    base_water = 55.0  # %
    
    # Changes over time (simulating fat loss and muscle gain)
    weight_change = -week * 0.5  # Lose 0.5kg per week
    fat_change = -week * 0.8  # Lose 0.8% fat per week
    muscle_change = week * 0.3  # Gain 0.3% muscle per week
    water_change = week * 0.2  # Slight increase in water
    
    return {
        'user_id': user_id,
        'week': week,
        'weight': round(base_weight + weight_change, 1),
        'bmi': round((base_weight + weight_change) / (1.75 ** 2), 1),  # Assuming 1.75m height
        'fat_percentage': round(max(10.0, base_fat + fat_change), 1),  # Min 10%
        'muscle_percentage': round(min(45.0, base_muscle + muscle_change), 1),  # Max 45%
        'water_percentage': round(min(65.0, base_water + water_change), 1),  # Max 65%
        'recorded_at': (datetime.now() - timedelta(weeks=12-week)).isoformat()
    }

def generate_user_metadata(user_id=1):
    """Generate sample user metadata."""
    ages = [25, 28, 30, 32, 35, 28, 26, 33]
    countries = ['US', 'IN', 'CN', 'JP', 'UK', 'CA', 'AU', 'DE']
    genders = ['M', 'F']
    
    return {
        'user_id': user_id,
        'age': random.choice(ages),
        'gender': random.choice(genders),
        'country': random.choice(countries),
        'height_cm': random.randint(160, 185),
        'activity_level': random.choice(['sedentary', 'moderate', 'active', 'very_active']),
        'goal': random.choice(['fat_loss', 'muscle_gain', 'recomposition', 'maintenance'])
    }

def generate_all_sample_data():
    """Generate all sample data files."""
    print("=" * 60)
    print("Generating Sample Data for 3D Body Progress Engine")
    print("=" * 60)
    print()
    
    # Create output directories
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)
    
    meshes_dir = sample_dir / "meshes"
    metadata_dir = sample_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    # Generate meshes
    mesh_files = generate_sample_meshes(str(meshes_dir))
    print()
    
    # Generate BIA data for each week
    print("Generating BIA (Bioelectrical Impedance Analysis) data...")
    bia_data = []
    for week in [0, 4, 8, 12]:
        bia = generate_bia_data(user_id=1, week=week)
        bia_data.append(bia)
        print(f"  Week {week}: Weight={bia['weight']}kg, Fat={bia['fat_percentage']}%, Muscle={bia['muscle_percentage']}%")
    
    # Save BIA data
    bia_file = metadata_dir / "user1_bia_data.json"
    with open(bia_file, 'w') as f:
        json.dump(bia_data, f, indent=2)
    print(f"    ✓ Saved: {bia_file}")
    print()
    
    # Generate user metadata
    print("Generating user metadata...")
    user_meta = generate_user_metadata(user_id=1)
    user_file = metadata_dir / "user1_metadata.json"
    with open(user_file, 'w') as f:
        json.dump(user_meta, f, indent=2)
    print(f"    ✓ Saved: {user_file}")
    print(f"    User: Age={user_meta['age']}, Country={user_meta['country']}, Goal={user_meta['goal']}")
    print()
    
    # Create upload mapping file
    upload_mapping = {
        'user_id': 1,
        'uploads': [
            {
                'week': 0,
                'file': mesh_files['baseline'],
                'is_baseline': True,
                'bia_data': bia_data[0]
            },
            {
                'week': 4,
                'file': mesh_files['week4'],
                'is_baseline': False,
                'bia_data': bia_data[1]
            },
            {
                'week': 8,
                'file': mesh_files['week8'],
                'is_baseline': False,
                'bia_data': bia_data[2]
            },
            {
                'week': 12,
                'file': mesh_files['week12'],
                'is_baseline': False,
                'bia_data': bia_data[3]
            }
        ]
    }
    
    mapping_file = sample_dir / "upload_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(upload_mapping, f, indent=2)
    print(f"✓ Upload mapping saved: {mapping_file}")
    print()
    
    print("=" * 60)
    print("✓ Sample data generation complete!")
    print("=" * 60)
    print()
    print("Generated files:")
    print(f"  - Meshes: {meshes_dir}/")
    print(f"  - Metadata: {metadata_dir}/")
    print(f"  - Upload mapping: {mapping_file}")
    print()
    print("You can now use these files to test the system!")
    print()
    print("To upload via API:")
    print("  curl -X POST 'http://localhost:8000/api/upload' \\")
    print("    -F 'file=@sample_data/meshes/user1_week0.obj' \\")
    print("    -F 'user_id=1'")
    print()

if __name__ == "__main__":
    try:
        generate_all_sample_data()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

