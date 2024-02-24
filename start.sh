#!/bin/bash

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Homebrew is installed, if not, install it
if ! command_exists brew; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check if Pipenv is installed, if not, install it
if ! command_exists gh; then
    echo "Installing Pipenv..."
    brew install pipenv
fi

# Check if Pipenv is installed, if not, install it
if ! command_exists pipenv; then
    echo "Installing Pipenv..."
    brew install pipenv
fi

# Navigate to the directory containing main.py
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Copy folder contents to /usr/local/lib/dealfront-scraper


# Install dependencies using Pipenv
pipenv install

# Activate the virtual environment
pipenv shell

# # Run the main.py file
python main.py