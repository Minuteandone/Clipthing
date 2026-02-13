# 🌐 Web Version - Complete Guide

Welcome to the GitHub Pages deployable version of CLIP Neuron Visualizer!

## What's New

The project now includes a web version that can be:
- ✅ Deployed to GitHub Pages (frontend)
- ✅ Connected to various backends (local, cloud, etc.)
- ✅ Used without any local installation
- ✅ Shared as a public URL

## Files Overview

### Frontend Options

| File | Purpose | Setup | Pros |
|------|---------|-------|------|
| `index.html` | Standalone HTML | Just open in browser | No build needed |
| `web/` | Next.js React app | `npm install && npm run dev` | Full-featured, customizable |
| GitHub Pages | Deployed version | Push to main branch | Already hosted, public |

### Backend

| File | Purpose | Setup | Use for |
|------|---------|-------|---------|
| `api_server.py` | FastAPI backend | `python api_server.py` | Local/remote deployment |
| `requirements-api.txt` | API dependencies | `pip install -r requirements-api.txt` | Installing backend |

## Getting Started (5 Minutes)

### Quickest Way: GitHub Pages + Local Backend

1. **Use the web interface** (no setup needed):
   - Open: https://Minuteandone.github.io/Clipthing/

2. **Start the backend** (Python):
   ```bash
   pip install -r requirements-api.txt
   python api_server.py
   ```

3. **Open the web URL** in your browser
   - The frontend will auto-connect to `http://localhost:8000`
   - Start generating!

## Step-by-Step Guides

### For Web Users
1. Open: https://Minuteandone.github.io/Clipthing/
2. Follow on-screen instructions
3. Select layer and neuron
4. Click "Generate"

**Note**: You'll need a backend running (see deployment options below)

### For Local Development

```bash
# Set up backend
pip install -r requirements-api.txt
python api_server.py
# Runs on http://localhost:8000

# In another terminal, use web interface
open index.html
# Or for Next.js development:
cd web && npm install && npm run dev
# Opens http://localhost:3000
```

### For Deploying Your Own Version

See detailed guides:
- **Quick**: [DEPLOY_GITHUB_PAGES.md](DEPLOY_GITHUB_PAGES.md)
- **Detailed**: [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md)

## Architecture

```
User's Browser
    ↓
Frontend (GitHub Pages / index.html / Local React)
    ↓ (API calls)
Backend Server (api_server.py)
    ↓
CLIP Model + Visualization Engine
    ↓
Generated Images
```

## Feature Comparison

### Command Line vs Web

| Feature | CLI | Web |
|---------|-----|-----|
| Setup | Easy | Medium (backend needed) |
| Use | Terminal | Browser |
| Batch processing | ✅ | ✅ (via parameters) |
| Real-time feedback | Limited | ✅ |
| Sharing results | Manual | Easy (download) |
| No installation | ❌ | ✅ |

### Local vs Cloud Backend

| Aspect | Local | Cloud |
|--------|-------|-------|
| Speed | Fast (GPU) | Slow (CPU usually) |
| Setup | Easy | Medium |
| Cost | Free | Free-$$$ |
| Accessibility | LAN only | Public URL |

## Deployment Options

### Quick Deploy (No Experience Needed)

```bash
# Just run this
pip install -r requirements-api.txt
python api_server.py

# Then open:
# https://Minuteandone.github.io/Clipthing/
# And set API to: http://localhost:8000
```

### Deploy to Cloud (30 minutes)

Choose one:

1. **Hugging Face Spaces** (Free, CPU, slow)
   - Go to https://huggingface.co/spaces
   - Create space, upload files
   - URL: `https://your-username-clipthing.hf.space`

2. **Vercel** (Free tier available)
   - Connect GitHub repo
   - Auto-deploys from pushes
   - URL: `https://your-deployment.vercel.app`

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for full instructions.

## Common Questions

### Q: Do I need to install anything?
**A**: Not to use the interface! Just open the GitHub Pages URL. You only need to run a backend (Python) for image generation.

### Q: Can I customize the interface?
**A**: Yes! Edit `index.html` for simple changes, or modify `web/` for advanced customization.

