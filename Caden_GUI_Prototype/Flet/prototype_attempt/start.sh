#!/bin/bash

# create virtual envirnment named .venv
python -m venv .venv

# check if os is windows or unix and activate venv
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    echo "Unix-like OS detected"
    # activate venv for unix
    source ./.venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Windows OS detected"
    # activate venv for windows
    ./.venv/Scripts/activate
else
    echo "Unknown OS"
    # stop script
    exit 1
fi



# install requirements
pip install -r "requirements.txt"

# run the application
flet run main.py
