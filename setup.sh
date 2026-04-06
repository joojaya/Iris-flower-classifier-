#!/bin/bash

# Iris ML Classifier Setup Script
# This script sets up the entire project environment

echo "======================================"
echo "🌸 Iris ML Classifier Setup"
echo "======================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
python -m venv venv
echo "  Virtual environment created"
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Virtual environment activated"
echo ""

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "  Pip upgraded"
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt
echo "  Dependencies installed"
echo ""

# Create necessary directories
echo "✓ Creating directories..."
mkdir -p templates
echo "  Directories created"
echo ""

# Verify installation
echo "✓ Verifying installation..."
python -c "import flask; import sklearn; import numpy; print('  All dependencies verified!')"
echo ""

echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run Flask app: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "Happy predicting! 🌸🚀"
