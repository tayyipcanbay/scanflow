"""
Generate 3D mesh files for different body types and create comparison outputs.
"""
import numpy as np
import trimesh
from pathlib import Path
import json
from datetime import datetime, timedelta

def generate_body_type_mesh(
    body_type="overweight",
    gender="M",
    age=45,
    height_cm=172,
    weight_kg=105,
    fat_distribution=None,
    muscle_distribution=None
):
    """
    Generate 3D body mesh for different body types.
    
    Body types: overweight, normal, athletic, muscular, slim
    """
    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    # Default distributions based on body type
    if fat_distribution is None:
        if body_type == "overweight":
            fat_distribution = {
                'belly': 0.85,
                'thighs': 0.75,
                'arms': 0.40,
                'chest': 0.60
            }
        elif body_type == "normal":
            fat_distribution = {
                'belly': 0.50,
                'thighs': 0.45,
                'arms': 0.30,
                'chest': 0.40
            }
        elif body_type == "athletic":
            fat_distribution = {
                'belly': 0.30,
                'thighs': 0.35,
                'arms': 0.25,
                'chest': 0.30
            }
        elif body_type == "muscular":
            fat_distribution = {
                'belly': 0.20,
                'thighs': 0.25,
                'arms': 0.20,
                'chest': 0.25
            }
        else:  # slim
            fat_distribution = {
                'belly': 0.25,
                'thighs': 0.30,
                'arms': 0.20,
                'chest': 0.25
            }
    
    if muscle_distribution is None:
        if body_type == "overweight":
            muscle_distribution = {
                'arms': 0.25,
                'legs': 0.35,
                'chest': 0.30
            }
        elif body_type == "normal":
            muscle_distribution = {
                'arms': 0.40,
                'legs': 0.45,
                'chest': 0.40
            }
        elif body_type == "athletic":
            muscle_distribution = {
                'arms': 0.60,
                'legs': 0.65,
                'chest': 0.55
            }
        elif body_type == "muscular":
            muscle_distribution = {
                'arms': 0.75,
                'legs': 0.70,
                'chest': 0.70
            }
        else:  # slim
            muscle_distribution = {
                'arms': 0.35,
                'legs': 0.40,
                'chest': 0.35
            }
    
    # Create base mesh
    mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    
    # Scale to height
    height_scale = height_cm / 200.0
    width_scale = 0.4 * (1 + (bmi - 22) * 0.1)
    depth_scale = 0.35 * (1 + (bmi - 22) * 0.1)
    
    mesh.vertices[:, 0] *= width_scale
    mesh.vertices[:, 1] *= height_scale
    mesh.vertices[:, 2] *= depth_scale
    mesh.vertices[:, 1] -= height_scale * 0.5
    
    # Apply fat and muscle distribution
    for i, vertex in enumerate(mesh.vertices):
        y_pos = vertex[1]
        x_pos = abs(vertex[0])
        z_pos = abs(vertex[2])
        
        # Belly region
        if -0.1 < y_pos < 0.3 and z_pos > 0.1:
            fat_factor = fat_distribution['belly']
            direction = np.array([0, 0, 1])
            expansion = fat_factor * 0.2
            mesh.vertices[i] += direction * expansion
        
        # Thighs region
        elif -0.8 < y_pos < -0.2:
            fat_factor = fat_distribution['thighs']
            direction = vertex.copy()
            direction[1] = 0
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
                expansion = fat_factor * 0.15
                mesh.vertices[i] += direction * expansion
        
        # Chest region
        elif 0.2 < y_pos < 0.6 and z_pos > 0.05:
            fat_factor = fat_distribution['chest']
            muscle_factor = muscle_distribution['chest']
            direction = np.array([0, 0, 1])
            expansion = (fat_factor * 0.1) + (muscle_factor * 0.08)
            mesh.vertices[i] += direction * expansion
        
        # Arms region
        elif 0.0 < y_pos < 0.5 and x_pos > 0.2:
            fat_factor = fat_distribution['arms']
            muscle_factor = muscle_distribution['arms']
            direction = np.array([1 if vertex[0] > 0 else -1, 0, 0])
            expansion = (fat_factor * 0.08) + (muscle_factor * 0.1)
            mesh.vertices[i] += direction * expansion
    
    # Age-related changes
    if age > 40:
        age_factor = (age - 40) / 30.0
        upper_mask = mesh.vertices[:, 1] > 0.1
        mesh.vertices[upper_mask, 1] -= age_factor * 0.05
        mesh.vertices[upper_mask, 2] += age_factor * 0.03
    
    mesh.fix_normals()
    mesh.remove_unreferenced_vertices()
    
    return mesh

