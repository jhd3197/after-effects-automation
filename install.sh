#!/bin/bash
# After Effects Automation - Installation Script
# This script installs the package in development mode

echo ""
echo "============================================================"
echo "After Effects Automation - Installation"
echo "============================================================"
echo ""

echo "Installing package in development mode..."
echo ""

pip install -e .

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "Installation Complete!"
    echo "============================================================"
    echo ""
    echo "The following commands are now available:"
    echo ""
    echo "  ae-automation run config.json"
    echo "  ae-automation editor config.json"
    echo "  ae-automation generate --all"
    echo "  ae-automation test"
    echo ""
    echo "Try running: ae-automation --help"
    echo ""
    echo "============================================================"
else
    echo ""
    echo "============================================================"
    echo "Installation Failed"
    echo "============================================================"
    echo ""
    echo "Please check the error messages above."
    echo "You may need to install Python dependencies first:"
    echo ""
    echo "  pip install -r requirements.txt"
    echo ""
    echo "============================================================"
fi
