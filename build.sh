#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Starting Build Process ---"

# 1. Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 2. Build the Database & Similarity Matrix
# This runs backend/db/__main__.py logic
echo "Initializing database and processing movie data..."
python -m backend.db

# 3. Install Node dependencies and build the React Frontend
echo "Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "--- Build Complete ---"
