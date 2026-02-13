# CLIP Neuron Visualizer - Setup & Getting Started

## ⚡ Quick Start (5 minutes)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Minuteandone/Clipthing.git
cd Clipthing

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Web Interface (Recommended)

```bash
streamlit run app.py
```

Open browser to `http://localhost:8501` and follow the interactive interface.

### 3. Or Run Quick Start Example

```bash
python quickstart.py
```

This will generate a quick demo visualization.

---

## 📋 Requirements

- Python 3.8+
- ~8GB GPU VRAM (12GB recommended) OR 16GB+ RAM for CPU
- ~500MB disk space (for model + dependencies)

### Package Requirements

All packages in `requirements.txt`:
- `torch` - Deep learning framework
- `torchvision` - Computer vision utilities
- `clip-by-openai` - OpenAI's CLIP model
- `Pillow` - Image processing
- `numpy` - Numerical computing
- `matplotlib` - Visualization
- `scikit-image` - Image processing
- `tqdm` - Progress bars
- `streamlit` - Web interface

---

## 🚀 Usage Modes

### Mode 1: Web Interface (Easiest)

```bash
streamlit run app.py
```

**Advantages:**
- ✨ Interactive and user-friendly
- 📊 Real-time parameter adjustment
- 📈 Live progress visualization
- 💾 One-click image export

### Mode 2: Command Line

```bash
# List all layers
python cli.py --list-layers

# List neurons in a layer
python cli.py --layer visual.transformer.resblocks.5.attn --neurons

# Generate visualization
python cli.py \
  --layer visual.transformer.resblocks.5.attn \
  --neuron 32 \
  --output my_visualization.png \
  --iterations 1000
```

**Advantages:**
- 💻 Perfect for batch processing
- 🔄 Easy to automate
- 📝 Works in headless environments

### Mode 3: Python Script

```python
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer
import torch
import clip

# Load model
model, _ = clip.load("ViT-B/32", device="cuda")

# Create inspector and visualizer
inspector = LayerInspector(model)
visualizer = FeatureVisualizer(model, device="cuda")

# Generate visualization
image = visualizer.generate_image(
    layer_name="visual.transformer.resblocks.5.attn",
    neuron_index=32,
    num_iterations=1000,
    image_size=224
)

image.save("visualization.png")
```

**Advantages:**
- 🎓 Full control over parameters
- 🔧 Easy to customize
- 📚 Perfect for research

---

## 🎯 Which Mode Should I Use?

| Use Case | Recommended |
|----------|-------------|
| First time exploring | 🌐 Web Interface |
| Interactive experimentation | 🌐 Web Interface |
| Batch processing many neurons | 💻 Command Line |
| Integration in another project | 🐍 Python Script |
| Large-scale visualization | 🐍 Python Script |

---

## 🔧 Troubleshooting

### Problem: CUDA out of memory

**Solution:**
```bash
# Reduce image size
python cli.py --layer ... --neuron ... --size 128 --iterations 500

# Or use CPU (slower but uses less GPU RAM)
# Edit feature_visualizer.py or app.py to use device="cpu"
```

### Problem: Very slow generation

**Solution:**
```bash
# Use GPU instead of CPU
# Reduce image size and iterations
python cli.py --layer ... --neuron ... --size 128 --iterations 300

# Check you're not running other GPU processes
nvidia-smi  # Shows GPU usage
```

### Problem: Model download fails

**Solution:**
```bash
# The model (~340MB) should auto-download to ~/.cache/clip
# If it fails, check your internet connection
# You can manually download from:
# https://openaipublic.blob.core.windows.net/clip/models/...

# Or pre-download using:
import clip
model, _ = clip.load("ViT-B/32")  # This downloads the model
```

### Problem: ImportError with CLIP

**Solution:**
```bash
# Make sure you installed from requirements
pip uninstall clip-by-openai
pip install clip-by-openai

# Or install from source
pip install git+https://github.com/openai/CLIP.git
```

---

## 📊 Expected Performance

**On NVIDIA A100 GPU:**
- 224x224, 1000 iterations: ~60 seconds
- 512x512, 1000 iterations: ~3 minutes

**On NVIDIA RTX 3090 GPU:**
- 224x224, 1000 iterations: ~90 seconds
- 512x512, 1000 iterations: ~4-5 minutes

**On CPU (slow!):**
- 224x224, 1000 iterations: ~10-15 minutes
- 512x512 not recommended

---

## 🎓 Understanding the Visualization

The generated images show what features maximally activate a specific neuron:

**Early Layers (resblocks 0-2):**
- Low-level visual features
- Edges, colors, textures

**Middle Layers (resblocks 3-6):**
- Intermediate features
- Shapes, patterns, orientations

**Late Layers (resblocks 7-11):**
- High-level semantic features
- Object parts, concepts

---

## 💡 Tips for Best Results

### 1. Use Good Parameters
- **Small iterations (300-500)**: Quick preview
- **Medium iterations (1000)**: Good balance (default)
- **Large iterations (2000+)**: Detailed results

### 2. Experiment with Learning Rate
- **0.01** (default): Works for most cases
- **0.001-0.005**: More stable, slower
- **0.02-0.05**: Faster but can be noisy

### 3. Layer Selection
- Early layers show low-level features
- Middle layers are most interpretable
- Late layers show semantic features

### 4. Reproducibility
- Use `--seed` flag for reproducible results
- Same seed = same result (if nothing else changes)

---

## 🔍 Exploring the Model

### List all layers:
```bash
python cli.py --list-layers | head -20
```

### Analyze a specific layer:
```bash
python cli.py --layer visual.transformer.resblocks.5.attn --neurons | head -10
```

### Generate multiple visualizations:
```bash
for i in {0..7}; do
  python cli.py \
    --layer visual.transformer.resblocks.5.attn \
    --neuron $i \
    --output neuron_$i.png
done
```

---

## 📚 Learn More

- **README.md**: Full documentation
- **layer_inspector.py**: Learn about layer structure
- **feature_visualizer.py**: Understand visualization algorithm
- **app.py**: See web interface implementation

---

## 🎉 Ready to Start?

1. **For beginners**: `streamlit run app.py`
2. **For quick demo**: `python quickstart.py`
3. **For command line**: `python cli.py --help`
4. **For coding**: Check the Python examples above

Enjoy exploring CLIP neurons! 🧠✨
