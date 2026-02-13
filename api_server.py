"""
FastAPI backend for CLIP Neuron Visualizer web interface.
This server provides API endpoints for layer information, neuron names, and image generation.

Installation:
    pip install fastapi uvicorn python-multipart

Usage:
    uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import torch
import clip
from io import BytesIO
from typing import Optional

from layer_inspector import LayerInspector
from feature_visualizer import FeatureVisualizer

# Initialize FastAPI app
app = FastAPI(
    title="CLIP Neuron Visualizer API",
    description="API for generating CLIP neuron visualizations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
model = None
device = None
inspector = None
visualizer = None


def initialize_models():
    """Initialize CLIP model and utilities."""
    global model, device, inspector, visualizer
    
    if model is not None:
        return
    
    print("Loading CLIP model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    model, _ = clip.load("ViT-B/32", device=device)
    inspector = LayerInspector(model, model_name="ViT-B/32")
    visualizer = FeatureVisualizer(model, device=device)
    
    print("✓ Models loaded!")


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup."""
    initialize_models()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "device": device or "not initialized",
        "model": "CLIP ViT-B/32"
    }


@app.get("/api/layers")
async def get_layers():
    """Get list of available layers."""
    try:
        initialize_models()
        layers = inspector.get_layer_names()
        
        # Filter to interesting layers
        interesting_layers = [
            l for l in layers
            if any(x in l for x in ['transformer', 'attn', 'mlp', 'ln', 'proj'])
        ]
        
        if not interesting_layers:
            interesting_layers = layers
        
        return {
            "layers": interesting_layers,
            "total": len(layers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/neurons")
async def get_neurons(layer: str):
    """Get available neurons for a layer."""
    try:
        initialize_models()
        neurons = inspector.get_neuron_names(layer)
        return {
            "layer": layer,
            "neurons": neurons,
            "count": len(neurons)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid layer: {str(e)}")


@app.get("/api/layer-info")
async def get_layer_info(layer: str):
    """Get information about a specific layer."""
    try:
        initialize_models()
        info = inspector.get_layer_info(layer)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid layer: {str(e)}")


@app.post("/api/generate")
async def generate_visualization(
    layer_name: str,
    neuron_index: int,
    image_size: int = 224,
    num_iterations: int = 1000,
    learning_rate: float = 0.01,
    blur_every: int = 10,
    seed: int = 42
):
    """Generate a neuron visualization."""
    try:
        initialize_models()
        
        # Validate inputs
        if image_size < 64 or image_size > 512:
            raise ValueError("image_size must be between 64 and 512")
        
        if num_iterations < 100 or num_iterations > 5000:
            raise ValueError("num_iterations must be between 100 and 5000")
        
        # Generate image
        print(f"Generating: layer={layer_name}, neuron={neuron_index}")
        
        generated_image = visualizer.generate_image(
            layer_name=layer_name,
            neuron_index=neuron_index,
            image_size=image_size,
            num_iterations=num_iterations,
            learning_rate=learning_rate,
            blur_every=blur_every,
            seed=seed
        )
        
        # Convert to PNG bytes
        img_byte_arr = BytesIO()
        generated_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Return image
        return StreamingResponse(
            img_byte_arr,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=neuron_{neuron_index}.png"}
        )
    
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "name": "CLIP Neuron Visualizer API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "layers": "/api/layers",
            "neurons": "/api/neurons?layer=<layer_name>",
            "layer_info": "/api/layer-info?layer=<layer_name>",
            "generate": "/api/generate (POST)"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
