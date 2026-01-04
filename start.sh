#!/bin/bash
# Automated startup script for Word Frequency Mini Project (Linux/Mac)

echo "============================================================"
echo "Word Frequency Mini Project - Quick Start"
echo "============================================================"
echo ""

# Run the Python setup and start script
python3 start.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "============================================================"
    echo "Error occurred. Please check the messages above."
    echo "============================================================"
    read -p "Press Enter to continue..."
fi
