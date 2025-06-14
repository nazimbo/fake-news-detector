#!/usr/bin/env bash
# Build script for Render
set -o errexit

pip install -r requirements.txt
python install_nltk.py

# Check if models exist and are accessible
if [ ! -d "models" ] || [ ! -f "models/vectorizer.joblib" ]; then
    echo "Models not found. Training new models..."
    python trainer_main.py
else
    echo "Models found, checking integrity..."
    ls -la models/
fi