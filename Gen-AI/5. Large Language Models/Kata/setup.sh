#!/bin/bash

# News Summarization Tool - Setup Script
# Run this script to set up the complete environment

echo "=========================================="
echo "News Summarization Tool Setup"
echo "=========================================="
echo ""

# Step 1: Install python3-venv (requires sudo)
echo "Step 1: Installing python3-venv (requires sudo password)..."
sudo apt install -y python3.12-venv

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to install python3-venv"
    echo "Please run: sudo apt install python3.12-venv"
    exit 1
fi

echo "✓ python3-venv installed successfully"
echo ""

# Step 2: Create virtual environment
echo "Step 2: Creating virtual environment..."
cd "/home/ishs/Desktop/Projects/MLops/MLOps/Gen-AI/5. Large Language Models/Kata"
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created successfully"
echo ""

# Step 3: Activate virtual environment and install dependencies
echo "Step 3: Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""

# Step 4: Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Step 4: Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key"
else
    echo "Step 4: .env file already exists"
fi

echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key:"
echo "   nano .env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "=========================================="

