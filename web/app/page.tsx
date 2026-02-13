'use client';

import React, { useState, useEffect } from 'react';
import { AlertCircle, Zap, Github, Info } from 'lucide-react';
import axios from 'axios';

const API_ENDPOINT = process.env.NEXT_PUBLIC_API_ENDPOINT || 'http://localhost:8000';

interface LayerInfo {
  name: string;
  type: string;
  parameters: number;
  out_features?: number;
}

interface GenerationState {
  isGenerating: boolean;
  progress: number;
  currentActivation: number;
  error: string | null;
}

export default function Home() {
  const [layers, setLayers] = useState<string[]>([]);
  const [selectedLayer, setSelectedLayer] = useState<string>('');
  const [neurons, setNeurons] = useState<string[]>([]);
  const [selectedNeuron, setSelectedNeuron] = useState<number>(0);
  const [layerInfo, setLayerInfo] = useState<LayerInfo | null>(null);
  const [generationState, setGenerationState] = useState<GenerationState>({
    isGenerating: false,
    progress: 0,
    currentActivation: 0,
    error: null,
  });
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  
  // Parameters
  const [imageSize, setImageSize] = useState(224);
  const [iterations, setIterations] = useState(1000);
  const [learningRate, setLearningRate] = useState(0.01);
  const [blurEvery, setBlurEvery] = useState(10);
  const [seed, setSeed] = useState(42);

  // Load layers on mount
  useEffect(() => {
    loadLayers();
  }, []);

  // Load neurons when layer changes
  useEffect(() => {
    if (selectedLayer) {
      loadNeurons();
      loadLayerInfo();
    }
  }, [selectedLayer]);

  const loadLayers = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINT}/api/layers`);
      setLayers(response.data.layers || []);
      if (response.data.layers && response.data.layers.length > 0) {
        setSelectedLayer(response.data.layers[0]);
      }
    } catch (error) {
      setGenerationState(prev => ({
        ...prev,
        error: 'Failed to load layers. Make sure the backend is running.'
      }));
      // Use default layers if API fails
      setLayers([
        'visual.transformer.resblocks.0.attn',
        'visual.transformer.resblocks.5.attn',
        'visual.transformer.resblocks.11.attn',
      ]);
    }
  };

  const loadNeurons = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINT}/api/neurons`, {
        params: { layer: selectedLayer }
      });
      setNeurons(response.data.neurons || []);
      setSelectedNeuron(0);
    } catch (error) {
      console.error('Failed to load neurons:', error);
      // Generate default neuron names
      const defaultNeurons = Array.from({ length: 64 }, (_, i) => `neuron_${i}`);
      setNeurons(defaultNeurons);
    }
  };

  const loadLayerInfo = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINT}/api/layer-info`, {
        params: { layer: selectedLayer }
      });
      setLayerInfo(response.data);
    } catch (error) {
      console.error('Failed to load layer info:', error);
    }
  };

  const generateVisualization = async () => {
    setGenerationState({
      isGenerating: true,
      progress: 0,
      currentActivation: 0,
      error: null,
    });

    try {
      const response = await axios.post(
        `${API_ENDPOINT}/api/generate`,
        {
          layer_name: selectedLayer,
          neuron_index: selectedNeuron,
          image_size: imageSize,
          num_iterations: iterations,
          learning_rate: learningRate,
          blur_every: blurEvery,
          seed: seed,
        },
        {
          responseType: 'blob',
        }
      );

      const imageUrl = URL.createObjectURL(response.data);
      setGeneratedImage(imageUrl);
      
      setGenerationState(prev => ({
        ...prev,
        isGenerating: false,
        progress: 100,
      }));
    } catch (error: any) {
      setGenerationState(prev => ({
        ...prev,
        isGenerating: false,
        error: error.response?.data?.detail || 'Failed to generate visualization. Make sure the backend is running.',
      }));
    }
  };

  const downloadImage = () => {
    if (!generatedImage) return;
    
    const link = document.createElement('a');
    link.href = generatedImage;
    link.download = `neuron_${selectedNeuron}_${selectedLayer.replace(/\./g, '_')}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Zap className="w-8 h-8 text-purple-400" />
            <h1 className="text-4xl font-bold text-white">🧠 CLIP Neuron Visualizer</h1>
          </div>
          <p className="text-purple-200">Generate images that maximally excite specific neurons in CLIP-ViT-B/32</p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Control Panel */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800 rounded-lg p-6 border border-purple-500/30">
              <h2 className="text-xl font-bold text-white mb-4">Controls</h2>

              {/* Layer Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-purple-200 mb-2">
                  Layer
                </label>
                <select
                  value={selectedLayer}
                  onChange={(e) => setSelectedLayer(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-700 text-white rounded border border-purple-500/50 focus:border-purple-400 focus:outline-none"
                >
                  {layers.map(layer => (
                    <option key={layer} value={layer}>{layer}</option>
                  ))}
                </select>
              </div>

              {/* Neuron Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-purple-200 mb-2">
                  Neuron ({neurons[selectedNeuron] || 'N/A'})
                </label>
                <select
                  value={selectedNeuron}
                  onChange={(e) => setSelectedNeuron(parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-700 text-white rounded border border-purple-500/50 focus:border-purple-400 focus:outline-none"
                >
                  {neurons.map((neuron, idx) => (
                    <option key={idx} value={idx}>{idx}: {neuron}</option>
                  ))}
                </select>
              </div>

              {/* Layer Info */}
              {layerInfo && (
                <div className="mb-6 p-4 bg-slate-700/50 rounded border border-purple-500/20">
                  <p className="text-xs text-purple-300 mb-1">
                    <strong>Type:</strong> {layerInfo.type}
                  </p>
                  <p className="text-xs text-purple-300">
                    <strong>Parameters:</strong> {layerInfo.parameters?.toLocaleString() || 'N/A'}
                  </p>
                </div>
              )}

              {/* Parameters */}
              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2">
                    Image Size: {imageSize}×{imageSize}
                  </label>
                  <input
                    type="range"
                    min="64"
                    max="512"
                    step="32"
                    value={imageSize}
                    onChange={(e) => setImageSize(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2">
                    Iterations: {iterations}
                  </label>
                  <input
                    type="range"
                    min="100"
                    max="5000"
                    step="100"
                    value={iterations}
                    onChange={(e) => setIterations(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2">
                    Learning Rate: {learningRate.toFixed(3)}
                  </label>
                  <input
                    type="range"
                    min="0.001"
                    max="0.1"
                    step="0.001"
                    value={learningRate}
                    onChange={(e) => setLearningRate(parseFloat(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2">
                    Blur Every: {blurEvery}
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="50"
                    step="1"
                    value={blurEvery}
                    onChange={(e) => setBlurEvery(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2">
                    Seed: {seed}
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="10000"
                    value={seed}
                    onChange={(e) => setSeed(parseInt(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-700 text-white rounded border border-purple-500/50"
                  />
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateVisualization}
                disabled={generationState.isGenerating}
                className={`w-full py-3 rounded font-bold transition-colors ${
                  generationState.isGenerating
                    ? 'bg-purple-600/50 text-purple-200 cursor-not-allowed'
                    : 'bg-purple-600 hover:bg-purple-700 text-white'
                }`}
              >
                {generationState.isGenerating ? `Generating... ${generationState.progress}%` : '🚀 Generate'}
              </button>

              {/* Error Message */}
              {generationState.error && (
                <div className="mt-4 p-4 bg-red-900/30 border border-red-500/50 rounded flex gap-2 text-red-300 text-sm">
                  <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-medium mb-1">Connection Error</p>
                    <p className="text-xs">{generationState.error}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Info Box */}
            <div className="mt-6 bg-blue-900/30 border border-blue-500/50 rounded-lg p-4 text-blue-200 text-sm">
              <div className="flex gap-2 mb-2">
                <Info className="w-5 h-5 flex-shrink-0" />
                <strong>Note:</strong>
              </div>
              <p className="text-xs leading-relaxed">
                This web version requires a backend API running. For local development, run the Python backend server.
              </p>
            </div>
          </div>

          {/* Visualization Area */}
          <div className="lg:col-span-2">
            <div className="bg-slate-800 rounded-lg p-6 border border-purple-500/30 h-full">
              {generatedImage ? (
                <div>
                  <h2 className="text-xl font-bold text-white mb-4">Generated Visualization</h2>
                  <div className="bg-slate-900 rounded-lg p-4 mb-4">
                    <img
                      src={generatedImage}
                      alt="Generated visualization"
                      className="w-full rounded"
                    />
                  </div>
                  <div className="space-y-2">
                    <button
                      onClick={downloadImage}
                      className="w-full py-2 bg-green-600 hover:bg-green-700 text-white rounded font-semibold transition-colors"
                    >
                      💾 Download Image
                    </button>
                    <button
                      onClick={() => setGeneratedImage(null)}
                      className="w-full py-2 bg-slate-700 hover:bg-slate-600 text-white rounded font-semibold transition-colors"
                    >
                      ✨ Generate Another
                    </button>
                  </div>
                </div>
              ) : (
                <div className="h-full flex items-center justify-center text-center">
                  <div>
                    <Zap className="w-16 h-16 text-purple-400/30 mx-auto mb-4" />
                    <p className="text-purple-300 text-lg">Select parameters and click "Generate" to create a visualization</p>
                    <p className="text-purple-400 text-sm mt-2">The image will appear here once generation is complete</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 pt-8 border-t border-purple-500/20">
          <div className="flex items-center justify-between text-purple-300 text-sm">
            <p>CLIP Neuron Visualizer • Powered by OpenAI CLIP</p>
            <a href="https://github.com/Minuteandone/Clipthing" className="flex items-center gap-2 hover:text-purple-200">
              <Github className="w-4 h-4" />
              GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
