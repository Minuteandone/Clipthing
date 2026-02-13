@echo off
REM Quick setup script for local development with GitHub Pages deployment (Windows)

echo 🚀 CLIP Neuron Visualizer - GitHub Pages Setup
echo ================================================

REM Check Python version
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check Node version
echo ✓ Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found. Some features will be unavailable.
    echo    Install Node.js if you want to use the Next.js version.
)

REM Create virtual environment
echo ✓ Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo ✓ Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements-api.txt

REM Try to setup Node.js environment
node --version >nul 2>&1
if not errorlevel 1 (
    echo ✓ Setting up Node.js...
    cd web
    call npm install
    cd ..
)

REM Create output directory
if not exist "generated_images" mkdir generated_images

echo.
echo ✅ Setup complete!
echo.
echo To start developing:
echo.
echo 1. Start the backend API:
echo    python api_server.py
echo.
echo 2. In another terminal, open the web interface:
echo    - Option A (Simple HTML): Open index.html in your browser
echo    - Option B (Next.js dev): cd web ^&^& npm run dev
echo.
echo 3. Open your browser:
echo    - Simple HTML: file:///path/to/index.html
echo    - Next.js: http://localhost:3000
echo    - GitHub Pages: https://Minuteandone.github.io/Clipthing/
echo.
echo To deploy:
echo    git add .
echo    git commit -m "Changes"
echo    git push origin main
echo    # GitHub Actions automatically deploys to GitHub Pages!
echo.
