#!/bin/bash

# Quick Start Guide for Iris ML Classifier
# Copy this script and run it to get started immediately

echo "🌸 Iris ML Classifier - Quick Start"
echo "===================================="
echo ""

# Create project directory
PROJECT_DIR="iris-ml-project"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo "✓ Creating project structure..."

# Create directories
mkdir -p templates

# Copy all files from the setup
echo "✓ Setting up Flask application..."

# Python virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv

# Activate and install
echo "✓ Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install Flask scikit-learn numpy pandas

echo ""
echo "===================================="
echo "✅ Setup Complete!"
echo "===================================="
echo ""
echo "📖 Next Steps:"
echo "1. Copy app.py to the project directory"
echo "2. Copy templates/index.html to the templates folder"
echo "3. Run: source venv/bin/activate"
echo "4. Run: python app.py"
echo "5. Open: http://localhost:5000"
echo ""
echo "🚀 Start predicting flowers!"
