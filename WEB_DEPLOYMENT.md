# 🌐 Web Deployment Guide

This guide covers all options for deploying CLIP Neuron Visualizer to the web.

## Overview

There are multiple ways to use the web interface:

1. **GitHub Pages (Recommended for most users)**: Pre-deployed frontend, connect to backend
2. **Standalone HTML**: Simple HTML file that works with any backend
3. **Next.js (Development)**: Full-featured React app for local testing
4. **API Server**: Backend service for handling computations

## Quick Start

### For Users (No Setup Required)

Open the GitHub Pages version: https://Minuteandone.github.io/Clipthing/

Then connect it to a backend API:
- **Local**: Run `python api_server.py` and connect to `http://localhost:8000`
- **Remote**: Use a cloud backend (see deployment options below)

### For Developers

```bash
# Clone repository
git clone https://github.com/Minuteandone/Clipthing.git
cd Clipthing

# Option A: Simple HTML interface
# Just open index.html in your browser with a running backend

# Option B: Next.js development
cd web
npm install
npm run dev
# Opens at http://localhost:3000

# In another terminal, start the backend
pip install -r ../requirements-api.txt
python api_server.py
```

## Option 1: GitHub Pages (Recommended)

### For Users

The frontend is already deployed at: https://Minuteandone.github.io/Clipthing/

To use it:

1. Choose a backend (see "Backend Options" section below)
2. Open the GitHub Pages URL
3. Configure API endpoint if needed

### For Developers (Deploying Changes)

```bash
cd web
npm install
npm run build
# Commits build output, GitHub Actions handles deployment automatically
```

GitHub Actions automatically builds and deploys when you push to `main`.

## Option 2: Standalone HTML

### For Users

Use the `index.html` file directly:

1. Start a backend API server
2. Open `index.html` in your browser
3. Configure API endpoint via URL parameter:

```
file:///path/to/index.html?api=http://localhost:8000
```

### For Developers

The `index.html` file is completely self-contained:
- No build step needed
- No Node.js required
- Works with any backend

To customize:

1. Open `index.html` in a text editor
2. Modify CSS in the `<style>` tag
3. Modify JavaScript in the `<script>` tag
4. Save and refresh in browser

## Option 3: Next.js Development

### Setup

```bash
cd web
npm install
```

### Development

```bash
npm run dev
# Opens at http://localhost:3000
```

### Production Build

```bash
npm run build
# Exports to ./out directory
```

### Customization

Edit:
- `app/page.tsx`: Main interface component
- `app/globals.css`: Styling
- `next.config.js`: Configuration

## Backend Options

### Option A: Local Backend (Development)

```bash
# Install dependencies
pip install -r requirements-api.txt

# Start server
python api_server.py
# Runs at http://localhost:8000
```

**Pros**:
- ✅ Full control
- ✅ No dependencies on external services
- ✅ GPU acceleration if available

**Cons**:
- ❌ Must run locally
- ❌ Only accessible from your machine

### Option B: Hugging Face Spaces (Free Tier)

**Setup** (5 minutes):

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - Name: `clipthing-visualizer`
   - License: OpenRAIL-M
   - Space SDK: `docker`
4. Upload files:
   - `api_server.py`
   - `layer_inspector.py`
   - `feature_visualizer.py`
   - `requirements-api.txt`
5. Create `Dockerfile`:

```dockerfile
FROM pytorch/pytorch:2.0-cuda11.8-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements-api.txt

EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

6. Space will build and deploy automatically

**URL**: `https://username-clipthing-visualizer.hf.space`

**Pros**:
- ✅ Free
- ✅ Public URL
- ✅ Auto-builds from git

**Cons**:
- ⚠️ CPU only (slow ~5-10 min per generation)
- ⚠️ Free tier has rate limits
- ⚠️ Sleeps after 48 hours of inactivity

### Option C: Vercel (Free Tier)

**Setup** (10 minutes):

1. Create account at https://vercel.com
2. Create `api/generate.py`:

```python
from api_server import app
handler = app
```

3. Create `vercel.json`:

```json
{
  "builds": [{"src": "api/**/*.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "api/generate.py"}]
}
```

