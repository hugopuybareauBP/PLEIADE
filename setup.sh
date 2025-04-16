#!/bin/bash

echo "🚀 Starting full project setup..."

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "env_pleiade" ]; then
    echo "🐍 Creating Python virtual environment (env_pleiade)..."
    python3 -m venv env_pleiade
else
    echo "✅ Python virtual environment already exists."
fi

# Step 2: Activate virtual environment and install backend dependencies
echo "📦 Installing backend dependencies from requirements.txt..."
source env_pleiade/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Step 3: Install frontend dependencies
if [ -d "frontend" ]; then
    echo "🧱 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "⚠️ Frontend folder not found. Skipping frontend setup."
fi

echo "✅ Setup complete!"
echo ""
echo "➡️ To activate the Python environment:"
echo "source env_pleiade/bin/activate"
echo "➡️ To run the backend:"
echo "export PYTHONPATH=$(pwd)"
echo "python backend/app/main.py"
echo "➡️ To run the frontend:"
echo "cd frontend && npm run dev"
