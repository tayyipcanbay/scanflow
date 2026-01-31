# Streamlit App Guide - 3D Body Progress Visualization

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install streamlit plotly
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
# Option 1: Use the script
chmod +x run_streamlit.sh
./run_streamlit.sh

# Option 2: Manual
streamlit run streamlit_app.py
```

### 3. Open in Browser

The app will automatically open at: **http://localhost:8501**

## 📋 Features

### ✅ Upload & Compare
- Upload baseline mesh (Week 0)
- Upload comparison mesh (Week 4, 8, 12...)
- Automatic comparison and analysis

### ✅ 3D Visualization
- Interactive 3D mesh viewer
- Color-coded deformation:
  - 🟢 **Green** = Volume reduction (fat loss)
  - 🔴 **Red** = Volume increase (muscle gain)
  - ⚪ **White** = No significant change

### ✅ Statistics & Analysis
- Overall statistics (avg change, max change)
- Region breakdown (waist, chest, arms, thighs, hips)
- Change distribution charts
- Deformation analysis

### ✅ AI Insights
- Human-readable insights
- Confidence scores
- Region-specific analysis

### ✅ Export Results
- Download comparison results as JSON
- Save statistics and insights

## 🎯 How to Use

1. **Upload Files**:
   - Click "Browse files" in sidebar
   - Select baseline mesh (e.g., `realistic_week0.obj`)
   - Select comparison mesh (e.g., `realistic_week12.obj`)

2. **View Results**:
   - 3D visualization appears automatically
   - Rotate, zoom, and pan the mesh
   - See color gradation showing changes

3. **Analyze Data**:
   - Check statistics panel
   - Review region breakdown
   - Read AI insights

4. **Export**:
   - Click "Download Results" button
   - Save JSON file with all data

## 📊 Example Workflow

```bash
# 1. Generate sample data
python generate_realistic_body.py

# 2. Start Streamlit
streamlit run streamlit_app.py

# 3. In the browser:
#    - Upload: sample_data/meshes/realistic_week0.obj (baseline)
#    - Upload: sample_data/meshes/realistic_week12.obj (comparison)
#    - View the 3D visualization with color gradation!
```

## 🎨 Color Coding

- **Green Areas**: Volume decreased (fat loss, reduction)
- **Red Areas**: Volume increased (muscle gain, growth)
- **White/Gray Areas**: No significant change
- **Intensity**: Darker = more change, Lighter = less change

## 🔧 Troubleshooting

### Port Already in Use
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Module Not Found
```bash
pip install streamlit plotly
```

### Mesh Processing Error
- Make sure meshes have same topology
- Check file format (OBJ, GLB, FBX)
- Verify mesh files are valid

## 📝 Notes

- The app processes meshes in real-time
- Large meshes may take a few seconds
- Results are cached for faster re-rendering
- All processing happens locally (no API needed)

## 🎯 Supported File Formats

- **OBJ** (.obj) - Recommended
- **GLB** (.glb) - Binary format
- **FBX** (.fbx) - Autodesk format

Enjoy visualizing your body progress! 🏆

