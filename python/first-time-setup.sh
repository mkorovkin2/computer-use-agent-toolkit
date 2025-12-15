#!/bin/bash

# Computer Use Agent Toolkit - First Time Setup Script
# This script sets up the development environment for the first time

set -e  # Exit on any error

echo "🤖 Computer Use Agent Toolkit - First Time Setup"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or later.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Found Python ${PYTHON_VERSION}${NC}"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)
echo "📁 Project root: ${PROJECT_ROOT}"
echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists at: ${PROJECT_ROOT}/venv${NC}"
    read -p "Do you want to remove it and create a fresh one? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf venv
    else
        echo "Using existing virtual environment..."
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🏗️  Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "📦 Upgrading pip to latest version..."
python -m pip install --upgrade pip --quiet
PIP_VERSION=$(pip --version | cut -d' ' -f2)
echo -e "${GREEN}✓ pip upgraded to version ${PIP_VERSION}${NC}"
echo ""

# Install the package
echo "📥 Installing computer-use-agent package..."
cd python
pip install -e . --quiet
echo -e "${GREEN}✓ Package installed in editable mode${NC}"
echo ""

# Optional: Install dev dependencies
read -p "📚 Do you want to install development dependencies (pytest, black, mypy)? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "📥 Installing dev dependencies..."
    pip install -e ".[dev]" --quiet
    echo -e "${GREEN}✓ Dev dependencies installed${NC}"
else
    echo "⏭️  Skipping dev dependencies"
fi
echo ""

# Verify installation
echo "🧪 Verifying installation..."
if python -c "import computer_use_agent" 2>/dev/null; then
    echo -e "${GREEN}✓ computer-use-agent package successfully imported${NC}"
else
    echo -e "${RED}❌ Failed to import computer-use-agent${NC}"
    exit 1
fi
echo ""

# Print success message
echo "=================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Set your Anthropic API key:"
echo -e "   ${BLUE}export ANTHROPIC_API_KEY='your-api-key-here'${NC}"
echo ""
echo "2. Activate the virtual environment (in future sessions):"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "3. Run an example:"
echo -e "   ${BLUE}cd examples/python${NC}"
echo -e "   ${BLUE}python 01_simple_click.py${NC}"
echo ""
echo "4. Or start coding:"
echo -e "   ${BLUE}python${NC}"
echo -e "   ${BLUE}>>> from computer_use_agent import ComputerUseAgent${NC}"
echo -e "   ${BLUE}>>> agent = ComputerUseAgent(api_key='your-key')${NC}"
echo ""
echo "📖 Documentation: ../README.md"
echo "💡 Examples: ../examples/python/"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"

