#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Increment the patch version in pyproject.toml
python increment_version.py

# Clean previous builds and dist directory
uv clean
rm -rf dist/

# Build the package using hatch
hatch build

# Publish the package to PyPI
uv publish -t $PYPI_API_TOKEN