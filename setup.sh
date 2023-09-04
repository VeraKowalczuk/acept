#!/bin/bash -x

# setup python virtual environment for the project
python -m venv venv
source venv/bin/activate
which python
# this should return: .../venv/bin/python

# install the project requirements
# pip install -r requirements.txt
# install the project dependencies and the project as a package in editable mode
pip install -e .

# Fetch dependencies in submodules
git submodule update --init --recursive

# UrbanHeatPro
pip install -e deps/UrbanHeatPro/

# urbs

