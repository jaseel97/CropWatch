#!/bin/bash

# Install setup tools from local files
echo "Installing dependencies for setuptools-69.2.0..."
cd dependencies-win/setuptools-69.2.0 || exit
python setup.py install
cd ../..

# Install pip from local files
echo "Installing dependencies for pip24.0..."
cd dependencies-win/pip24.0 || exit
python setup.py install
cd ../..

# Run pip install for requirements-deb.txt
echo "Installing requirements..."
pip install --no-index --find-links /dependencies-deb -r requirements-deb.txt

echo "Installation complete."