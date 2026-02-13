"""
Quick start example for CLIP Neuron Visualizer
Run this after installing dependencies: pip install -r requirements.txt
"""

import torch
import clip
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer
from pathlib import Path

def quick_start_example():
    """Quick start example for neuron visualization."""
    
    print("=" * 60)
    print("🧠 CLIP Neuron Visualizer - Quick Start")
    print("=" * 60)
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n📍 Using device: {device.upper()}")
    
    # Load CLIP model
    print("\n📥 Loading CLIP ViT-B/32 model...")
    model, preprocess = clip.load("ViT-B/32", device=device)
    print("✓ Model loaded!")
    
    # Initialize inspector
    print("\n🔍 Initializing layer inspector...")
    inspector = LayerInspector(model, model_name="ViT-B/32")
    layer_names = inspector.get_layer_names()
    print(f"✓ Found {len(layer_names)} layers")
    
    # Select a layer for visualization
    # Let's use a middle layer for interesting results
    selected_layer = "visual.transformer.resblocks.5.attn"
    
    print(f"\n📋 Selected layer: {selected_layer}")
    
    # Get information about this layer
    layer_info = inspector.get_layer_info(selected_layer)
    print(f"   Type: {layer_info.get('type')}")
    print(f"   Parameters: {layer_info.get('parameters'):,}")
    
    # Get available neurons
    neuron_names = inspector.get_neuron_names(selected_layer)
    print(f"   Available neurons: {len(neuron_names)}")
    
    # Select a neuron
    selected_neuron = 0
    print(f"\n📍 Selected neuron: {selected_neuron} ({neuron_names[selected_neuron]})")
    
    # Initialize visualizer
    print("\n🎨 Initializing feature visualizer...")
    visualizer = FeatureVisualizer(model, device=device)
    print("✓ Visualizer ready!")
    
    # Generate visualization
    print("\n🚀 Generating visualization (this may take a minute)...")
    print("   Parameters:")
    print("   - Image size: 224x224")
    print("   - Iterations: 500")
    print("   - Learning rate: 0.01")
    
    def progress(current, total, activation):
        percent = (current / total) * 100
        print(f"   Progress: {percent:5.1f}% | Activation: {activation:.4f}", end='\r')
    
    # Generate image with smaller number of iterations for quick demo
    generated_image = visualizer.generate_image(
        layer_name=selected_layer,
        neuron_index=selected_neuron,
        image_size=224,
        num_iterations=500,
        learning_rate=0.01,
        seed=42,
        progress_callback=progress
    )
    
    print("\n\n✓ Visualization complete!")
    
    # Save the image
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "quick_start_example.png"
    
    generated_image.save(output_path)
    print(f"\n💾 Image saved to: {output_path}")
    
    # Print next steps
    print("\n" + "=" * 60)
    print("🎉 Next Steps:")
    print("=" * 60)
    print("\n1. Try the interactive web interface:")
    print("   $ streamlit run app.py")
    print("\n2. Or use the command-line interface:")
    print("   $ python cli.py --list-layers")
    print("   $ python cli.py --layer <layer_name> --neuron <index>")
    print("\n3. Learn more:")
    print("   - Read README.md for detailed documentation")
    print("   - Check cli.py --help for all available options")
    print("=" * 60)


if __name__ == "__main__":
    try:
        quick_start_example()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have installed all dependencies:")
        print("pip install -r requirements.txt")