def create_comparison_mesh_with_colors(
    baseline_mesh,
    comparison_mesh,
    output_path
):
    """
    Create a single comparison mesh file with color-coded vertices.
    The mesh uses vertex colors to show increase (red) and decrease (green).
    """
    # Ensure same topology
    if len(baseline_mesh.vertices) != len(comparison_mesh.vertices):
        raise ValueError("Meshes must have same vertex count")
    
    # Calculate displacements
    displacements = comparison_mesh.vertices - baseline_mesh.vertices
    
    # Calculate magnitudes
    magnitudes = np.linalg.norm(displacements, axis=1)
    
    # Project onto normals
    if hasattr(baseline_mesh, 'vertex_normals') and baseline_mesh.vertex_normals is not None:
        normals = baseline_mesh.vertex_normals
    else:
        baseline_mesh.fix_normals()
        normals = baseline_mesh.vertex_normals
    
    projections = np.array([
        np.dot(displacements[i], normals[i]) if np.linalg.norm(normals[i]) > 0 else 0
        for i in range(len(displacements))
    ])
    
    # Create color mapping
    max_proj = np.max(np.abs(projections)) if np.max(np.abs(projections)) > 0 else 1.0
    normalized_proj = projections / max_proj
    
    # Generate vertex colors (RGB)
    vertex_colors = []
    for proj in normalized_proj:
        if proj < -0.01:  # Decrease - Green
            intensity = min(abs(proj), 1.0)
            vertex_colors.append([0, int(255 * intensity), 0])
        elif proj > 0.01:  # Increase - Red
            intensity = min(proj, 1.0)
            vertex_colors.append([int(255 * intensity), 0, 0])
        else:  # No change - White
            vertex_colors.append([255, 255, 255])
    
    vertex_colors = np.array(vertex_colors, dtype=np.uint8)
    
    # Use comparison mesh as base (the "after" state)
    comparison_mesh.visual.vertex_colors = vertex_colors
    
    # Export as OBJ with MTL file for colors
    comparison_mesh.export(str(output_path))
    
    # Also create MTL file for proper color rendering
    mtl_path = output_path.with_suffix('.mtl')
    with open(mtl_path, 'w') as f:
        f.write("newmtl Material\n")
        f.write("Ka 1.000 1.000 1.000\n")
        f.write("Kd 1.000 1.000 1.000\n")
        f.write("Ks 0.000 0.000 0.000\n")
        f.write("d 1.0\n")
        f.write("illum 1\n")
    
    # Update OBJ to reference MTL
    obj_content = Path(output_path).read_text()
    if "mtllib" not in obj_content:
        obj_content = f"mtllib {mtl_path.name}\nusemtl Material\n" + obj_content
        Path(output_path).write_text(obj_content)
    
    return {
        'mesh': comparison_mesh,
        'colors': vertex_colors,
        'projections': projections,
        'magnitudes': magnitudes,
        'displacements': displacements
    }

def generate_body_type_dataset():
    """Generate dataset of different body types."""
    print("=" * 60)
    print("Generating Body Type Dataset")
    print("=" * 60)
    print()
    
    output_dir = Path("sample_data/body_types")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    body_types = [
        ("overweight", 105, 35.5, "M", 45),
        ("normal", 75, 25.3, "M", 30),
        ("athletic", 80, 27.0, "M", 28),
        ("muscular", 85, 28.7, "M", 32),
        ("slim", 65, 22.0, "F", 25)
    ]
    
    dataset = {}
    
    for body_type, weight, bmi, gender, age in body_types:
        print(f"Generating {body_type} body type...")
        
        # Baseline (current state)
        baseline_mesh = generate_body_type_mesh(
            body_type=body_type,
            gender=gender,
            age=age,
            height_cm=172,
            weight_kg=weight
        )
        
        baseline_path = output_dir / f"{body_type}_baseline.obj"
        baseline_mesh.export(str(baseline_path))
        print(f"  ✓ Baseline: {baseline_path}")
        
        # Create "after" state (transformed)
        if body_type == "overweight":
            # Transform to normal/athletic
            after_weight = weight - 20
            after_mesh = generate_body_type_mesh(
                body_type="normal",
                gender=gender,
                age=age,
                height_cm=172,
                weight_kg=after_weight
            )
        elif body_type == "normal":
            # Transform to athletic
            after_weight = weight + 5
            after_mesh = generate_body_type_mesh(
                body_type="athletic",
                gender=gender,
                age=age,
                height_cm=172,
                weight_kg=after_weight
            )
        else:
            # Slight improvement
            after_mesh = generate_body_type_mesh(
                body_type=body_type,
                gender=gender,
                age=age,
                height_cm=172,
                weight_kg=weight - 5
            )
        
        after_path = output_dir / f"{body_type}_after.obj"
        after_mesh.export(str(after_path))
        print(f"  ✓ After: {after_path}")
        
        # Create comparison mesh with colors
        comparison_path = output_dir / f"{body_type}_comparison.obj"
        comparison_data = create_comparison_mesh_with_colors(
            baseline_mesh,
            after_mesh,
            comparison_path
        )
        print(f"  ✓ Comparison: {comparison_path}")
        print()
        
        dataset[body_type] = {
            'baseline': str(baseline_path),
            'after': str(after_path),
            'comparison': str(comparison_path),
            'weight_kg': weight,
            'bmi': bmi,
            'gender': gender,
            'age': age
        }
    
    # Save dataset info
    dataset_file = output_dir / "dataset_info.json"
    with open(dataset_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    print(f"✓ Dataset info saved: {dataset_file}")
    print()
    
    print("=" * 60)
    print("✓ Body type dataset generation complete!")
    print("=" * 60)
    print()
    print("Generated files:")
    for body_type, data in dataset.items():
        print(f"  {body_type}:")
        print(f"    - Baseline: {Path(data['baseline']).name}")
        print(f"    - After: {Path(data['after']).name}")
        print(f"    - Comparison (with colors): {Path(data['comparison']).name}")
    print()
    print("The comparison files contain vertex colors:")
    print("  🟢 Green vertices = Volume decrease (fat loss)")
    print("  🔴 Red vertices = Volume increase (muscle gain)")
    print("  ⚪ White vertices = No significant change")

if __name__ == "__main__":
    try:
        generate_body_type_dataset()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

