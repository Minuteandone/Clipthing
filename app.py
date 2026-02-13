"""
Main interactive Streamlit application for CLIP neuron visualization.
"""

import streamlit as st
import torch
import clip
from pathlib import Path
from datetime import datetime
import os

from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer


@st.cache_resource
def load_clip_model():
    """Load CLIP model with caching."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, device


@st.cache_resource
def get_layer_inspector(model):
    """Get layer inspector with caching."""
    return LayerInspector(model, model_name="ViT-B/32")


@st.cache_resource
def get_feature_visualizer(model, device):
    """Get feature visualizer with caching."""
    return FeatureVisualizer(model, device=device)


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="CLIP Neuron Visualizer",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧠 CLIP Neuron Visualizer")
    st.markdown(
        "Generate images that maximally excite specific neurons in CLIP-ViT-B/32"
    )
    
    # Load model
    st.sidebar.header("Model Configuration")
    with st.spinner("Loading CLIP model..."):
        model, device = load_clip_model()
        inspector = get_layer_inspector(model)
        visualizer = get_feature_visualizer(model, device)
    
    st.sidebar.success("✓ CLIP model loaded!")
    st.sidebar.write(f"Device: {device.upper()}")
    
    # Layer selection
    st.sidebar.header("Layer Selection")
    layer_names = inspector.get_layer_names()
    
    # Filter to interesting layers (exclude very small ones)
    interesting_layers = [
        l for l in layer_names 
        if any(x in l for x in ['transformer', 'attn', 'mlp', 'ln', 'proj'])
    ]
    
    if not interesting_layers:
        interesting_layers = layer_names
    
    selected_layer = st.sidebar.selectbox(
        "Select Layer",
        interesting_layers,
        help="Choose the layer whose neurons you want to visualize"
    )
    
    # Display layer info
    layer_info = inspector.get_layer_info(selected_layer)
    with st.sidebar.expander("Layer Details"):
        st.write(f"**Name**: {layer_info.get('name', 'N/A')}")
        st.write(f"**Type**: {layer_info.get('type', 'N/A')}")
        st.write(f"**Parameters**: {layer_info.get('parameters', 'N/A'):,}")
        if 'out_features' in layer_info:
            st.write(f"**Output Features**: {layer_info['out_features']}")
    
    # Neuron selection
    st.sidebar.header("Neuron Selection")
    neuron_names = inspector.get_neuron_names(selected_layer)
    
    if neuron_names:
        # Create neuron options
        neuron_options = {name: idx for idx, name in enumerate(neuron_names)}
        
        selected_neuron_name = st.sidebar.selectbox(
            "Select Neuron",
            neuron_options.keys(),
            help="Choose the neuron to visualize"
        )
        
        selected_neuron_idx = neuron_options[selected_neuron_name]
        
        st.sidebar.write(f"📍 Selected: {selected_neuron_name} (Index: {selected_neuron_idx})")
    else:
        st.sidebar.error("❌ No neurons found for this layer")
        return
    
    # Visualization parameters
    st.sidebar.header("Visualization Parameters")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        image_size = st.number_input(
            "Image Size",
            min_value=64,
            max_value=512,
            value=224,
            step=32,
            help="Resolution of generated image"
        )
    
    with col2:
        num_iterations = st.number_input(
            "Iterations",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100,
            help="Number of optimization steps"
        )
    
    learning_rate = st.sidebar.slider(
        "Learning Rate",
        min_value=0.001,
        max_value=0.1,
        value=0.01,
        step=0.001,
        help="Optimization learning rate"
    )
    
    blur_every = st.sidebar.slider(
        "Blur Every N Iterations",
        min_value=5,
        max_value=50,
        value=10,
        help="Apply blur periodically for smoothness"
    )
    
    seed_value = st.sidebar.number_input(
        "Random Seed",
        min_value=0,
        max_value=10000,
        value=42,
        step=1,
        help="Set for reproducible results"
    )
    
    # Generate button
    st.sidebar.header("Generation")
    generate_btn = st.sidebar.button(
        "🚀 Generate Visualization",
        use_container_width=True,
        type="primary"
    )
    
    # Main content area
    if generate_btn:
        try:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("🎨 Generated Image")
                progress_bar = st.progress(0)
                status_text = st.empty()
                activation_text = st.empty()
            
            with col2:
                st.subheader("📊 Generation Info")
                info_placeholder = st.empty()
                info_placeholder.info(
                    f"Layer: {selected_layer}\n\n"
                    f"Neuron: {selected_neuron_name} ({selected_neuron_idx})\n\n"
                    f"Size: {image_size}x{image_size}\n\n"
                    f"Iterations: {num_iterations}"
                )
            
            # Progress callback
            def update_progress(current, total, activation):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Progress: {current}/{total}")
                activation_text.text(f"Activation: {activation:.4f}")
            
            # Generate image
            st.write("Generating image (this may take a few minutes)...")
            
            generated_image = visualizer.generate_image(
                layer_name=selected_layer,
                neuron_index=selected_neuron_idx,
                image_size=image_size,
                num_iterations=num_iterations,
                learning_rate=learning_rate,
                blur_every=blur_every,
                seed=seed_value,
                progress_callback=update_progress
            )
            
            # Display results
            with col1:
                st.image(generated_image, use_column_width=True)
            
            # Save option
            st.sidebar.header("Export")
            if st.sidebar.button("💾 Save Image", use_container_width=True):
                # Create output directory
                output_dir = Path("generated_images")
                output_dir.mkdir(exist_ok=True)
                
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"neuron_{selected_neuron_idx}_{selected_layer.replace('.', '_')}_{timestamp}.png"
                filepath = output_dir / filename
                
                # Save image
                generated_image.save(filepath)
                st.success(f"✓ Image saved to {filepath}")
                st.sidebar.write(f"Saved: {filename}")
        
        except Exception as e:
            st.error(f"❌ Error during generation: {str(e)}")
            st.write("Please check the parameters and try again.")
    
    # Information section
    with st.expander("ℹ️ About"):
        st.markdown("""
        ### CLIP Neuron Visualizer
        
        This tool generates images that maximally activate specific neurons in the CLIP-ViT-B/32 model.
        
        **How it works:**
        1. Select a layer from the CLIP visual encoder
        2. Choose a specific neuron in that layer
        3. The tool optimizes a random image to maximize the activation of that neuron
        4. The result is a synthetic image that reveals what features the neuron responds to
        
        **Parameters:**
        - **Image Size**: Resolution of the generated image (larger = slower but possibly more detailed)
        - **Iterations**: Number of optimization steps (more = better but slower)
        - **Learning Rate**: How quickly the optimization proceeds
        - **Blur Every N Iterations**: Periodically smooths the image for more natural results
        - **Random Seed**: For reproducible results
        
        **Output:**
        The generated image shows visual patterns that strongly activate the selected neuron.
        This helps understand what visual features are encoded in different parts of the model.
        """)
    
    with st.expander("⚙️ Technical Details"):
        st.markdown("""
        **Model**: CLIP ViT-B/32
        - Vision Transformer with base configuration
        - 224x224 input resolution
        - 12 transformer blocks
        
        **Optimization Method**:
        - Adam optimizer
        - Total variation regularization for smoothness
        - Periodic Gaussian blur
        - Gradient-based image generation
        
        **Normalization**:
        - ImageNet normalization applied during optimization
        - Results denormalized for display
        """)


if __name__ == "__main__":
    main()
