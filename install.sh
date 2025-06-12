#!/bin/bash

# Kubernetes Troubleshooting Slack Bot Installation Script

echo "Installing Kubernetes Troubleshooting Slack Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 before continuing."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file with your Slack and AWS credentials."
else
    echo ".env file already exists."
fi

# Make the script executable
chmod +x src/main.py

echo "Installation complete!"
echo "To start the bot, run: source venv/bin/activate && python src/main.py"
