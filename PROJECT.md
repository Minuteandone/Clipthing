# 📖 Project Overview

## What is CLIP Neuron Visualizer?

A sophisticated tool for visualizing what specific neurons in OpenAI's CLIP vision model "see" and respond to. By generating images that maximally excite individual neurons, we can understand the learned visual features at different layers of the model.

## 🗂 Project Structure

```
Clipthing/
│
├── 📄 README.md                    Main documentation
├── 📄 SETUP.md                     Installation & troubleshooting
├── 📄 LICENSE                      MIT License
├── 📄 requirements.txt             Python dependencies
│
├── 🎨 Core Application
│   ├── app.py                      Streamlit web interface (interactive)
│   ├── cli.py                      Command-line interface
│   ├── batch.py                    Batch processing tool
│   └── quickstart.py               Quick start example
│
├── 🔧 Utilities
│   ├── layer_inspector.py          Analyzes model architecture
│   └── feature_visualizer.py       Implements visualization algorithm
│
└── 📁 generated_images/            Output directory (auto-created)
```

## 📚 Key Files Explained

### `app.py` - Web Interface
**Purpose**: Interactive Streamlit application for exploring neurons
**Use**: Best for beginners and interactive exploration
```bash
streamlit run app.py
```
**Features**:
- Real-time layer and neuron selection
- Parameter adjustment sliders
- Live progress visualization
- One-click image export

### `cli.py` - Command Line Interface
**Purpose**: Batch processing and automated visualization
**Use**: Perfect for scripts and automation
```bash
python cli.py --layer <name> --neuron <idx>
```
**Features**:
- List all layers
- List neurons in a layer
- Generate with custom parameters
- Scripting-friendly

### `batch.py` - Batch Processing
**Purpose**: Generate multiple visualizations efficiently
**Use**: When you need many neurons visualized
```bash
python batch.py --layer <name> --neuron-range 0 64 8
```
**Features**:
- Process multiple neurons at once
- Automatic progress tracking
- Metadata file generation
- Skip existing files

### `quickstart.py` - Quick Start
**Purpose**: Demo to verify installation works
**Use**: First time users
```bash
python quickstart.py
```
**Features**:
- Generates one demo visualization
- Shows how to use the library
- ~30-60 seconds total time

### `layer_inspector.py` - Model Analysis
**Purpose**: Inspect CLIP architecture and neurons
**Key Classes**:
- `LayerInspector`: Analyze layers and get neuron names

**Used by**: All other tools
**Example**:
```python
from layer_inspector import LayerInspector
inspector = LayerInspector(model)
layers = inspector.get_layer_names()
neurons = inspector.get_neuron_names(layer)
```

### `feature_visualizer.py` - Visualization Engine
**Purpose**: Core algorithm for generating visualizations
**Key Classes**:
- `NeuronActivationHook`: Captures neuron outputs
- `FeatureVisualizer`: Generates images via optimization

**Used by**: All other tools
**Core Algorithm**:
1. Start with random image
2. Forward pass through model
3. Capture target neuron activation
4. Backprop to compute gradients
5. Update image to maximize activation
6. Apply regularization (blur, TV loss)
7. Repeat until convergence

## 🎯 Usage Paths

### For Interactive Exploration
```bash
1. pip install -r requirements.txt
2. streamlit run app.py
3. Click buttons and sliders
4. Save images
```

### For Quick Demo
```bash
1. pip install -r requirements.txt
2. python quickstart.py
3. Check generated_images/ folder
```

### For Command Line
```bash
1. pip install -r requirements.txt
2. python cli.py --list-layers            # See available layers
3. python cli.py --layer X --neurons     # See neurons
4. python cli.py --layer X --neuron Y   # Generate!
```

### For Batch Processing
```bash
1. pip install -r requirements.txt
2. python batch.py --layer X --neuron-range 0 64 8
3. Grab coffee ☕
4. Check generated_images/ for results
```

### For Custom Scripts
```python
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer
import torch, clip

model, _ = clip.load("ViT-B/32", device="cuda")
visualizer = FeatureVisualizer(model, device="cuda")

img = visualizer.generate_image(
    layer_name="visual.transformer.resblocks.5.attn",
    neuron_index=32,
    num_iterations=1000
)
img.save("output.png")
```

## 🔍 Understanding the Model

### CLIP Architecture
```
Input Image (224×224)
    ↓
Patch Embedding (16×16 patches)
    ↓
Transformer Encoder (12 blocks)
    ├─ Block 0-2: Low-level features
    ├─ Block 3-6: Mid-level features
    └─ Block 7-11: High-level features
    ↓
Vision Output (768-dim)
```

### Layer Hierarchy
- `visual.conv1`: Initial patch embedding
- `visual.transformer`: Main transformer blocks
  - `visual.transformer.resblocks.N.ln_1`: Layer norm
  - `visual.transformer.resblocks.N.attn`: Multi-head attention
  - `visual.transformer.resblocks.N.mlp`: Feed-forward network
  - `visual.transformer.resblocks.N.ln_2`: Layer norm

