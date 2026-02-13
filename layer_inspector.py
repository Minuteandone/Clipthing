"""
Module for inspecting CLIP model layers and neurons.
"""

import torch
import torch.nn as nn
from typing import Dict, List, Tuple
import clip


class LayerInspector:
    """Inspects and provides information about CLIP model layers."""
    
    def __init__(self, model, model_name="ViT-B/32"):
        """
        Initialize the layer inspector.
        
        Args:
            model: The CLIP model
            model_name: Name of the model (e.g., "ViT-B/32")
        """
        self.model = model
        self.model_name = model_name
        self.layers_info = self._extract_layers()
    
    def _extract_layers(self) -> Dict[str, nn.Module]:
        """Extract all named layers from the model."""
        layers = {}
        
        # Get visual encoder layers
        for name, module in self.model.visual.named_modules():
            if name and not name.startswith('_'):
                layers[f"visual.{name}"] = module
        
        return layers
    
    def get_layer_names(self) -> List[str]:
        """Get all available layer names."""
        return sorted(list(self.layers_info.keys()))
    
    def get_layer(self, layer_name: str) -> nn.Module:
        """Get a specific layer by name."""
        return self.layers_info.get(layer_name)
    
    def get_layer_info(self, layer_name: str) -> Dict:
        """Get information about a specific layer."""
        layer = self.get_layer(layer_name)
        if layer is None:
            return {}
        
        info = {
            "name": layer_name,
            "type": type(layer).__name__,
            "parameters": sum(p.numel() for p in layer.parameters()),
        }
        
        # Try to determine output shape
        if hasattr(layer, 'out_features'):
            info['out_features'] = layer.out_features
        elif hasattr(layer, 'num_channels'):
            info['num_channels'] = layer.num_channels
        
        return info
    
    def get_neuron_names(self, layer_name: str) -> List[str]:
        """
        Get neuron names for a given layer.
        Returns semantic names based on common patterns.
        """
        layer = self.get_layer(layer_name)
        if layer is None:
            return []
        
        # Try to get number of output features
        num_neurons = 0
        if hasattr(layer, 'out_features'):
            num_neurons = layer.out_features
        elif hasattr(layer, 'weight') and len(layer.weight.shape) > 0:
            num_neurons = layer.weight.shape[0]
        
        if num_neurons == 0:
            return []
        
        # Generate semantic names based on layer type and position
        names = []
        layer_type = type(layer).__name__
        
        if isinstance(layer, nn.Linear):
            for i in range(num_neurons):
                # Create meaningful names for linear layers
                names.append(f"neuron_{i}")
        elif isinstance(layer, nn.Conv2d):
            channels = layer.out_channels if hasattr(layer, 'out_channels') else num_neurons
            for i in range(channels):
                names.append(f"channel_{i}")
        else:
            for i in range(min(num_neurons, 768)):  # Limit to reasonable number
                names.append(f"unit_{i}")
        
        return names
    
    def get_layer_output_shape(self, layer_name: str, input_shape: Tuple) -> Tuple:
        """
        Estimate the output shape of a layer given an input shape.
        """
        layer = self.get_layer(layer_name)
        if layer is None:
            return None
        
        try:
            with torch.no_grad():
                dummy_input = torch.randn(input_shape)
                if hasattr(layer, 'out_features'):
                    return (input_shape[0], layer.out_features)
                elif isinstance(layer, nn.Conv2d):
                    return (input_shape[0], layer.out_channels, input_shape[2], input_shape[3])
        except:
            pass
        
        return None
