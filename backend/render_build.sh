#!/usr/bin/env bash
# Build script for Render
set -o errexit

pip install -r requirements.txt
python install_nltk.py

# If models don't exist, you might need to generate them
if [ ! -d "models" ]; then
    echo "Models directory not found. Please ensure models are committed to repo."
fi