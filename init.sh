#!/bin/bash

## be sure the file has right permissions
## chmod +x init.sh

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Please source this script: source init.sh"
  exit 1
fi

# Install Homebrew if it's not already installed
if ! command -v brew &> /dev/null
then
  echo "Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew is already installed"
fi

# Install Python 3 if it's not already installed
if ! command -v python3 &> /dev/null
then
  echo "Python3 not found. Installing..."
  brew install python
else
  echo "Python3 is already installed"
fi

# Install pip if it's not already installed
if ! command -v pip3 &> /dev/null
then
  echo "pip3 not found. Installing..."
  brew install pip3
else
  echo "pip3 is already installed"
fi

# Install tesseract if it's not already installed
if ! command -v tesseract &> /dev/null
then
  echo "tesseract not found. Installing..."
  brew install tesseract
else
  echo "tesseract is already installed"
fi

# Set up a virtual environment
if [ ! -d "venv" ]
then
  echo "Creating a virtual environment..."
  python3 -m venv venv
else
  echo "Virtual environment already exists"
fi

# Activate the virtual environment
source venv/bin/activate

# Install Python virtual environment package if not installed
if ! python3 -m ensurepip &> /dev/null
then
  echo "Ensurepip not found. Installing..."
  python3 -m ensurepip
else
  echo "Ensurepip is already installed"
fi

# Upgrade pip
pip install --upgrade pip

# Install required Python packages
pip install -r requirements.txt

# Inform the user that setup is complete
echo "Environment setup is complete. Virtual environment is activated."

# Run the scripts in order
echo "Environment is all set up!"

