# Quick Test - Generate Comparison Mesh

## Test the Comparison Mesh Generation

```bash
cd backend
source venv/bin/activate
python test_comparison_mesh.py
```

This will:
1. Generate a baseline mesh (overweight)
2. Generate a comparison mesh (transformed)
3. Create a single comparison mesh file with color-coded vertices
4. Show statistics about the colors

## Generate All Body Types

```bash
python generate_body_types.py
```

This creates:
- 5 different body types
- Baseline and "after" meshes for each
- **Comparison mesh files with embedded colors** (the output you want!)

## The Output Files

The `*_comparison.obj` files are **single mesh files** with:
- ✅ Same mesh structure as input
- ✅ Vertex colors embedded (green/red/white)
- ✅ Can be opened in Blender, MeshLab, etc.
- ✅ Shows increase/decrease directly in the mesh

## View in Streamlit

The cache error is harmless. Just:
1. Refresh your browser
2. Upload the baseline and comparison files
3. You'll see the side-by-side view

Or use the side-by-side viewer:
```bash
streamlit run streamlit_comparison_viewer.py
```

## What You Get

**Input Data:**
- `overweight_baseline.obj` - Before state
- `overweight_after.obj` - After state

**Output Data (Single File):**
- `overweight_comparison.obj` - **Single mesh with colors!**
  - Green vertices = decrease
  - Red vertices = increase
  - White vertices = no change

This is exactly what you asked for - one mesh file showing the comparison!

