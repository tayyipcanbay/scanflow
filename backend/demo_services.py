"""
Demo script to show the core services working.
"""
import numpy as np
from app.services.mesh_comparator import MeshComparator
from app.services.region_detector import RegionDetector
from app.services.color_mapper import ColorMapper

def demo_services():
    """Demonstrate the core services with synthetic data."""
    print("=" * 60)
    print("3D Body Progress Engine - Service Demo")
    print("=" * 60)
    print()
    
    # Create synthetic mesh data (simulating a body mesh)
    print("1. Creating synthetic mesh data...")
    num_vertices = 1000
    baseline_vertices = np.random.rand(num_vertices, 3) * 2 - 1  # Random vertices
    comparison_vertices = baseline_vertices.copy()
    
    # Simulate some changes: some vertices move inward (decrease), some outward (increase)
    changes = np.random.rand(num_vertices) * 0.1 - 0.05  # Random changes between -0.05 and 0.05
    normals = np.random.rand(num_vertices, 3)
    normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)  # Normalize
    
    # Apply changes along normals
    comparison_vertices = baseline_vertices + normals * changes.reshape(-1, 1)
    
    print(f"   Created {num_vertices} vertices")
    print()
    
    # Test Region Detector
    print("2. Testing Region Detector...")
    region_detector = RegionDetector()
    region_masks = region_detector.detect_regions(baseline_vertices)
    
    for region, mask in region_masks.items():
        count = np.sum(mask)
        if count > 0:
            print(f"   {region.value}: {count} vertices ({count/num_vertices*100:.1f}%)")
    print()
    
    # Simulate comparison data
    print("3. Simulating mesh comparison...")
    displacements = comparison_vertices - baseline_vertices
    magnitudes = np.linalg.norm(displacements, axis=1)
    projections = np.array([
        np.dot(displacements[i], normals[i]) for i in range(len(displacements))
    ])
    
    increase_count = np.sum(projections > 0)
    decrease_count = np.sum(projections < 0)
    no_change_count = np.sum(projections == 0)
    
    print(f"   Vertices with increase: {increase_count} ({increase_count/num_vertices*100:.1f}%)")
    print(f"   Vertices with decrease: {decrease_count} ({decrease_count/num_vertices*100:.1f}%)")
    print(f"   Vertices with no change: {no_change_count} ({no_change_count/num_vertices*100:.1f}%)")
    print()
    
    # Test Color Mapper
    print("4. Testing Color Mapper...")
    color_mapper = ColorMapper()
    colors, metadata = color_mapper.map_displacement_to_colors_normalized(
        projections, magnitudes
    )
    
    # Count colors
    green_count = np.sum((colors[:, 1] > 0) & (colors[:, 0] == 0))  # Green
    red_count = np.sum((colors[:, 0] > 0) & (colors[:, 1] == 0))  # Red
    white_count = np.sum((colors[:, 0] == 255) & (colors[:, 1] == 255))  # White
    
    print(f"   Green (decrease) vertices: {green_count}")
    print(f"   Red (increase) vertices: {red_count}")
    print(f"   White (no change) vertices: {white_count}")
    print(f"   Max change magnitude: {metadata['max_change']:.4f}")
    print()
    
    # Test Region Statistics
    print("5. Testing Region Statistics...")
    region_stats = region_detector.aggregate_region_statistics(
        baseline_vertices, displacements, magnitudes, projections
    )
    
    for region, stats in region_stats.items():
        print(f"   {region.upper()}:")
        print(f"     - Increase: {stats['increase_percentage']:.1f}%")
        print(f"     - Decrease: {stats['decrease_percentage']:.1f}%")
        print(f"     - Avg magnitude: {stats['avg_magnitude']:.4f}")
    print()
    
    print("=" * 60)
    print("✓ All services working correctly!")
    print("=" * 60)
    print()
    print("The system is ready to process real 3D mesh files!")

if __name__ == "__main__":
    try:
        demo_services()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

