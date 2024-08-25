#!/bin/bash

# Ensure that pip is available
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Installing pip..."
    apt-get update && apt-get install -y python3-pip
fi

# Install Python dependencies
pip install -r requirements.txt

# Run Django collectstatic
python3.9 manage.py collectstatic --noinput
