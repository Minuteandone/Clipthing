#!/bin/bash
# Quick setup script for local development with GitHub Pages deployment

echo "🚀 CLIP Neuron Visualizer - GitHub Pages Setup"
echo "================================================"

# Check Python version
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Node version
echo "✓ Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Some features will be unavailable."
    echo "   Install Node.js if you want to use the Next.js version."
fi

# Create virtual environment
echo "✓ Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements-api.txt

# Try to setup Node.js environment
if command -v node &> /dev/null; then
    echo "✓ Setting up Node.js..."
    cd web
    npm install
    cd ..
fi

# Create output directory
mkdir -p generated_images

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start developing:"
echo ""
echo "1. Start the backend API:"
echo "   python api_server.py"
echo ""
echo "2. In another terminal, open the web interface:"
echo "   - Option A (Simple HTML): Open index.html in your browser"
echo "   - Option B (Next.js dev): cd web && npm run dev"
echo ""
echo "3. Open your browser:"
echo "   - Simple HTML: file:///path/to/index.html"
echo "   - Next.js: http://localhost:3000"
echo "   - GitHub Pages: https://Minuteandone.github.io/Clipthing/"
echo ""
echo "To deploy:"
echo "   git add ."
echo "   git commit -m 'Changes'"
echo "   git push origin main"
echo "   # GitHub Actions automatically deploys to GitHub Pages!"
echo ""
