"""
Streamlit app for 3D Body Progress Visualization
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
    page_title="3D Body Progress Engine",
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
st.markdown("Upload 3D mesh files to visualize body changes over time")
st.markdown("---")

# Sidebar
st.sidebar.header("📤 Upload Meshes")
st.sidebar.markdown("Upload your 3D body mesh files (GLB, OBJ, FBX)")

# File uploaders
baseline_file = st.sidebar.file_uploader(
    "Baseline Mesh (Before)",
    type=['obj', 'glb', 'fbx'],
    key="baseline",
    help="Upload your 'before' mesh file (e.g., before_fitness.glb)"
)

comparison_file = st.sidebar.file_uploader(
    "Comparison Mesh (After)",
    type=['obj', 'glb', 'fbx'],
    key="comparison",
    help="Upload your 'after' mesh file (e.g., after_fitness.glb)"
)

# Quick load buttons for fitness files
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Quick Load")
if st.sidebar.button("Load Fitness Files (before/after_fitness.glb)"):
    fitness_before = Path("../before_fitness.glb")
    fitness_after = Path("../after_fitness.glb")
    
    if fitness_before.exists() and fitness_after.exists():
        st.sidebar.success("Files found! Upload them using the file uploaders above.")
        st.info(f"Found files:\n- {fitness_before}\n- {fitness_after}\n\nPlease upload them using the file uploaders.")
    else:
        st.sidebar.warning("Files not found in expected location. Please upload manually.")

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
    # Process files
    with st.spinner("Processing meshes..."):
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
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Overall Statistics")
                st.metric("Average Change", f"{stats['avg_magnitude']:.4f}")
                st.metric("Max Change", f"{stats['max_magnitude']:.4f}")
                
                st.markdown("### Change Distribution")
                increase_pct = stats['increase_percentage']
                decrease_pct = stats['decrease_percentage']
                
                st.progress(increase_pct / 100, text=f"Increase: {increase_pct:.1f}%")
                st.progress(decrease_pct / 100, text=f"Decrease: {decrease_pct:.1f}%")
            
            with col2:
                st.subheader("🗺️ Region Breakdown")
                for region, region_data in region_stats.items():
                    with st.expander(region.replace('_', ' ').title()):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Increase", f"{region_data['increase_percentage']:.1f}%")
                        with col_b:
                            st.metric("Decrease", f"{region_data['decrease_percentage']:.1f}%")
                        st.metric("Avg Magnitude", f"{region_data['avg_magnitude']:.4f}")
            
            # Side-by-Side Comparison View
            st.markdown("---")
            st.subheader("📊 Side-by-Side Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Baseline (Before)")
                baseline_vertices = comparison_result["baseline_vertices"]
                baseline_faces = baseline_data["faces"]
                
                fig_baseline = go.Figure()
                
                if len(baseline_faces) > 0:
                    fig_baseline.add_trace(go.Mesh3d(
                        x=baseline_vertices[:, 0],
                        y=baseline_vertices[:, 1],
                        z=baseline_vertices[:, 2],
                        i=baseline_faces[:, 0],
                        j=baseline_faces[:, 1],
                        k=baseline_faces[:, 2],
                        color='lightgray',
                        opacity=0.8,
                        name='Baseline'
                    ))
                else:
                    fig_baseline.add_trace(go.Scatter3d(
                        x=baseline_vertices[:, 0],
                        y=baseline_vertices[:, 1],
                        z=baseline_vertices[:, 2],
                        mode='markers',
                        marker=dict(size=3, color='lightgray', opacity=0.6),
                        name='Baseline'
                    ))
                
                fig_baseline.update_layout(
                    title="Before",
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
                st.markdown("### Current (After) - Color Coded")
                comparison_vertices = comparison_result["comparison_vertices"]
                # Use baseline faces since comparison_vertices are now aligned to baseline topology
                comparison_faces = baseline_data["faces"]
                projections = comparison_result["projections"]
                
                # Normalize for color mapping
                max_proj = np.max(np.abs(projections)) if np.max(np.abs(projections)) > 0 else 1.0
                normalized_proj = (projections / max_proj + 1) / 2  # Map to [0,1]
                
                fig_comparison = go.Figure()
                
                # Add mesh with color gradation
                if len(comparison_faces) > 0 and len(comparison_faces.shape) == 2 and comparison_faces.shape[1] == 3:
                    # Ensure face indices are valid
                    max_face_idx = np.max(comparison_faces)
                    if max_face_idx < len(comparison_vertices):
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
                                title=dict(text="Change", side="right"),
                                len=0.5
                            ),
                            opacity=0.8
                        ))
                    else:
                        # Fallback to scatter if face indices are invalid
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
                else:
                    # Fallback to scatter
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
                    title="After (Color-Coded)",
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
            
            # Color legend
            st.markdown("""
            <div style="background: #f0f0f0; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h4>🎨 Color Legend:</h4>
                <ul style="margin: 10px 0;">
                    <li><strong style="color: #00ff00;">🟢 Green</strong> = Volume Reduction (Fat Loss / Decrease)</li>
                    <li><strong style="color: #ff0000;">🔴 Red</strong> = Volume Increase (Muscle Gain / Increase)</li>
                    <li><strong>⚪ White</strong> = No Significant Change</li>
                </ul>
                <p><strong>💡 Tip:</strong> Use your mouse to rotate, zoom, and pan the 3D visualization.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Color-coded scatter plot (alternative view)
            st.subheader("📈 Deformation Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Scatter plot colored by change
                fig_scatter = go.Figure()
                
                # Use comparison vertices for scatter plot
                comparison_vertices_scatter = comparison_result["comparison_vertices"]
                
                # Separate increases and decreases
                increase_mask = comparison_result["projections"] > 0
                decrease_mask = comparison_result["projections"] < 0
                neutral_mask = comparison_result["projections"] == 0
                
                if np.any(increase_mask):
                    fig_scatter.add_trace(go.Scatter3d(
                        x=comparison_vertices_scatter[increase_mask, 0],
                        y=comparison_vertices_scatter[increase_mask, 1],
                        z=comparison_vertices_scatter[increase_mask, 2],
                        mode='markers',
                        marker=dict(
                            size=3,
                            color='red',
                            opacity=0.6
                        ),
                        name='Increase (Red)'
                    ))
                
                if np.any(decrease_mask):
                    fig_scatter.add_trace(go.Scatter3d(
                        x=comparison_vertices_scatter[decrease_mask, 0],
                        y=comparison_vertices_scatter[decrease_mask, 1],
                        z=comparison_vertices_scatter[decrease_mask, 2],
                        mode='markers',
                        marker=dict(
                            size=3,
                            color='green',
                            opacity=0.6
                        ),
                        name='Decrease (Green)'
                    ))
                
                if np.any(neutral_mask):
                    fig_scatter.add_trace(go.Scatter3d(
                        x=comparison_vertices_scatter[neutral_mask, 0],
                        y=comparison_vertices_scatter[neutral_mask, 1],
                        z=comparison_vertices_scatter[neutral_mask, 2],
                        mode='markers',
                        marker=dict(
                            size=2,
                            color='gray',
                            opacity=0.3
                        ),
                        name='No Change'
                    ))
                
                fig_scatter.update_layout(
                    title="Change Distribution (Point Cloud)",
                    scene=dict(
                        xaxis_title="Width",
                        yaxis_title="Height",
                        zaxis_title="Depth"
                    ),
                    height=600
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col2:
                # Histogram of changes
                fig_hist = go.Figure()
                
                fig_hist.add_trace(go.Histogram(
                    x=comparison_result["projections"][increase_mask] if np.any(increase_mask) else [],
                    name='Increase',
                    marker_color='red',
                    opacity=0.7
                ))
                
                fig_hist.add_trace(go.Histogram(
                    x=comparison_result["projections"][decrease_mask] if np.any(decrease_mask) else [],
                    name='Decrease',
                    marker_color='green',
                    opacity=0.7
                ))
                
                fig_hist.update_layout(
                    title="Distribution of Changes",
                    xaxis_title="Displacement (projection on normal)",
                    yaxis_title="Number of Vertices",
                    barmode='overlay',
                    height=600
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
            
            # Insights
            st.markdown("---")
            st.subheader("🧠 AI Insights")
            st.info(insights['text'])
            st.caption(f"Confidence: {insights['confidence']*100:.0f}%")
            
            # Download comparison mesh with colors
            st.markdown("---")
            st.subheader("💾 Export Comparison Mesh")
            
            # Create comparison mesh with vertex colors
            # Use baseline faces since comparison_vertices are aligned to baseline topology
            comparison_vertices = comparison_result["comparison_vertices"]
            comparison_faces = baseline_data["faces"]
            
            comparison_mesh = trimesh.Trimesh(
                vertices=comparison_vertices,
                faces=comparison_faces,
                vertex_colors=colors
            )
            
            # Export to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.obj') as tmp_export:
                comparison_mesh.export(tmp_export.name)
                export_path = tmp_export.name
            
            # Download button
            with open(export_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Comparison Mesh (with colors)",
                    data=f.read(),
                    file_name="comparison_mesh_colored.obj",
                    mime="application/octet-stream",
                    help="This single mesh file contains vertex colors: Green=decrease, Red=increase, White=no change"
                )
            
            st.caption("💡 This single mesh file contains embedded vertex colors showing increase (red) and decrease (green). Open in Blender or MeshLab to view.")
            
            # Also export metadata
            st.markdown("---")
            st.subheader("📊 Export Statistics")
            
            results_summary = {
                'statistics': stats,
                'region_statistics': region_stats,
                'insights': insights['text'],
                'color_metadata': color_metadata
            }
            
            import json
            results_json = json.dumps(results_summary, indent=2)
            
            st.download_button(
                label="📥 Download Statistics (JSON)",
                data=results_json,
                file_name="comparison_results.json",
                mime="application/json"
            )
            
            # Cleanup temp file
            try:
                os.unlink(export_path)
            except:
                pass
        
        except Exception as e:
            st.error(f"Error processing meshes: {str(e)}")
            st.exception(e)
        
        finally:
            # Cleanup temp files
            try:
                os.unlink(tmp_baseline_path)
                os.unlink(tmp_comparison_path)
            except:
                pass

elif baseline_file or comparison_file:
    st.warning("⚠️ Please upload both baseline and comparison meshes to compare.")
    
    if baseline_file:
        st.success(f"✓ Baseline mesh uploaded: {baseline_file.name}")
    if comparison_file:
        st.success(f"✓ Comparison mesh uploaded: {comparison_file.name}")

else:
    # Welcome screen
    st.info("👆 Upload two 3D mesh files in the sidebar to get started!")
    
    st.markdown("### 📋 How to Use:")
    st.markdown("""
    1. **Upload Baseline Mesh**: Your first/initial body scan (Week 0)
    2. **Upload Comparison Mesh**: A later body scan (Week 4, 8, 12...)
    3. **View Results**: 
       - 3D visualization with color gradation
       - Statistics and region breakdown
       - AI-generated insights
       - Deformation analysis
    """)
    
    st.markdown("### 🎯 Supported Formats:")
    st.markdown("- **OBJ** (.obj)")
    st.markdown("- **GLB** (.glb)")
    st.markdown("- **FBX** (.fbx)")
    
    st.markdown("### 💡 Example:")
    st.code("""
    Baseline: realistic_week0.obj (105kg, high belly fat)
    Comparison: realistic_week12.obj (97kg, reduced belly fat)
    
    Result: Green areas show fat loss, Red areas show muscle gain
    """, language="text")