4. Deploy:

```bash
npm install -g vercel
vercel
```

**URL**: `https://your-deployment.vercel.app`

**Pros**:
- ✅ Fast deployment
- ✅ Good uptime

**Cons**:
- ❌ CPU only (slow)
- ⚠️ Request timeout limits (60 seconds)
- ❌ Not ideal for long computations

### Option D: AWS EC2 with GPU (Paid)

Most powerful option, but requires budget.

**Setup**:

1. Launch EC2 instance with NVIDIA GPU
2. Install CUDA and Python
3. Upload code to instance
4. Start API server
5. Use Elastic IP for stable URL

**Pros**:
- ✅ Fast GPU computation
- ✅ Unlimited usage
- ✅ Full control

**Cons**:
- ❌ Costs money ($0.50-5/hour for GPU instances)
- ❌ Requires AWS knowledge

### Option E: Google Cloud Run with GPU

Similar to AWS but with container support.

## Configuration

### Frontend Configuration

The frontend looks for the API endpoint in this order:

1. **URL parameter**: `https://domain.com?api=http://localhost:8000`
2. **Environment variable**: `NEXT_PUBLIC_API_ENDPOINT`
3. **Default**: `http://localhost:8000`

### Backend Configuration

The API server needs:
- Python 3.8+
- PyTorch with CLIP
- ~8GB VRAM for comfortable operation

Set device in `api_server.py`:
```python
device = "cuda"  # or "cpu"
```

## Troubleshooting

### "API connection failed"

**Problem**: Frontend can't reach backend

**Solutions**:
1. Check backend is running: `curl http://your-api:8000/health`
2. Check CORS is enabled
3. Check firewall allows connections
4. Verify URL in frontend

### "Out of memory"

**Problem**: GPU runs out of memory

**Solutions**:
```bash
# Use CPU instead
# In api_server.py, change:
device = "cpu"

# Or reduce parameters:
# --size 128 --iterations 300
```

### "Very slow generation"

**Problem**: Taking 10+ minutes

**Solutions**:
- Using CPU? (Expected 10-15 min)
- Using free Hugging Face? (Expected 5-10 min)
- Reduce iterations/size

## Comparison Table

| Option | Setup Time | Cost | Speed | Scalability |
|--------|-----------|------|-------|-------------|
| Local  | 2 min | Free | Fast | Local only |
| HF Spaces | 5 min | Free | Slow | Limited |
| Vercel | 10 min | Free | Very slow | Limited |
| AWS GPU | 30 min | $$$ | Fast | Unlimited |
| Vercel GPU | 20 min | $$$ | Fast | Scalable |

## Deployment Checklist

- [ ] Choose backend option
- [ ] Deploy backend API
- [ ] Test API health endpoint
- [ ] Update frontend API endpoint
- [ ] Test generation works
- [ ] Share URL with others

## Advanced: Custom Domain + HTTPS

### Cloudflare (Free)

1. Add domain to Cloudflare
2. Set nameservers
3. Works with any backend

### GitHub Pages + Custom Domain

1. Add `CNAME` file to repository with your domain
2. Configure DNS records
3. GitHub provides HTTPS

## Monitoring & Maintenance

### Check Backend Health

```bash
curl https://your-api/health
```

### View Logs

**Local**: Check terminal where server runs

**Hugging Face**: Check "Logs" tab in Space

**Vercel**: Check "Functions" tab in dashboard

### Update Code

```bash
git push origin main
# Automatic re-deployment
```

## Performance Tips

1. **Cache Generated Images**: Reduce duplicate generations
2. **Use CDN**: For image delivery
3. **Horizontal Scaling**: Run multiple API instances
4. **Use GPU**: Critical for reasonable times
5. **Optimize Parameters**: Smaller images are faster

## Security Considerations

1. **Rate Limiting**: Prevent abuse
2. **Authentication**: Optional API key
3. **CORS**: Currently allows all origins (restrict if needed)
4. **HTTPS**: Always use for production

## Support

For issues:
1. Check logs
2. Verify API is running
3. Check network connectivity
4. Open GitHub issue with details

---

Choose your deployment option and get started! 🚀
