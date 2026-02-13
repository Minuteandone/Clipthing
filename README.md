# 🧠 CLIP Neuron Visualizer

Generate images that maximally excite specific neurons in OpenAI's CLIP ViT-B/32 model. This tool provides deep insights into what visual features different neurons in the vision transformer respond to.

## Overview

This project implements feature visualization for CLIP's visual encoder. By optimizing random images to maximize the activation of specific neurons, we can visualize what each neuron "looks for" - providing interpretability into the model's learned representations.

**Features:**
- 🎯 Select any layer in CLIP's visual transformer
- 📍 Choose specific neurons with semantic names
- 🎨 Generate high-quality visualizations via gradient-based optimization
- 🖥️ Interactive web interface (Streamlit + Next.js)
- 💻 Command-line interface for batch processing
- 📊 Real-time progress tracking and activation monitoring
- 🌐 GitHub Pages deployment support

## 🚀 Quick Demo

**Try it online** (GitHub Pages hosted frontend): https://Minuteandone.github.io/Clipthing/
- Frontend is deployed and ready to use
- Connect to a backend API for image generation (see deployment guide)

## Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (optional but highly recommended, CPU will be very slow)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Minuteandone/Clipthing.git
cd Clipthing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The first time you run the application, it will automatically download the CLIP model (~340MB).

## Usage

### Option 0: Web Interface (GitHub Pages)

**No local installation needed!** The frontend is hosted on GitHub Pages:

👉 **https://Minuteandone.github.io/Clipthing/**

This provides a beautiful web interface that works in any modern browser. To use it, you'll need to connect it to a backend API:
- Run locally: `python api_server.py`
- Or use a cloud-hosted backend (Hugging Face Spaces, Vercel, etc.)

See [DEPLOY_GITHUB_PAGES.md](DEPLOY_GITHUB_PAGES.md) for detailed deployment instructions.

### Option 1: Interactive Web Interface (Recommended)

Launch the Streamlit web application:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- ✨ Real-time layer and neuron selection
- 📊 Live progress visualization with activation values
- 🎨 Interactive parameter tuning
- 💾 One-click image export

**Workflow:**
1. Select a layer from the visual encoder
2. Choose a specific neuron (with semantic name)
3. Adjust visualization parameters
4. Click "Generate Visualization"
5. Wait for optimization to complete
6. Save the generated image

### Option 2: Command-Line Interface

#### List available layers:
```bash
python cli.py --list-layers
```

#### List neurons in a layer:
```bash
python cli.py --layer visual.transformer.resblocks.0.attn --neurons
```

#### Generate an image:
```bash
python cli.py \
  --layer visual.transformer.resblocks.0.attn \
  --neuron 42 \
  --output my_visualization.png \
  --iterations 1000 \
  --size 224
```

#### Full CLI options:
```
--list-layers           List all available layers
--layer LAYER          Layer name (e.g., 'visual.transformer.resblocks.0.attn')
--neuron INDEX         Neuron index
--neurons              List neurons in selected layer
--output PATH          Output image path (default: generated_image.png)
--size SIZE            Image size (default: 224)
--iterations N         Number of iterations (default: 1000)
--lr RATE              Learning rate (default: 0.01)
--blur-every N         Apply blur every N iterations (default: 10)
--seed SEED            Random seed for reproducibility (default: 42)
```

### Option 3: API Server (for Web Interface)

Start a FastAPI backend server for the web interface:

```bash
# Install FastAPI dependencies
pip install -r requirements-api.txt

# Start the server
python api_server.py
# Server runs at http://localhost:8000
```

Then use:
- The web interface at `index.html` (no Node.js needed)
- Or the GitHub Pages version: https://Minuteandone.github.io/Clipthing/

For deployment to GitHub Pages with a backend, see [DEPLOY_GITHUB_PAGES.md](DEPLOY_GITHUB_PAGES.md)

## How It Works

### Feature Visualization Pipeline

1. **Initialization**: Start with a random image
2. **Forward Pass**: Input image through CLIP to target neuron
3. **Activation Capture**: Extract activation output from target neuron via backward hooks
4. **Optimization**: Use gradient descent to maximize the neuron's activation
5. **Regularization**: Apply:
   - Total variation loss for smoothness
   - Periodic Gaussian blur
   - Value clipping to maintain reasonable ranges
6. **Output**: Generate final visualization

### Architecture Details

**Model**: CLIP ViT-B/32
- Vision Transformer with 12 transformer blocks
- 768-dimensional embeddings
- Trained on 400 million image-text pairs

**Key Components**:
- `layer_inspector.py`: Analyzes model architecture and neuron properties
- `feature_visualizer.py`: Implements gradient-based feature visualization
- `app.py`: Streamlit web interface
- `cli.py`: Command-line interface
- `api_server.py`: FastAPI backend for web interface
- `web/`: Next.js React web application (GitHub Pages deployable)
- `index.html`: Standalone HTML interface (no Node.js required)