## 🎨 What the Visualizations Show

### Early Layers (blocks 0-2)
Show **low-level visual features**:
- Edges and boundaries
- Colors and gradients
- Simple textures
- Oriented lines

**Example**: A neuron might respond to red vertical edges

### Middle Layers (blocks 3-6)
Show **intermediate features**:
- Shapes (circles, corners)
- Patterns and repetitions
- Surface properties
- Object-part orientations

**Example**: A neuron might respond to circular shapes

### Late Layers (blocks 7-11)
Show **high-level semantic features**:
- Object parts (eyes, wheels)
- Entire objects
- Scenes
- Complex concepts

**Example**: A neuron might respond to faces or animals

## ⚙️ Technical Details

### Optimization Algorithm
- **Optimizer**: Adam (adaptive learning)
- **Loss**: Negative neuron activation (gradient ascent)
- **Regularization**:
  - Total Variation (smoothness)
  - Periodic Gaussian blur
  - Value clipping

### Hyperparameters
- **Iterations**: 100-5000 (more = better but slower)
- **Learning Rate**: 0.001-0.1 (balance between speed and stability)
- **Image Size**: 64-512 (larger = more detail but slower)
- **Blur**: Apply every 5-50 iterations for smoothness

### Performance
- GPU (A100): ~60 sec for 224×224, 1000 iter
- GPU (RTX 3090): ~90 sec for 224×224, 1000 iter
- CPU: 10-15 min (very slow!)

## 🚀 Getting Started

### Absolute Beginner
1. `pip install -r requirements.txt`
2. `streamlit run app.py`
3. Click around and enjoy!

### Want to Experiment
1. `python cli.py --list-layers | grep resblocks`
2. Pick an interesting layer
3. `python cli.py --layer visual.transformer.resblocks.5.attn --neuron 0 --output my_viz.png`

### Want to Integrate
1. Import `LayerInspector` and `FeatureVisualizer`
2. Load your CLIP model
3. Call `visualizer.generate_image()`
4. Process the returned PIL Image

### Want Batch Jobs
1. `python batch.py --layer visual.transformer.resblocks.5.attn --neuron-range 0 768 16`
2. Let it run (will create metadata.json with results)

## 📊 Example Workflows

### Explore Attention Heads
```bash
# See what attention heads in resblock 5 respond to
python cli.py --layer visual.transformer.resblocks.5.attn --neurons
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 0 --output attn_0.png
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 1 --output attn_1.png
# ... repeat for all interesting heads
```

### Examine Layer Progression
```bash
# Compare same neuron index across layers
for layer in 0 3 6 9; do
  python cli.py \
    --layer visual.transformer.resblocks.$layer.mlp \
    --neuron 256 \
    --output layer_$layer.png
done
```

### High-Quality Visualizations
```bash
# For publication/detailed analysis
python cli.py \
  --layer visual.transformer.resblocks.7.attn \
  --neuron 128 \
  --size 512 \
  --iterations 2000 \
  --lr 0.005 \
  --blur-every 20 \
  --output high_quality.png
```

## 🔧 Customization

### Add Custom Layers
The tool automatically discovers all layers. No changes needed!

### Adjust Visualization Quality
Edit `feature_visualizer.py`:
```python
# More regularization (smoother)
tv_loss = self._total_variation(image) * 0.02  # Increase

# Less blur (more detail)
kernel_size = 2  # Smaller kernel

# Different optimizer
optimizer = torch.optim.SGD([image], lr=learning_rate)
```

### Change Model
Replace `"ViT-B/32"` with other CLIP models:
- `"ViT-B/16"` - larger vision encoder
- `"ViT-L/14"` - even larger
- `"RN50"` - ResNet variant

## 💾 Output Files

### Generated Images
- Path: `generated_images/`
- Format: PNG (lossless)
- Name: `neuron_<idx>_<layer>_<timestamp>.png`

### Batch Metadata
- Path: `generated_images/<layer>_metadata.json`
- Contains: Status, parameters, file locations

## 🐛 Troubleshooting

See SETUP.md for common issues and solutions.

## 📝 Citation

If you use this tool, please cite CLIP:

```bibtex
@article{radford2021learning,
  title={Learning Transferable Visual Models From Natural Language Supervision},
  author={Radford, Alec and Kim, Jong Wook and Hallacy, Chris and others},
  journal={arXiv preprint arXiv:2103.00020},
  year={2021}
}
```

## 🎓 Learn More

- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [Feature Visualization Overview](https://distill.pub/2017/feature-visualization/)
- [Understanding Vision Transformers](https://arxiv.org/abs/2010.11929)

## 🎉 Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Check [SETUP.md](SETUP.md) for installation help
3. Run [quickstart.py](quickstart.py) for a demo
4. Launch [app.py](app.py) for interactive exploration

Happy exploring! 🧠✨
