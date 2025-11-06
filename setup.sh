#!/bin/bash
# Setup script for Local RAG Pipeline

echo "🚀 Setting up Local RAG Pipeline..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.8+ is required. Found: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p my_documents
mkdir -p my_rag_storage
echo "✅ Directories created"
echo ""

# Check for GPU
echo "🎮 Checking for GPU support..."
python3 -c "import torch; print('✅ GPU available:', torch.cuda.is_available())"
echo ""

echo "="*80
echo "✨ Setup complete!"
echo "="*80
echo ""
echo "Next steps:"
echo "1. Place your documents in ./my_documents/"
echo "2. Run: python rag_interface.py --documents ./my_documents"
echo "3. Start querying your documents!"
echo ""
echo "For help: python rag_interface.py --help"
echo ""
echo "Optional: Try the examples with 'python example_usage.py'"
echo ""