## Visualization Parameters

### Image Size (64-512)
Larger images can capture more spatial detail but take longer to optimize.
- 64px: Fast, coarse features
- 224px: Good balance (default)
- 512px: Detailed features, slow

### Iterations (100-5000)
More iterations = better optimized image but longer computation.
- 100: Quick preview
- 1000: Recommended (default)
- 5000: Detailed optimization

### Learning Rate (0.001-0.1)
Controls optimization step size.
- 0.001: Slow, stable
- 0.01: Balanced (default)
- 0.1: Fast, can be unstable

### Blur Every N Iterations (5-50)
Periodically smooths the image for more natural results.
- Smaller values: More blur, smoother results
- Larger values: Less blur, more detail
- Default: 10

## Understanding the Results

The generated images reveal:

1. **Early layers** (resblocks 0-2): Low-level visual features
   - Edges, textures, colors, simple patterns

2. **Middle layers** (resblocks 3-6): Intermediate features
   - Shapes, orientations, local patterns

3. **Late layers** (resblocks 7-11): High-level semantic features
   - Object parts, complex structures, semantic concepts

## Example Usage Scenarios

### Analyze attention head responses:
```bash
python cli.py --layer visual.transformer.resblocks.5.attn --neurons
python cli.py --layer visual.transformer.resblocks.5.attn --neuron 0 --output attn_head_0.png
```

### Generate detailed feature maps:
```bash
python cli.py \
  --layer visual.transformer.resblocks.10.mlp \
  --neuron 128 \
  --size 512 \
  --iterations 2000 \
  --output detailed_feature.png
```

### Reproducible experiments:
```bash
python cli.py \
  --layer visual.transformer.resblocks.3.attn \
  --neuron 64 \
  --seed 12345 \
  --output reproducible.png
```

## Performance

Estimated generation times (on NVIDIA A100 GPU):

| Image Size | Iterations | Time |
|-----------|-----------|------|
| 64x64     | 500       | 10s  |
| 224x224   | 1000      | 60s  |
| 512x512   | 1000      | 180s |
| 224x224   | 5000      | 300s |

CPU times will be 10-50x slower depending on your hardware.

## Project Structure

```
Clipthing/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── app.py                    # Streamlit web interface
├── cli.py                    # Command-line interface
├── layer_inspector.py        # Model analysis tools
├── feature_visualizer.py     # Feature visualization engine
└── generated_images/         # Output directory (auto-created)
```

## Troubleshooting

### Out of Memory (OOM) errors
- Reduce image size with `--size 128`
- Reduce iterations with `--iterations 500`
- Use CPU if GPU memory is limited (slower): change `device = "cpu"`

### Slow generation
- Reduce image size
- Reduce number of iterations
- Use GPU instead of CPU

### Model download issues
- Check internet connection
- The model (~340MB) will auto-download to `~/.cache/clip`
- You can manually download from OpenAI's CLIP repository

### Layer not found errors
- Use `--list-layers` to see exact layer names
- Layer names are case-sensitive

## Advanced Usage

### Batch generation script:

```python
from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer
import torch
import clip

model, _ = clip.load("ViT-B/32", device="cuda")
inspector = LayerInspector(model)
visualizer = FeatureVisualizer(model, device="cuda")

# Generate visualizations for multiple neurons
layer = "visual.transformer.resblocks.5.attn"
for neuron_idx in range(0, 64, 8):
    img = visualizer.generate_image(
        layer_name=layer,
        neuron_index=neuron_idx,
        num_iterations=1000
    )
    img.save(f"neuron_{neuron_idx}.png")
```

### Custom visualization parameters:

```python
# Fine-tuned for different layer types
params = {
    "visual.transformer.resblocks.0": {
        "iterations": 500,
        "lr": 0.02,
        "size": 128
    },
    "visual.transformer.resblocks.11": {
        "iterations": 2000,
        "lr": 0.01,
        "size": 224
    }
}
```

## Citation

If you use this tool in academic work, please cite:

```bibtex
@article{radford2021learning,
  title={Learning Transferable Visual Models From Natural Language Supervision},
  author={Radford, Alec and Kim, Jong Wook and Hallacy, Chris and others},
  journal={arXiv preprint arXiv:2103.00020},
  year={2021}
}
```

Feature visualization technique based on:
```bibtex
@article{erhan2009visualizing,
  title={Visualizing and Understanding Convolutional Networks},
  author={Erhan, Dumitru and Bengio, Yoshua and Courville, Aaron and Vincent, Pascal},
  journal={arXiv preprint arXiv:1311.2901},
  year={2013}
}
```

## License

This project is released under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Contact

For questions or discussions, please open an issue on the GitHub repository.

---

**Happy visualizing! 🎨✨**