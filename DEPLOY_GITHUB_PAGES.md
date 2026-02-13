# 🚀 GitHub Pages Deployment Guide

This guide covers deploying the CLIP Neuron Visualizer to GitHub Pages.

## Overview

The project now includes a web-based version that can be deployed to GitHub Pages:
- **Frontend**: Next.js React application (static export)
- **Backend**: FastAPI server (can be deployed separately)

## Architecture

```
GitHub Pages (Frontend)
    ↓ (API calls)
Remote Backend Server
    ↓
CLIP Model + Visualization Engine
    ↓
Generated Images
```

## Quick Start (3 steps)

### 1. Prerequisites
- GitHub account with this repository
- Node.js 18+ (for local development)
- Python 3.8+ (for backend)

### 2. Deploy Frontend to GitHub Pages

#### Automatic (Recommended)

The repository includes GitHub Actions workflow that automatically deploys when you push to `main`:

```bash
# Just push to main branch
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

The frontend will be available at: `https://Minuteandone.github.io/Clipthing/`

#### Manual

```bash
cd web
npm install
npm run build
# Output is in ./out directory
```

### 3. Setup Backend API

You need a backend server to handle image generation. Choose one:

#### Option A: Local Development

```bash
# Install Python dependencies
pip install fastapi uvicorn python-multipart
pip install -r requirements.txt

# Start the API server
python api_server.py
# Server runs at http://localhost:8000
```

Then open the web app and set `NEXT_PUBLIC_API_ENDPOINT=http://localhost:8000`

#### Option B: Hugging Face Spaces (Free)

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Create new Space with "Docker" runtime
3. Upload these files:
   - `api_server.py`
   - `layer_inspector.py`
   - `feature_visualizer.py`
   - `requirements.txt`
4. Create `Dockerfile`:

```dockerfile
FROM pytorch/pytorch:2.0-cuda11.8-runtime-ubuntu22.04

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

5. Update `.env.local` in web folder:
```
NEXT_PUBLIC_API_ENDPOINT=https://your-username-clipthing.hf.space
```

#### Option C: Deploy Backend to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json` in root:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "projectSettings": {
    "pythonVersion": "3.9"
  }
}
```

3. Deploy:
```bash
vercel
```

4. Update `.env.local`:
```
NEXT_PUBLIC_API_ENDPOINT=https://your-deployment.vercel.app
```

## Configuration

### Frontend Configuration

Edit `web/.env.local`:

```env
# For local backend
NEXT_PUBLIC_API_ENDPOINT=http://localhost:8000

# For remote backend
NEXT_PUBLIC_API_ENDPOINT=https://api.example.com
```

### Backend Configuration

The FastAPI server automatically:
- Loads CLIP model
- Provides all endpoints
- Handles CORS for frontend requests

## File Structure

```
Clipthing/
├── web/                          # Next.js frontend
│   ├── app/
│   │   ├── page.tsx             # Main interface
│   │   ├── layout.tsx           # Layout
│   │   └── globals.css          # Tailwind styles
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── .env.local.example
│
├── api_server.py                # FastAPI backend
├── layer_inspector.py           # Utilities
├── feature_visualizer.py        # Visualization
├── requirements.txt
│
└── .github/workflows/
    └── deploy-pages.yml         # GitHub Actions
```

## API Endpoints

### GET `/health`
Health check endpoint
```bash
curl http://localhost:8000/health
```

### GET `/api/layers`
List all available layers
```bash
curl http://localhost:8000/api/layers
```

### GET `/api/neurons?layer=<layer_name>`
List neurons in a specific layer
```bash
curl "http://localhost:8000/api/neurons?layer=visual.transformer.resblocks.5.attn"
```

### GET `/api/layer-info?layer=<layer_name>`
Get information about a layer
```bash
curl "http://localhost:8000/api/layer-info?layer=visual.transformer.resblocks.5.attn"
```

### POST `/api/generate`
Generate visualization
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "layer_name": "visual.transformer.resblocks.5.attn",
    "neuron_index": 32,
    "image_size": 224,
    "num_iterations": 1000,
    "learning_rate": 0.01,
    "blur_every": 10,
    "seed": 42
  }' \
  --output visualization.png
```

## Troubleshooting

### "API connection failed"

**Problem**: Frontend can't reach backend API

**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS is enabled in `api_server.py`
3. Verify `NEXT_PUBLIC_API_ENDPOINT` is correct in `.env.local`

### "Model not found"

**Problem**: Backend can't load CLIP model

**Solution**:
```bash
# Pre-download model
python -c "import clip; clip.load('ViT-B/32')"
# Model caches to ~/.cache/clip/
```

### GitHub Pages shows blank page

**Problem**: Frontend doesn't load

**Solution**:
1. Check `basePath` in `web/next.config.js` is `/Clipthing`
2. Run: `cd web && npm run build`
3. Check `./web/out` has output files

### Slow generation

**Problem**: Takes too long or fails

**Solution**:
- Reduce `image_size` (224 → 128)
- Reduce `iterations` (1000 → 500)
- Use GPU backend: check `/health` endpoint

## Deployment Summary

### Frontend (GitHub Pages) ✓
- Automatic via GitHub Actions
- Deployed at: `https://Minuteandone.github.io/Clipthing/`
- Updates on every push to `main`

### Backend (Choose One)

| Option | Ease | Cost | Speed |
|--------|------|------|-------|
| Local Dev | Easy | Free | Fast (GPU) |
| HF Spaces | Medium | Free | Slow (CPU) |
| Vercel | Medium | Free ($) | Slow (needs GPU addon) |
| Custom VPS | Hard | $$$ | Fast (GPU) |

## Next Steps

1. ✅ Frontend deployed to GitHub Pages
2. ⬜ Choose and deploy a backend
3. ⬜ Update `.env.local` with backend URL
4. ⬜ Test the web interface
5. ⬜ Share with others!

## Useful Links

- [Next.js Export Documentation](https://nextjs.org/docs/advanced-features/static-html-export)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Pages Docs](https://pages.github.com/)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)
- [Vercel Deployment](https://vercel.com/docs)

## Contributing

To improve the deployment:

1. Fork the repository
2. Create a feature branch
3. Make changes to `web/` or `api_server.py`
4. Test locally
5. Submit a pull request

## Support

For issues or questions:
1. Check existing [GitHub Issues](https://github.com/Minuteandone/Clipthing/issues)
2. Open a new issue with details
3. Include error messages and steps to reproduce

---

**Happy deploying! 🚀**
