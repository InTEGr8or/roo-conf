#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Clean previous builds and dist directory
uv clean
rm -rf dist/

# Increment the patch version
uv run python increment_version.py

# Build the package using hatch
hatch build

# Publish the package to PyPI
uv publish -t $PYPI_API_TOKEN