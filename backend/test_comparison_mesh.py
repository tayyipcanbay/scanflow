"""
Test script to generate and verify comparison mesh with colors.
"""
import numpy as np
import trimesh
from pathlib import Path
from generate_body_types import generate_body_type_mesh, create_comparison_mesh_with_colors

def test_comparison_mesh_generation():
    """Test generating comparison mesh with colors."""
    print("=" * 60)
    print("Testing Comparison Mesh Generation")
    print("=" * 60)
    print()
    
    # Create output directory
    output_dir = Path("sample_data/test_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate baseline (overweight)
    print("1. Generating baseline mesh (overweight body type)...")
    baseline_mesh = generate_body_type_mesh(
        body_type="overweight",
        gender="M",
        age=45,
        height_cm=172,
        weight_kg=105
    )
    baseline_path = output_dir / "test_baseline.obj"
    baseline_mesh.export(str(baseline_path))
    print(f"   ✓ Saved: {baseline_path}")
    print(f"   Vertices: {len(baseline_mesh.vertices)}")
    print()
    
    # Generate comparison (normal/athletic)
    print("2. Generating comparison mesh (transformed body)...")
    comparison_mesh = generate_body_type_mesh(
        body_type="normal",
        gender="M",
        age=45,
        height_cm=172,
        weight_kg=85  # Lost 20kg
    )
    comparison_path = output_dir / "test_comparison_raw.obj"
    comparison_mesh.export(str(comparison_path))
    print(f"   ✓ Saved: {comparison_path}")
    print(f"   Vertices: {len(comparison_mesh.vertices)}")
    print()
    
    # Create comparison mesh with colors
    print("3. Creating comparison mesh with color-coded vertices...")
    comparison_output = output_dir / "test_comparison_colored.obj"
    
    try:
        result = create_comparison_mesh_with_colors(
            baseline_mesh,
            comparison_mesh,
            comparison_output
        )
        print(f"   ✓ Saved: {comparison_output}")
        print(f"   ✓ MTL file: {comparison_output.with_suffix('.mtl')}")
        print()
        
        # Analyze colors
        colors = result['colors']
        projections = result['projections']
        
        green_count = np.sum((colors[:, 1] > 200) & (colors[:, 0] < 50))
        red_count = np.sum((colors[:, 0] > 200) & (colors[:, 1] < 50))
        white_count = np.sum((colors[:, 0] > 200) & (colors[:, 1] > 200))
        
        print("4. Color Analysis:")
        print(f"   🟢 Green vertices (decrease): {green_count} ({green_count/len(colors)*100:.1f}%)")
        print(f"   🔴 Red vertices (increase): {red_count} ({red_count/len(colors)*100:.1f}%)")
        print(f"   ⚪ White vertices (no change): {white_count} ({white_count/len(colors)*100:.1f}%)")
        print()
        
        print("5. Statistics:")
        print(f"   Average magnitude: {np.mean(result['magnitudes']):.4f}")
        print(f"   Max magnitude: {np.max(result['magnitudes']):.4f}")
        print(f"   Average projection: {np.mean(projections):.4f}")
        print()
        
        print("=" * 60)
        print("✓ Test successful!")
        print("=" * 60)
        print()
        print("Generated files:")
        print(f"  - Baseline: {baseline_path}")
        print(f"  - Comparison (raw): {comparison_path}")
        print(f"  - Comparison (colored): {comparison_output}")
        print()
        print("The colored comparison mesh can be opened in:")
        print("  - Blender")
        print("  - MeshLab")
        print("  - Any OBJ viewer that supports vertex colors")
        print()
        print("Colors represent:")
        print("  🟢 Green = Volume decrease (fat loss)")
        print("  🔴 Red = Volume increase (muscle gain)")
        print("  ⚪ White = No significant change")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comparison_mesh_generation()

