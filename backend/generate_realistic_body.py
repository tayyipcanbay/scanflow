"""
Generate realistic 3D body meshes based on human body specifications.
"""
import numpy as np
import trimesh
from pathlib import Path
import json
from datetime import datetime, timedelta

def generate_realistic_body_mesh(
    gender="M",
    age=45,
    height_cm=172,
    weight_kg=105,
    fat_distribution=None,
    muscle_distribution=None,
    version=1,
    changes=None
):
    """
    Generate a realistic 3D body mesh based on body specifications.
    
    Args:
        gender: "M" or "F"
        age: Age in years
        height_cm: Height in cm
        weight_kg: Weight in kg
        fat_distribution: Dict with belly, thighs, arms, chest (0-1)
        muscle_distribution: Dict with arms, legs, chest (0-1)
        version: Version number (1 = baseline, 2+ = with changes)
        changes: Dictionary with region changes (optional)
    
    Returns:
        trimesh.Trimesh object
    """
    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    # Default fat distribution if not provided
    if fat_distribution is None:
        fat_distribution = {
            'belly': 0.8,
            'thighs': 0.7,
            'arms': 0.3,
            'chest': 0.5
        }
    
    # Default muscle distribution if not provided
    if muscle_distribution is None:
        muscle_distribution = {
            'arms': 0.3,
            'legs': 0.4,
            'chest': 0.4
        }
    
    # Create base body mesh using icosphere
    # Higher subdivisions for more detail
    mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    
    # Scale to height (Y-axis is vertical)
    height_scale = height_cm / 200.0  # Normalize to reasonable scale
    width_scale = 0.4 * (1 + (bmi - 22) * 0.1)  # Width based on BMI
    depth_scale = 0.35 * (1 + (bmi - 22) * 0.1)  # Depth based on BMI
    
    # Apply base scaling
    mesh.vertices[:, 0] *= width_scale  # Width (left-right)
    mesh.vertices[:, 1] *= height_scale  # Height (vertical)
    mesh.vertices[:, 2] *= depth_scale  # Depth (front-back)
    
    # Center at origin (feet at bottom)
    mesh.vertices[:, 1] -= height_scale * 0.5
    
    # Apply fat distribution to vertices
    for i, vertex in enumerate(mesh.vertices):
        y_pos = vertex[1]  # Vertical position
        x_pos = abs(vertex[0])  # Distance from center (width)
        z_pos = abs(vertex[2])  # Distance from center (depth)
        
        # Belly region (middle abdomen, front)
        if -0.1 < y_pos < 0.3 and z_pos > 0.1:
            fat_factor = fat_distribution['belly']
            # Expand outward (increase volume)
            direction = np.array([0, 0, 1])  # Forward
            expansion = fat_factor * 0.2
            mesh.vertices[i] += direction * expansion
        
        # Thighs region (lower body, sides and front)
        elif -0.8 < y_pos < -0.2:
            fat_factor = fat_distribution['thighs']
            # Expand outward
            direction = vertex.copy()
            direction[1] = 0  # Horizontal only
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
                expansion = fat_factor * 0.15
                mesh.vertices[i] += direction * expansion
        
        # Chest region (upper body, front)
        elif 0.2 < y_pos < 0.6 and z_pos > 0.05:
            fat_factor = fat_distribution['chest']
            muscle_factor = muscle_distribution['chest']
            # Combine fat and muscle
            direction = np.array([0, 0, 1])  # Forward
            expansion = (fat_factor * 0.1) + (muscle_factor * 0.08)
            mesh.vertices[i] += direction * expansion
        
        # Arms region (sides, upper body)
        elif 0.0 < y_pos < 0.5 and x_pos > 0.2:
            fat_factor = fat_distribution['arms']
            muscle_factor = muscle_distribution['arms']
            # Arms are more vertical
            direction = np.array([1 if vertex[0] > 0 else -1, 0, 0])
            expansion = (fat_factor * 0.08) + (muscle_factor * 0.1)
            mesh.vertices[i] += direction * expansion
    
    # Apply age-related changes (slight sagging, less definition)
    if age > 40:
        age_factor = (age - 40) / 30.0  # 0-1 for ages 40-70
        # Slight downward shift in upper body
        upper_mask = mesh.vertices[:, 1] > 0.1
        mesh.vertices[upper_mask, 1] -= age_factor * 0.05
        mesh.vertices[upper_mask, 2] += age_factor * 0.03  # Slight forward lean
    
    # Apply changes if this is not baseline (for time progression)
    if version > 1 and changes:
        for i, vertex in enumerate(mesh.vertices):
            y_pos = vertex[1]
            x_pos = abs(vertex[0])
            z_pos = abs(vertex[2])
            
            # Waist/belly changes
            if -0.1 < y_pos < 0.3 and z_pos > 0.1:
                if 'waist' in changes or 'belly' in changes:
                    change = changes.get('waist', changes.get('belly', 0))
                    direction = np.array([0, 0, 1])
                    mesh.vertices[i] += direction * change * 0.15
            
            # Thigh changes
            elif -0.8 < y_pos < -0.2:
                if 'thighs' in changes:
                    change = changes['thighs']
                    direction = vertex.copy()
                    direction[1] = 0
                    if np.linalg.norm(direction) > 0:
                        direction = direction / np.linalg.norm(direction)
                        mesh.vertices[i] += direction * change * 0.12
            
            # Chest changes
            elif 0.2 < y_pos < 0.6 and z_pos > 0.05:
                if 'chest' in changes:
                    change = changes['chest']
                    direction = np.array([0, 0, 1])
                    mesh.vertices[i] += direction * change * 0.1
            
            # Arm changes
            elif 0.0 < y_pos < 0.5 and x_pos > 0.2:
                if 'arms' in changes:
                    change = changes['arms']
                    direction = np.array([1 if vertex[0] > 0 else -1, 0, 0])
                    mesh.vertices[i] += direction * change * 0.08
    
    # Ensure mesh is valid
    mesh.fix_normals()
    mesh.remove_duplicate_faces()
    mesh.remove_unreferenced_vertices()
    
    return mesh

