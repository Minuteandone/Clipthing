"""
Command-line script for CLIP neuron visualization.
Usage: python cli.py --layer <layer_name> --neuron <neuron_index> --output <output_path>
"""

import argparse
import torch
import clip
from pathlib import Path
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer


def main():
    parser = argparse.ArgumentParser(
        description="Generate images that maximize neuron activations in CLIP"
    )
    
    parser.add_argument(
        "--list-layers",
        action="store_true",
        help="List all available layers and exit"
    )
    
    parser.add_argument(
        "--layer",
        type=str,
        help="Layer name (e.g., 'visual.transformer.resblocks.0.attn')"
    )
    
    parser.add_argument(
        "--neuron",
        type=int,
        help="Neuron index"
    )
    
    parser.add_argument(
        "--neurons",
        action="store_true",
        help="List neurons in the selected layer and exit"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="generated_image.png",
        help="Output image path (default: generated_image.png)"
    )
    
    parser.add_argument(
        "--size",
        type=int,
        default=224,
        help="Image size (default: 224)"
    )
    
    parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Number of optimization iterations (default: 1000)"
    )
    
    parser.add_argument(
        "--lr",
        type=float,
        default=0.01,
        help="Learning rate (default: 0.01)"
    )
    
    parser.add_argument(
        "--blur-every",
        type=int,
        default=10,
        help="Apply blur every N iterations (default: 10)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)"
    )
    
    args = parser.parse_args()
    
    # Load model
    print("Loading CLIP model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    print(f"✓ Model loaded on {device.upper()}")
    
    # Initialize inspector
    inspector = LayerInspector(model, model_name="ViT-B/32")
    
    # List layers if requested
    if args.list_layers:
        print("\n📋 Available Layers:")
        print("-" * 60)
        for layer_name in inspector.get_layer_names():
            info = inspector.get_layer_info(layer_name)
            print(f"{layer_name}")
            print(f"  Type: {info.get('type')}, Parameters: {info.get('parameters', 'N/A')}")
        return
    
    # Validate layer selection
    if not args.layer:
        print("❌ Error: --layer argument is required")
        print("Use --list-layers to see available layers")
        return
    
    layer_names = inspector.get_layer_names()
    if args.layer not in layer_names:
        print(f"❌ Error: Layer '{args.layer}' not found")
        print(f"Available layers: {layer_names}")
        return
    
    # List neurons if requested
    if args.neurons:
        neuron_names = inspector.get_neuron_names(args.layer)
        print(f"\n📍 Neurons in layer '{args.layer}':")
        print("-" * 60)
        for idx, name in enumerate(neuron_names):
            print(f"{idx:4d}: {name}")
        return
    
    # Validate neuron selection
    if args.neuron is None:
        print("❌ Error: --neuron argument is required")
        print(f"Use --layer {args.layer} --neurons to see available neurons")
        return
    
    neuron_names = inspector.get_neuron_names(args.layer)
    if args.neuron >= len(neuron_names):
        print(f"❌ Error: Neuron index {args.neuron} out of range (0-{len(neuron_names)-1})")
        return
    
    # Initialize visualizer
    print("\nInitializing visualizer...")
    visualizer = FeatureVisualizer(model, device=device)
    
    # Generate image
    print(f"\n🎨 Generating visualization...")
    print(f"  Layer: {args.layer}")
    print(f"  Neuron: {args.neuron} ({neuron_names[args.neuron]})")
    print(f"  Size: {args.size}x{args.size}")
    print(f"  Iterations: {args.iterations}")
    print(f"  Learning Rate: {args.lr}")
    
    def progress_callback(current, total, activation):
        percent = (current / total) * 100
        bar_length = 40
        filled = int(bar_length * current / total)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r  [{bar}] {percent:.1f}% | Activation: {activation:.4f}", end="")
    
    try:
        generated_image = visualizer.generate_image(
            layer_name=args.layer,
            neuron_index=args.neuron,
            image_size=args.size,
            num_iterations=args.iterations,
            learning_rate=args.lr,
            blur_every=args.blur_every,
            seed=args.seed,
            progress_callback=progress_callback
        )
        
        # Create output directory if needed
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save image
        generated_image.save(output_path)
        print(f"\n\n✓ Image saved to {output_path}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
