"""
Process before_fitness.glb and after_fitness.glb to create comparison mesh.
"""
import numpy as np
import trimesh
from pathlib import Path
from app.services.mesh_processor import MeshProcessor
from app.services.mesh_comparator import MeshComparator
from app.services.color_mapper import ColorMapper

def process_fitness_comparison():
    """Process the before/after fitness GLB files."""
    print("=" * 60)
    print("Processing Fitness Comparison Files")
    print("=" * 60)
    print()
    
    # File paths - try multiple locations
    possible_before_paths = [
        Path("../before_fitness.glb"),  # Parent directory (from backend/)
        Path("before_fitness.glb"),  # Current directory
        Path("D:/2025/02_Course/Semester 3/000001_Cursor/before_fitness.glb"),  # Windows absolute
        Path("/mnt/d/2025/02_Course/Semester 3/000001_Cursor/before_fitness.glb"),  # WSL path
    ]
    
    before_path = None
    after_path = None
    
    for path in possible_before_paths:
        if path.exists():
            before_path = path
            # Find corresponding after file in same directory
            after_path = path.parent / "after_fitness.glb"
            if after_path.exists():
                break
    
    if before_path is None or not before_path.exists():
        print("❌ File not found: before_fitness.glb")
        print("Please make sure the files are accessible")
        print("Tried paths:")
        for p in possible_before_paths:
            print(f"  - {p}")
        return
    
    if after_path is None or not after_path.exists():
        print(f"❌ File not found: after_fitness.glb")
        print(f"Looked in: {before_path.parent}")
        return
    
    print(f"✓ Found before file: {before_path}")
    print(f"✓ Found after file: {after_path}")
    print()
    
    # Initialize services
    processor = MeshProcessor()
    comparator = MeshComparator()
    color_mapper = ColorMapper()
    
    # Process meshes
    print("1. Loading and processing meshes...")
    try:
        baseline_data = processor.process_mesh_file(before_path)
        print(f"   ✓ Baseline loaded: {len(baseline_data['vertices'])} vertices")
        
        comparison_data = processor.process_mesh_file(after_path)
        print(f"   ✓ Comparison loaded: {len(comparison_data['vertices'])} vertices")
        print()
    except Exception as e:
        print(f"   ✗ Error loading meshes: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Check topology compatibility
    print("2. Checking mesh compatibility...")
    topology_match, error_msg = processor.compare_topology(baseline_data, comparison_data)
    if not topology_match:
        print(f"   ⚠️  Topology mismatch: {error_msg}")
        print("   Attempting to align and process anyway...")
        print()
    
    # Compare meshes
    print("3. Comparing meshes...")
    try:
        comparison_result = comparator.compare_meshes(
            baseline_data, comparison_data, align=True
        )
        print("   ✓ Comparison complete")
        print()
    except Exception as e:
        print(f"   ✗ Error comparing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Get statistics
    stats = comparator.get_displacement_statistics(comparison_result)
    print("4. Statistics:")
    print(f"   Average change: {stats['avg_magnitude']:.4f}")
    print(f"   Max change: {stats['max_magnitude']:.4f}")
    print(f"   Increase: {stats['increase_percentage']:.1f}%")
    print(f"   Decrease: {stats['decrease_percentage']:.1f}%")
    print()
    
    # Generate colors
    print("5. Generating color mapping...")
    colors, color_metadata = color_mapper.map_displacement_to_colors_normalized(
        comparison_result["projections"],
        comparison_result["magnitudes"]
    )
    
    green_count = np.sum((colors[:, 1] > 200) & (colors[:, 0] < 50))
    red_count = np.sum((colors[:, 0] > 200) & (colors[:, 1] < 50))
    white_count = np.sum((colors[:, 0] > 200) & (colors[:, 1] > 200))
    
    print(f"   🟢 Green (decrease): {green_count} vertices ({green_count/len(colors)*100:.1f}%)")
    print(f"   🔴 Red (increase): {red_count} vertices ({red_count/len(colors)*100:.1f}%)")
    print(f"   ⚪ White (no change): {white_count} vertices ({white_count/len(colors)*100:.1f}%)")
    print()
    
    # Create output directory
    output_dir = Path("sample_data/fitness_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create comparison mesh with colors
    print("6. Creating comparison mesh with colors...")
    comparison_vertices = comparison_result["comparison_vertices"]
    comparison_faces = comparison_data["faces"]
    
    # Create mesh with vertex colors
    comparison_mesh = trimesh.Trimesh(
        vertices=comparison_vertices,
        faces=comparison_faces,
        vertex_colors=colors
    )
    
    # Export comparison mesh
    comparison_output = output_dir / "fitness_comparison_colored.obj"
    comparison_mesh.export(str(comparison_output))
    print(f"   ✓ Saved: {comparison_output}")
    
    # Also export as GLB if possible
    try:
        glb_output = output_dir / "fitness_comparison_colored.glb"
        comparison_mesh.export(str(glb_output))
        print(f"   ✓ Saved: {glb_output}")
    except:
        print("   ⚠️  GLB export not available, using OBJ format")
    
    print()
    
    # Save metadata
    metadata = {
        'baseline_file': str(before_path),
        'comparison_file': str(after_path),
        'statistics': stats,
        'color_metadata': color_metadata,
        'vertex_count': len(comparison_vertices),
        'face_count': len(comparison_faces)
    }
    
    import json
    metadata_file = output_dir / "fitness_comparison_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    print(f"✓ Metadata saved: {metadata_file}")
    print()
    
    print("=" * 60)
    print("✓ Processing complete!")
    print("=" * 60)
    print()
    print("Output files:")
    print(f"  - Comparison mesh (colored): {comparison_output}")
    print(f"  - Metadata: {metadata_file}")
    print()
    print("The comparison mesh file contains:")
    print("  🟢 Green vertices = Volume decrease (fat loss)")
    print("  🔴 Red vertices = Volume increase (muscle gain)")
    print("  ⚪ White vertices = No significant change")
    print()
    print("You can now:")
    print("  1. Open the mesh in Blender/MeshLab to view colors")
    print("  2. Upload to Streamlit for visualization")
    print("  3. Use in the HTML viewer")

if __name__ == "__main__":
    try:
        process_fitness_comparison()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