### Q: How do I deploy it?
**A**: Your changes auto-deploy to GitHub Pages when you push to `main`.

### Q: Is it free?
**A**: Frontend: Yes (GitHub Pages is free). Backend: Depends on choice (local is free, cloud varies).

### Q: How fast is image generation?
**A**: 
- Local with GPU: 1-2 minutes
- Local with CPU: 10-15 minutes  
- Cloud free tier: 5-10 minutes

### Q: Can multiple people use it simultaneously?
**A**: With a single-instance backend, yes but might queue. Use horizontal scaling for best results.

## File Structure

```
Clipthing/
├── 🌐 Web Frontend
│   ├── index.html                    # Standalone HTML interface
│   │   └── No build needed, just open
│   │
│   └── web/                          # Next.js React app
│       ├── app/page.tsx              # Main component
│       ├── app/layout.tsx            # Layout
│       ├── app/globals.css           # Tailwind CSS
│       ├── next.config.js            # Config for GitHub Pages
│       ├── package.json              # Dependencies
│       └── tailwind.config.ts        # Tailwind config
│
├── 🔌 Backend API
│   ├── api_server.py                 # FastAPI server
│   ├── requirements-api.txt          # API dependencies
│   ├── layer_inspector.py            # Model analysis
│   └── feature_visualizer.py         # Core engine
│
├── 📚 Documentation
│   ├── README.md                     # Main guide
│   ├── DEPLOY_GITHUB_PAGES.md        # Quick deploy guide
│   ├── WEB_DEPLOYMENT.md             # Full web guide
│   ├── WEB_FEATURES.md               # This file
│   ├── SETUP.md                      # Installation guide
│   ├── PROJECT.md                    # Project overview
│   └── QUICKSTART_REFERENCE.md       # Quick reference
│
└── ⚙️ Configuration
    ├── .github/workflows/deploy-pages.yml  # CI/CD
    └── .gitignore                    # Git ignore rules
```

## Key Technologies

- **Frontend**: Next.js, React, Tailwind CSS (or vanilla HTML)
- **Backend**: FastAPI, PyTorch, CLIP
- **Hosting**: GitHub Pages (frontend), various options for backend
- **API**: REST API with CORS support

## Next Steps

1. **Try it now**: https://Minuteandone.github.io/Clipthing/
2. **Run backend locally**: `python api_server.py`
3. **Deploy to cloud**: Follow [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md)
4. **Customize interface**: Edit `index.html` or `web/` files
5. **Share with others**: Give them the GitHub Pages URL

## Troubleshooting

### Can't connect to API
- Make sure backend is running: `python api_server.py`
- Check URL is correct in browser
- Check firewall allows connections

### Generation is very slow
- Using free cloud backend? (Expected)
- Try reducing image size and iterations
- Deploy your own backend with GPU

### Want to use CLI instead?
- Use `python cli.py` (see README.md)
- No web needed, runs locally

## Advanced Usage

### Custom Backend
Modify `api_server.py` to:
- Add authentication
- Add rate limiting
- Add caching
- Use different models

### Custom Frontend
Edit `index.html` or Next.js to:
- Change colors
- Add new features
- Integrate with other tools
- Create custom workflows

### API Integration
Use the REST API directly:
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"layer_name": "...", "neuron_index": 0, ...}'
```

## Getting Help

1. **Check documentation**: README.md, SETUP.md, WEB_DEPLOYMENT.md
2. **See examples**: Read index.html for API usage
3. **Open an issue**: GitHub Issues for bugs/features
4. **Check status**: `/health` endpoint for backend status

## Summary

| Want To... | Do This |
|-----------|---------|
| Use now | Open GitHub Pages URL + run `python api_server.py` |
| Deploy to cloud | Follow WEB_DEPLOYMENT.md |
| Modify interface | Edit index.html or web/ |
| Use CLI only | Python commands (see README) |
| Integrate with code | Use REST API (see api_server.py) |

---

**Ready? Start here**: https://Minuteandone.github.io/Clipthing/ 🚀
