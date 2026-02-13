# 🚀 Quick Reference Guide

## Installation (2 steps)
```bash
pip install -r requirements.txt
```

## Run (choose one)

### 🌐 Web Interface (Easiest)
```bash
streamlit run app.py
# Opens at http://localhost:8501
```

### 💻 Command Line (Flexible)
```bash
# List layers
python cli.py --list-layers

# List neurons in a layer
python cli.py --layer visual.transformer.resblocks.5.attn --neurons

# Generate visualization
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 32 --output my_image.png
```

### ⚡ Quick Demo (30 seconds)
```bash
python quickstart.py
```

### 📦 Batch Processing (Multiple neurons)
```bash
python batch.py --layer visual.transformer.resblocks.5.attn --neuron-range 0 64 8
```

### 🐍 Custom Python Script
```python
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer
import torch, clip

model, _ = clip.load("ViT-B/32", device="cuda")
inspector = LayerInspector(model)
visualizer = FeatureVisualizer(model, device="cuda")

# Get available info
layers = inspector.get_layer_names()
neurons = inspector.get_neuron_names("visual.transformer.resblocks.5.attn")

# Generate visualization
image = visualizer.generate_image(
    layer_name="visual.transformer.resblocks.5.attn",
    neuron_index=32,
    image_size=224,
    num_iterations=1000,
    learning_rate=0.01
)
image.save("output.png")
```

## Key Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| image_size | 64-512 | 224 | Output resolution |
| iterations | 100-5000 | 1000 | Optimization steps |
| learning_rate | 0.001-0.1 | 0.01 | Optimization speed |
| blur_every | 5-50 | 10 | Smoothness |
| seed | Any int | 42 | Reproducibility |

## Understanding Results

**Early Layers (blocks 0-2)**
→ Edges, curves, colors, textures

**Middle Layers (blocks 3-6)**
→ Shapes, patterns, orientations

**Late Layers (blocks 7-11)**
→ Object parts, semantics, concepts

## Common Tasks

### Visualize a specific neuron
```bash
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 32 --output result.png
```

### Quick preview (fast)
```bash
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 32 \
  --size 128 --iterations 300 --output quick.png
```

### High quality (slow)
```bash
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 32 \
  --size 512 --iterations 2000 --output hq.png
```

### Batch processing (many neurons)
```bash
python batch.py --layer visual.transformer.resblocks.5.attn \
  --neuron-range 0 64 4
```

### Reproducible result
```bash
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 32 \
  --seed 12345 --output reproducible.png
```

## Help

**Get help for any command:**
```bash
python cli.py --help
python batch.py --help
```

**For detailed documentation:**
- `README.md` - Full guide
- `SETUP.md` - Installation & troubleshooting
- `PROJECT.md` - Architecture overview

**For issues:**
1. Check SETUP.md troubleshooting section
2. Verify GPU/CUDA availability: `nvidia-smi`
3. Ensure requirements installed: `pip list | grep -i torch`

## Performance Tips

**Speed up:**
- ↓ image_size (smaller = faster)
- ↓ iterations (fewer = faster)
- Use GPU instead of CPU

**Better quality:**
- ↑ iterations
- ↓ learning_rate (more stable)
- ↑ image_size (more detail)

**Reproducibility:**
- Use `--seed` flag
- Keep all parameters consistent

## File Locations

```
Clipthing/
├── ✅ app.py              ← Web interface
├── ✅ cli.py              ← Command line
├── ✅ batch.py            ← Batch processing
├── ✅ quickstart.py       ← Demo
├── ✅ layer_inspector.py  ← Utilities
├── ✅ feature_visualizer.py ← Utilities
└── 📁 generated_images/   ← Output folder
```

## Device Support

**GPU (Recommended)**
- NVIDIA CUDA: Automatic
- Apple Silicon: May need `device="mps"`
- AMD ROCm: May need special setup

**CPU (Slow!)**
- Always works
- ~10-15x slower than GPU
- Edit code: change `device="cuda"` to `device="cpu"`

## Examples

### Explore Attention Patterns
```bash
python cli.py --layer visual.transformer.resblocks.8.attn --neurons
for i in 0 4 8 12; do
  python cli.py --layer visual.transformer.resblocks.8.attn --neuron $i \
    --output attn_head_$i.png
done
```

### Compare Layer Depths
```bash
for b in 0 3 6 9 11; do
  python cli.py --layer visual.transformer.resblocks.$b.mlp --neuron 256 \
    --output layer_${b}_neuron_256.png
done
```

### Feature Atlas (many neurons)
```bash
python batch.py --layer visual.transformer.resblocks.5.mlp \
  --neuron-range 0 768 32 \
  --size 256 --iterations 800
```

## System Requirements

- Python 3.8+
- 8GB+ GPU VRAM (or 16GB+ RAM for CPU)
- ~500MB disk space
- Internet connection (for first-time model download)

## What Gets Downloaded

On first run:
- CLIP ViT-B/32 model: ~340MB
- PyTorch: ~2GB (if not installed)
- Dependencies: ~200MB

Total: ~3-4GB once

## Time Estimates (A100 GPU)

| Config | Time |
|--------|------|
| 64×64, 300 iter | 5s |
| 224×224, 500 iter | 30s |
| 224×224, 1000 iter | 60s |
| 512×512, 1000 iter | 180s |

CPU: 10-50x slower

## Troubleshooting

**Out of memory:**
```bash
python cli.py --layer ... --neuron ... --size 128 --iterations 300
```

**Slow generation:**
- Use GPU
- Reduce size/iterations
- Check `nvidia-smi` for other GPU processes

**Model download fails:**
- Check internet connection
- Model caches to `~/.cache/clip`
- Try manual: `import clip; clip.load("ViT-B/32")`

**Import errors:**
```bash
pip install --upgrade clip-by-openai torch torchvision
```

---

**Ready? Pick your method above and start exploring!** 🧠✨
