"""
Streamlit app with side-by-side comparison view like the reference image.
"""
import streamlit as st
import numpy as np
import trimesh
import plotly.graph_objects as go
from pathlib import Path
import tempfile
import os

# Import our services
from app.services.mesh_processor import MeshProcessor
from app.services.mesh_comparator import MeshComparator
from app.services.region_detector import RegionDetector
from app.services.color_mapper import ColorMapper
from app.services.insights_engine import InsightsEngine

# Page config
st.set_page_config(
    page_title="3D Body Progress - Side by Side",
    page_icon="🏆",
    layout="wide"
)

# Initialize services
@st.cache_resource
def get_services():
    return {
        'processor': MeshProcessor(),
        'comparator': MeshComparator(),
        'region_detector': RegionDetector(),
        'color_mapper': ColorMapper(),
        'insights_engine': InsightsEngine()
    }

services = get_services()

# Title
st.title("🏆 3D Body Progress Engine")
st.markdown("**Side-by-Side Comparison with Color-Coded Deformation**")
st.markdown("---")

# Sidebar
st.sidebar.header("📤 Upload Meshes")
st.sidebar.markdown("Upload baseline and comparison 3D mesh files")

baseline_file = st.sidebar.file_uploader(
    "Baseline Mesh (Before)",
    type=['obj', 'glb', 'fbx'],
    key="baseline"
)

comparison_file = st.sidebar.file_uploader(
    "Comparison Mesh (After)",
    type=['obj', 'glb', 'fbx'],
    key="comparison"
)

# Date inputs
col1, col2 = st.sidebar.columns(2)
with col1:
    baseline_date = st.date_input("Baseline Date", value=None, key="baseline_date")
with col2:
    baseline_time = st.time_input("Baseline Time", value=None, key="baseline_time")

col3, col4 = st.sidebar.columns(2)
with col3:
    comparison_date = st.date_input("Comparison Date", value=None, key="comparison_date")
with col4:
    comparison_time = st.time_input("Comparison Time", value=None, key="comparison_time")

# Color legend
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Color Legend")
st.sidebar.markdown("""
- 🟢 **Green** = Volume Reduction (Fat Loss)
- 🔴 **Red** = Volume Increase (Muscle Gain)
- ⚪ **White** = No Significant Change
""")