def generate_body_specification():
    """Generate the body specification JSON."""
    return {
        "gender": "M",
        "age": 45,
        "height_cm": 172,
        "weight_kg": 105,
        "fat_distribution": {
            "belly": 0.85,  # High belly fat
            "thighs": 0.75,  # High thigh fat
            "arms": 0.25,  # Low arm fat
            "chest": 0.55  # Moderate chest fat
        },
        "muscle_distribution": {
            "arms": 0.25,  # Low (sedentary)
            "legs": 0.35,  # Low-moderate
            "chest": 0.30  # Low-moderate
        }
    }

def generate_progression_meshes(base_spec, output_dir="sample_data/meshes"):
    """Generate meshes showing progression over time."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Generating Realistic 3D Body Meshes")
    print("=" * 60)
    print()
    print(f"Base Specification:")
    print(f"  Gender: {base_spec['gender']}")
    print(f"  Age: {base_spec['age']}")
    print(f"  Height: {base_spec['height_cm']} cm")
    print(f"  Weight: {base_spec['weight_kg']} kg")
    print(f"  BMI: {base_spec['weight_kg'] / ((base_spec['height_cm']/100)**2):.1f}")
    print()
    
    # Week 0 - Baseline (current state)
    print("Creating Week 0 mesh (Baseline - Current state)...")
    week0_mesh = generate_realistic_body_mesh(
        gender=base_spec['gender'],
        age=base_spec['age'],
        height_cm=base_spec['height_cm'],
        weight_kg=base_spec['weight_kg'],
        fat_distribution=base_spec['fat_distribution'],
        muscle_distribution=base_spec['muscle_distribution'],
        version=1
    )
    week0_path = output_path / "realistic_week0.obj"
    week0_mesh.export(str(week0_path))
    print(f"  ✓ Saved: {week0_path}")
    print(f"    Vertices: {len(week0_mesh.vertices)}")
    print()
    
    # Week 4 - Initial fat loss
    print("Creating Week 4 mesh (Initial fat loss in belly/thighs)...")
    week4_mesh = generate_realistic_body_mesh(
        gender=base_spec['gender'],
        age=base_spec['age'],
        height_cm=base_spec['height_cm'],
        weight_kg=103.0,  # Lost 2kg
        fat_distribution=base_spec['fat_distribution'],
        muscle_distribution=base_spec['muscle_distribution'],
        version=2,
        changes={'belly': -0.15, 'thighs': -0.12}  # Fat loss
    )
    week4_path = output_path / "realistic_week4.obj"
    week4_mesh.export(str(week4_path))
    print(f"  ✓ Saved: {week4_path}")
    print(f"    Vertices: {len(week4_mesh.vertices)}")
    print()
    
    # Week 8 - More fat loss, some muscle gain
    print("Creating Week 8 mesh (More fat loss, some muscle gain)...")
    week8_mesh = generate_realistic_body_mesh(
        gender=base_spec['gender'],
        age=base_spec['age'],
        height_cm=base_spec['height_cm'],
        weight_kg=100.0,  # Lost 5kg total
        fat_distribution={
            'belly': 0.70,  # Reduced from 0.85
            'thighs': 0.60,  # Reduced from 0.75
            'arms': 0.20,  # Reduced from 0.25
            'chest': 0.45  # Reduced from 0.55
        },
        muscle_distribution={
            'arms': 0.30,  # Slight increase
            'legs': 0.40,  # Slight increase
            'chest': 0.35  # Slight increase
        },
        version=3,
        changes={'belly': -0.25, 'thighs': -0.20, 'chest': 0.08, 'arms': 0.05}
    )
    week8_path = output_path / "realistic_week8.obj"
    week8_mesh.export(str(week8_path))
    print(f"  ✓ Saved: {week8_path}")
    print(f"    Vertices: {len(week8_mesh.vertices)}")
    print()
    
    # Week 12 - Significant progress
    print("Creating Week 12 mesh (Significant progress)...")
    week12_mesh = generate_realistic_body_mesh(
        gender=base_spec['gender'],
        age=base_spec['age'],
        height_cm=base_spec['height_cm'],
        weight_kg=97.0,  # Lost 8kg total
        fat_distribution={
            'belly': 0.55,  # Significantly reduced
            'thighs': 0.45,  # Significantly reduced
            'arms': 0.15,  # Reduced
            'chest': 0.35  # Reduced
        },
        muscle_distribution={
            'arms': 0.35,  # Increased
            'legs': 0.45,  # Increased
            'chest': 0.40  # Increased
        },
        version=4,
        changes={'belly': -0.35, 'thighs': -0.30, 'chest': 0.15, 'arms': 0.12}
    )
    week12_path = output_path / "realistic_week12.obj"
    week12_mesh.export(str(week12_path))
    print(f"  ✓ Saved: {week12_path}")
    print(f"    Vertices: {len(week12_mesh.vertices)}")
    print()
    
    return {
        'baseline': str(week0_path),
        'week4': str(week4_path),
        'week8': str(week8_path),
        'week12': str(week12_path)
    }

def generate_bia_data_progression(base_weight=105.0, height_cm=172):
    """Generate BIA data progression."""
    height_m = height_cm / 100
    
    bia_data = []
    for week in [0, 4, 8, 12]:
        # Weight loss progression
        weight = base_weight - (week * 0.67)  # ~0.67kg per week
        bmi = weight / (height_m ** 2)
        
        # Fat percentage decreases
        base_fat = 28.0  # Starting at ~28% body fat
        fat_pct = base_fat - (week * 1.0)  # ~1% per week
        
        # Muscle percentage increases slightly
        base_muscle = 32.0
        muscle_pct = base_muscle + (week * 0.3)  # ~0.3% per week
        
        # Water percentage increases
        base_water = 52.0
        water_pct = base_water + (week * 0.2)
        
        bia_data.append({
            'user_id': 1,
            'week': week,
            'weight': round(weight, 1),
            'bmi': round(bmi, 1),
            'fat_percentage': round(max(15.0, fat_pct), 1),
            'muscle_percentage': round(min(40.0, muscle_pct), 1),
            'water_percentage': round(min(60.0, water_pct), 1),
            'recorded_at': (datetime.now() - timedelta(weeks=12-week)).isoformat()
        })
    
    return bia_data

def main():
    """Main function to generate all realistic body data."""
    print("=" * 60)
    print("Realistic 3D Body Mesh Generator")
    print("=" * 60)
    print()
    
    # Create output directories
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)
    
    meshes_dir = sample_dir / "meshes"
    metadata_dir = sample_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    # Generate body specification
    body_spec = generate_body_specification()
    
    # Save specification
    spec_file = metadata_dir / "realistic_body_spec.json"
    with open(spec_file, 'w') as f:
        json.dump(body_spec, f, indent=2)
    print(f"✓ Body specification saved: {spec_file}")
    print()
    
    # Generate meshes
    mesh_files = generate_progression_meshes(body_spec, str(meshes_dir))
    
    # Generate BIA data
    print("Generating BIA data progression...")
    bia_data = generate_bia_data_progression(
        base_weight=body_spec['weight_kg'],
        height_cm=body_spec['height_cm']
    )
    
    bia_file = metadata_dir / "realistic_bia_data.json"
    with open(bia_file, 'w') as f:
        json.dump(bia_data, f, indent=2)
    print(f"✓ BIA data saved: {bia_file}")
    print()
    
    # Print BIA progression
    print("BIA Data Progression:")
    for data in bia_data:
        print(f"  Week {data['week']:2d}: Weight={data['weight']:5.1f}kg, "
              f"BMI={data['bmi']:4.1f}, Fat={data['fat_percentage']:4.1f}%, "
              f"Muscle={data['muscle_percentage']:4.1f}%")
    print()
    
    # Create upload mapping
    upload_mapping = {
        'user_id': 1,
        'body_specification': body_spec,
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
    
    mapping_file = sample_dir / "realistic_upload_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(upload_mapping, f, indent=2)
    print(f"✓ Upload mapping saved: {mapping_file}")
    print()
    
    print("=" * 60)
    print("✓ Realistic body mesh generation complete!")
    print("=" * 60)
    print()
    print("Generated files:")
    print(f"  - Meshes: {meshes_dir}/")
    print(f"    - realistic_week0.obj (Baseline)")
    print(f"    - realistic_week4.obj")
    print(f"    - realistic_week8.obj")
    print(f"    - realistic_week12.obj")
    print(f"  - Metadata: {metadata_dir}/")
    print(f"    - realistic_body_spec.json")
    print(f"    - realistic_bia_data.json")
    print(f"  - Upload mapping: {mapping_file}")
    print()
    print("These meshes represent a realistic 45-year-old male body")
    print("with high belly/thigh fat showing progression over 12 weeks.")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

