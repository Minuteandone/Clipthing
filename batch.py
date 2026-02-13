"""
Batch processing script for generating multiple neuron visualizations.
This script allows you to generate visualizations for multiple neurons at once.

Usage examples:
  python batch.py --layer visual.transformer.resblocks.5.attn --neuron-range 0 64 8
  python batch.py --layer visual.transformer.resblocks.10.mlp --neuron-range 0 768 32
"""

import argparse
import torch
import clip
from pathlib import Path
from datetime import datetime
import json
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer


def batch_generate(
    layer_name: str,
    neuron_range: tuple,
    output_dir: str = "generated_images",
    image_size: int = 224,
    iterations: int = 500,
    learning_rate: float = 0.01,
    blur_every: int = 10,
    seed_base: int = 42,
    skip_existing: bool = True
):
    """
    Generate visualizations for multiple neurons.
    
    Args:
        layer_name: Name of the layer
        neuron_range: Tuple of (start, end, step) for neuron indices
        output_dir: Directory to save images
        image_size: Size of generated images
        iterations: Number of optimization iterations
        learning_rate: Learning rate for optimization
        blur_every: Apply blur every N iterations
        seed_base: Base seed (will be offset by neuron index)
        skip_existing: Skip neurons that already have visualizations
    """
    
    # Setup
    device = "cuda" if torch.cuda.is_available() else "cpu"
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Load model
    print("Loading CLIP model...")
    model, _ = clip.load("ViT-B/32", device=device)
    
    # Setup inspector and visualizer
    inspector = LayerInspector(model)
    visualizer = FeatureVisualizer(model, device=device)
    
    # Validate layer
    if layer_name not in inspector.get_layer_names():
        print(f"❌ Layer '{layer_name}' not found!")
        return
    
    # Get neuron information
    neuron_names = inspector.get_neuron_names(layer_name)
    print(f"✓ Layer '{layer_name}' has {len(neuron_names)} neurons")
    
    # Parse neuron range
    start, end, step = neuron_range
    if end > len(neuron_names):
        end = len(neuron_names)
    
    neuron_indices = list(range(start, end, step))
    print(f"📍 Will visualize {len(neuron_indices)} neurons: {start}-{end} (step {step})")
    
    # Create metadata file
    metadata = {
        "layer": layer_name,
        "start_time": datetime.now().isoformat(),
        "parameters": {
            "image_size": image_size,
            "iterations": iterations,
            "learning_rate": learning_rate,
            "blur_every": blur_every,
        },
        "neurons": {}
    }
    
    # Generate visualizations
    print("\n" + "=" * 60)
    for i, neuron_idx in enumerate(neuron_indices):
        if neuron_idx >= len(neuron_names):
            print(f"⚠️  Neuron {neuron_idx} out of range, skipping")
            continue
        
        neuron_name = neuron_names[neuron_idx]
        
        # Check if file exists
        filename = f"{layer_name.replace('.', '_')}_neuron_{neuron_idx}.png"
        filepath = output_dir / filename
        
        if filepath.exists() and skip_existing:
            print(f"[{i+1}/{len(neuron_indices)}] Skipping neuron {neuron_idx} ({neuron_name}) - already exists")
            metadata["neurons"][neuron_idx] = {
                "name": neuron_name,
                "status": "skipped",
                "file": filename
            }
            continue
        
        print(f"[{i+1}/{len(neuron_indices)}] Generating neuron {neuron_idx} ({neuron_name})...")
        
        # Progress callback
        def progress(current, total, activation):
            percent = (current / total) * 100
            bar_length = 30
            filled = int(bar_length * current / total)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  [{bar}] {percent:.0f}% Activation: {activation:.4f}", end='\r')
        
        try:
            # Generate image
            image = visualizer.generate_image(
                layer_name=layer_name,
                neuron_index=neuron_idx,
                image_size=image_size,
                num_iterations=iterations,
                learning_rate=learning_rate,
                blur_every=blur_every,
                seed=seed_base + neuron_idx,
                progress_callback=progress
            )
            
            # Save image
            image.save(filepath)
            print(f"\n  ✓ Saved to {filename}")
            
            # Update metadata
            metadata["neurons"][neuron_idx] = {
                "name": neuron_name,
                "status": "success",
                "file": filename
            }
        
        except Exception as e:
            print(f"\n  ❌ Error generating neuron {neuron_idx}: {str(e)}")
            metadata["neurons"][neuron_idx] = {
                "name": neuron_name,
                "status": "error",
                "error": str(e)
            }
    
    # Save metadata
    metadata["end_time"] = datetime.now().isoformat()
    metadata_file = output_dir / f"{layer_name.replace('.', '_')}_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✓ Batch generation complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Metadata saved to: {metadata_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate neuron visualizations"
    )
    
    parser.add_argument(
        "--layer",
        type=str,
        required=True,
        help="Layer name (e.g., 'visual.transformer.resblocks.5.attn')"
    )
    
    parser.add_argument(
        "--neuron-range",
        type=int,
        nargs=3,
        metavar=("START", "END", "STEP"),
        default=(0, 64, 8),
        help="Neuron range as start end step (default: 0 64 8)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated_images",
        help="Output directory (default: generated_images)"
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
        default=500,
        help="Number of iterations (default: 500)"
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
        "--seed-base",
        type=int,
        default=42,
        help="Base seed for reproducibility (default: 42)"
    )
    
    parser.add_argument(
        "--no-skip",
        action="store_true",
        help="Regenerate even if files exist"
    )
    
    args = parser.parse_args()
    
    # Run batch generation
    batch_generate(
        layer_name=args.layer,
        neuron_range=tuple(args.neuron_range),
        output_dir=args.output_dir,
        image_size=args.size,
        iterations=args.iterations,
        learning_rate=args.lr,
        blur_every=args.blur_every,
        seed_base=args.seed_base,
        skip_existing=not args.no_skip
    )


if __name__ == "__main__":
    main()
