#!/bin/bash
set -e

# Install dependencies if requirements.txt exists
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

# Execute the command passed to the container (default: bash)
exec "$@"