# Main content
if baseline_file and comparison_file:
    with st.spinner("Processing meshes and generating comparison..."):
        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(baseline_file.name).suffix) as tmp_baseline:
            tmp_baseline.write(baseline_file.getvalue())
            tmp_baseline_path = tmp_baseline.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(comparison_file.name).suffix) as tmp_comparison:
            tmp_comparison.write(comparison_file.getvalue())
            tmp_comparison_path = tmp_comparison.name
        
        try:
            # Process meshes
            baseline_data = services['processor'].process_mesh_file(Path(tmp_baseline_path))
            comparison_data = services['processor'].process_mesh_file(Path(tmp_comparison_path))
            
            # Compare meshes
            comparison_result = services['comparator'].compare_meshes(
                baseline_data, comparison_data, align=True
            )
            
            # Get statistics
            stats = services['comparator'].get_displacement_statistics(comparison_result)
            
            # Detect regions
            region_stats = services['region_detector'].aggregate_region_statistics(
                comparison_result["baseline_vertices"],
                comparison_result["displacements"],
                comparison_result["magnitudes"],
                comparison_result["projections"]
            )
            
            # Generate colors
            colors, color_metadata = services['color_mapper'].map_displacement_to_colors_normalized(
                comparison_result["projections"],
                comparison_result["magnitudes"]
            )
            
            # Generate insights
            insights = services['insights_engine'].generate_insights(
                stats, region_stats, None
            )
            
            # Side-by-side comparison view
            st.subheader("📊 Side-by-Side Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Baseline (Before)")
                baseline_date_str = baseline_date.strftime("%Y-%m-%d") if baseline_date else "N/A"
                baseline_time_str = baseline_time.strftime("%I:%M %p") if baseline_time else ""
                st.caption(f"📅 {baseline_date_str} ({baseline_time_str})")
                
                # Baseline mesh visualization
                baseline_vertices = comparison_result["baseline_vertices"]
                baseline_faces = baseline_data["faces"]
                
                fig_baseline = go.Figure(data=[
                    go.Mesh3d(
                        x=baseline_vertices[:, 0],
                        y=baseline_vertices[:, 1],
                        z=baseline_vertices[:, 2],
                        i=baseline_faces[:, 0] if len(baseline_faces) > 0 else [],
                        j=baseline_faces[:, 1] if len(baseline_faces) > 0 else [],
                        k=baseline_faces[:, 2] if len(baseline_faces) > 0 else [],
                        color='lightgray',
                        opacity=0.8,
                        name='Baseline'
                    )
                ])
                
                fig_baseline.update_layout(
                    title="Baseline Mesh",
                    scene=dict(
                        xaxis_title="Width",
                        yaxis_title="Height",
                        zaxis_title="Depth",
                        aspectmode='data',
                        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                    ),
                    height=500,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                
                st.plotly_chart(fig_baseline, use_container_width=True)
            
            with col2:
                st.markdown("### Current (After)")
                comparison_date_str = comparison_date.strftime("%Y-%m-%d") if comparison_date else "N/A"
                comparison_time_str = comparison_time.strftime("%I:%M %p") if comparison_time else ""
                st.caption(f"📅 {comparison_date_str} ({comparison_time_str})")
                
                # Comparison mesh with colors
                comparison_vertices = comparison_result["comparison_vertices"]
                comparison_faces = comparison_data["faces"]
                
                # Normalize colors for Plotly
                colors_normalized = colors / 255.0
                projections = comparison_result["projections"]
                max_proj = np.max(np.abs(projections)) if np.max(np.abs(projections)) > 0 else 1.0
                normalized_proj = (projections / max_proj + 1) / 2  # Map to [0,1]
                
                fig_comparison = go.Figure()
                
                # Add mesh with color gradation
                if len(comparison_faces) > 0:
                    fig_comparison.add_trace(go.Mesh3d(
                        x=comparison_vertices[:, 0],
                        y=comparison_vertices[:, 1],
                        z=comparison_vertices[:, 2],
                        i=comparison_faces[:, 0],
                        j=comparison_faces[:, 1],
                        k=comparison_faces[:, 2],
                        intensity=normalized_proj,
                        colorscale=[[0, 'rgb(0,255,0)'], [0.5, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']],
                        name='Comparison',
                        showscale=True,
                        colorbar=dict(
                            title=dict(
                                text="Change",
                                side="right"
                            ),
                            len=0.5
                        ),
                        opacity=0.8
                    ))
                else:
                    # Fallback to scatter if no faces
                    fig_comparison.add_trace(go.Scatter3d(
                        x=comparison_vertices[:, 0],
                        y=comparison_vertices[:, 1],
                        z=comparison_vertices[:, 2],
                        mode='markers',
                        marker=dict(
                            size=3,
                            color=normalized_proj,
                            colorscale=[[0, 'rgb(0,255,0)'], [0.5, 'rgb(255,255,255)'], [1, 'rgb(255,0,0)']],
                            showscale=True,
                            opacity=0.8
                        ),
                        name='Comparison'
                    ))
                
                fig_comparison.update_layout(
                    title="Current Mesh (Color-Coded)",
                    scene=dict(
                        xaxis_title="Width",
                        yaxis_title="Height",
                        zaxis_title="Depth",
                        aspectmode='data',
                        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                    ),
                    height=500,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                
                st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Statistics
            st.markdown("---")
            st.subheader("📊 Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Change", f"{stats['avg_magnitude']:.4f}")
            with col2:
                st.metric("Max Change", f"{stats['max_magnitude']:.4f}")
            with col3:
                st.metric("Increase", f"{stats['increase_percentage']:.1f}%", delta="Volume gain")
            with col4:
                st.metric("Decrease", f"{stats['decrease_percentage']:.1f}%", delta="Volume loss")
            
            # Region breakdown
            st.markdown("---")
            st.subheader("🗺️ Region Breakdown")
            
            for region, region_data in region_stats.items():
                with st.expander(region.replace('_', ' ').title()):
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Increase", f"{region_data['increase_percentage']:.1f}%")
                    with col_b:
                        st.metric("Decrease", f"{region_data['decrease_percentage']:.1f}%")
                    with col_c:
                        st.metric("Avg Magnitude", f"{region_data['avg_magnitude']:.4f}")
            
            # Insights
            st.markdown("---")
            st.subheader("🧠 AI Insights")
            st.info(insights['text'])
            st.caption(f"Confidence: {insights['confidence']*100:.0f}%")
            
            # Export comparison mesh
            st.markdown("---")
            st.subheader("💾 Export Comparison Mesh")
            
            # Create comparison mesh with vertex colors
            from app.services.color_mapper import ColorMapper
            color_mapper = ColorMapper()
            
            # Save comparison mesh
            comparison_mesh_obj = trimesh.Trimesh(
                vertices=comparison_vertices,
                faces=comparison_faces if len(comparison_faces) > 0 else [],
                vertex_colors=colors
            )
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.obj') as tmp_export:
                comparison_mesh_obj.export(tmp_export.name)
                export_path = tmp_export.name
            
            with open(export_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Comparison Mesh (with colors)",
                    data=f.read(),
                    file_name="comparison_mesh.obj",
                    mime="application/octet-stream"
                )
            
            st.caption("This mesh file contains vertex colors showing increase (red) and decrease (green)")
        
        except Exception as e:
            st.error(f"Error processing meshes: {str(e)}")
            st.exception(e)
        
        finally:
            # Cleanup temp files
            try:
                os.unlink(tmp_baseline_path)
                os.unlink(tmp_comparison_path)
                if 'export_path' in locals():
                    os.unlink(export_path)
            except:
                pass

elif baseline_file or comparison_file:
    st.warning("⚠️ Please upload both baseline and comparison meshes to compare.")
    
    if baseline_file:
        st.success(f"✓ Baseline mesh uploaded: {baseline_file.name}")
    if comparison_file:
        st.success(f"✓ Comparison mesh uploaded: {comparison_file.name}")

else:
    st.info("👆 Upload two 3D mesh files in the sidebar to get started!")
    
    st.markdown("### 📋 How to Use:")
    st.markdown("""
    1. **Upload Baseline Mesh**: Your initial body scan (Before)
    2. **Upload Comparison Mesh**: Your later body scan (After)
    3. **Set Dates**: Optionally set dates/times for each scan
    4. **View Results**: 
       - Side-by-side comparison view
       - Color-coded deformation visualization
       - Statistics and region breakdown
       - AI-generated insights
    5. **Export**: Download the comparison mesh with embedded colors
    """)
    
    st.markdown("### 🎯 Supported Formats:")
    st.markdown("- **OBJ** (.obj) - Recommended")
    st.markdown("- **GLB** (.glb)")
    st.markdown("- **FBX** (.fbx)")

