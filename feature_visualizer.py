"""
Feature visualization module for generating images that maximize neuron activations.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from tqdm import tqdm
from typing import Callable, Tuple


class NeuronActivationHook:
    """Hook to capture and maximize neuron activations."""
    
    def __init__(self, neuron_index: int = None):
        """
        Initialize the hook.
        
        Args:
            neuron_index: Index of the neuron to track. If None, uses mean activation.
        """
        self.neuron_index = neuron_index
        self.activation = None
    
    def __call__(self, module, input, output):
        """Capture the activation."""
        self.activation = output
    
    def get_activation_value(self) -> torch.Tensor:
        """Get the activation value for the target neuron."""
        if self.activation is None:
            return torch.tensor(0.0)
        
        activation = self.activation
        
        # Handle different output shapes
        if len(activation.shape) == 4:  # Conv layer output (B, C, H, W)
            if self.neuron_index is not None:
                activation = activation[:, self.neuron_index, :, :]
            else:
                activation = activation.mean(dim=1)  # Average over channels
        elif len(activation.shape) == 2:  # Linear layer output (B, F)
            if self.neuron_index is not None:
                activation = activation[:, self.neuron_index]
            else:
                activation = activation.mean(dim=1)
        
        return activation.mean()  # Return mean activation


class FeatureVisualizer:
    """Generates images that maximize neuron activations."""
    
    def __init__(self, model: nn.Module, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        Initialize the feature visualizer.
        
        Args:
            model: The neural network model
            device: Device to run on (cuda or cpu)
        """
        self.model = model.to(device)
        self.device = device
        self.model.eval()
        
        # Disable gradients for the model
        for param in self.model.parameters():
            param.requires_grad = False
        
        # Image normalization stats (ImageNet)
        self.normalize = transforms.Normalize(
            mean=[0.48145466, 0.4578275, 0.40821073],
            std=[0.26862954, 0.26130258, 0.27577711]
        )
    
    def generate_image(
        self,
        layer_name: str,
        neuron_index: int,
        image_size: int = 224,
        num_iterations: int = 1000,
        learning_rate: float = 0.01,
        blur_every: int = 10,
        seed: int = None,
        progress_callback: Callable = None
    ) -> Image.Image:
        """
        Generate an image that maximally activates a specific neuron.
        
        Args:
            layer_name: Name of the layer (e.g., 'visual.transformer.resblocks.0')
            neuron_index: Index of the neuron to maximize
            image_size: Size of generated image
            num_iterations: Number of optimization iterations
            learning_rate: Learning rate for optimization
            blur_every: Apply blur every N iterations
            seed: Random seed for reproducibility
            progress_callback: Function to track progress
        
        Returns:
            PIL Image of the generated visualization
        """
        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)
        
        # Initialize random image
        image = torch.randn(1, 3, image_size, image_size, device=self.device, requires_grad=True)
        
        # Create optimizer
        optimizer = torch.optim.Adam([image], lr=learning_rate)
        
        # Register hook to capture activations
        target_layer = self._get_layer_by_name(layer_name)
        if target_layer is None:
            raise ValueError(f"Layer {layer_name} not found")
        
        hook = NeuronActivationHook(neuron_index)
        handle = target_layer.register_forward_hook(hook)
        
        try:
            for iteration in range(num_iterations):
                optimizer.zero_grad()
                
                # Normalize image
                normalized_image = self.normalize(image)
                
                # Forward pass through model
                with torch.no_grad():
                    _ = self.model.visual(normalized_image)
                
                # Get activation value
                activation = hook.get_activation_value()
                
                # Compute loss (negative because we want to maximize)
                loss = -activation
                
                # Backward pass
                loss.backward()
                
                # Apply gradient update
                optimizer.step()
                
                # Apply total variation regularization
                with torch.no_grad():
                    tv_loss = self._total_variation(image)
                    image.data -= 0.01 * tv_loss
                
                # Apply periodic blur for smoothness
                if (iteration + 1) % blur_every == 0:
                    with torch.no_grad():
                        image.data = self._apply_blur(image.data)
                
                # Clamp values to valid range
                with torch.no_grad():
                    image.data.clamp_(-2.0, 2.0)
                
                # Progress callback
                if progress_callback and (iteration + 1) % max(1, num_iterations // 20) == 0:
                    progress_callback(iteration + 1, num_iterations, float(activation.item()))
        
        finally:
            handle.remove()
        
        # Convert to PIL Image
        with torch.no_grad():
            img_np = self._tensor_to_image(image.detach())
        
        return Image.fromarray(img_np)
    
    def _get_layer_by_name(self, layer_name: str) -> nn.Module:
        """Get a layer by its name."""
        parts = layer_name.split('.')
        module = self.model
        
        for part in parts:
            if hasattr(module, part):
                module = getattr(module, part)
            else:
                return None
        
        return module
    
    def _total_variation(self, image: torch.Tensor) -> torch.Tensor:
        """Compute total variation loss."""
        diff1 = image[:, :, :, :-1] - image[:, :, :, 1:]
        diff2 = image[:, :, :-1, :] - image[:, :, 1:, :]
        
        tv = torch.mean(torch.abs(diff1)) + torch.mean(torch.abs(diff2))
        return tv
    
    def _apply_blur(self, image: torch.Tensor, kernel_size: int = 3) -> torch.Tensor:
        """Apply Gaussian blur to image."""
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        padding = kernel_size // 2
        blurred = F.avg_pool2d(image, kernel_size=kernel_size, stride=1, padding=padding)
        return blurred
    
    def _tensor_to_image(self, image_tensor: torch.Tensor) -> np.ndarray:
        """Convert tensor to numpy image array."""
        # Denormalize using ImageNet stats
        image_tensor = image_tensor.cpu().squeeze(0).permute(1, 2, 0)
        
        # Manual denormalization
        mean = torch.tensor([0.48145466, 0.4578275, 0.40821073])
        std = torch.tensor([0.26862954, 0.26130258, 0.27577711])
        
        image_tensor = image_tensor * std + mean
        
        # Clamp to [0, 1]
        image_tensor = torch.clamp(image_tensor, 0, 1)
        
        # Convert to uint8
        image_array = (image_tensor.numpy() * 255).astype(np.uint8)
        
        return image_array
