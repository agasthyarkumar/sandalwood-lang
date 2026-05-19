#!/bin/bash

# ================================================
# Sandalwood Language - Initialization Script
# ================================================
# Automates the setup of the Sandalwood language
# environment and installation.
# ================================================

set -e

echo "🎬 Sandalwood Language - Setup"
echo "=============================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

# Compare versions
INSTALLED_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
INSTALLED_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
REQUIRED_MAJOR=$(echo "$REQUIRED_VERSION" | cut -d. -f1)
REQUIRED_MINOR=$(echo "$REQUIRED_VERSION" | cut -d. -f2)

if [ "$INSTALLED_MAJOR" -lt "$REQUIRED_MAJOR" ] || \
   ([ "$INSTALLED_MAJOR" -eq "$REQUIRED_MAJOR" ] && [ "$INSTALLED_MINOR" -lt "$REQUIRED_MINOR" ]); then
  echo "❌ Error: Python $REQUIRED_VERSION or higher is required"
  echo "   Found: Python $PYTHON_VERSION"
  exit 1
fi

echo "✓ Python $PYTHON_VERSION found"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installing Sandalwood in development mode..."
cd "$SCRIPT_DIR"

# Install the package in development mode
python3 -m pip install -e . --quiet

echo "✓ Sandalwood installed successfully"
echo ""

# Verify installation
echo "Verifying installation..."
if command -v sandal &> /dev/null; then
  echo "✓ 'sandal' command is available"
else
  echo "❌ Error: 'sandal' command not found"
  echo "   Try: pip install -e ."
  exit 1
fi

echo ""
echo "=============================="
echo "✓ Setup Complete!"
echo "=============================="
echo ""
echo "Next steps:"
echo "  • Run an example: sandal examples/hello.sw"
echo "  • View manual: cat usermanual.md"
echo "  • Get help: sandal --help"
echo ""
