#!/bin/sh
set -e

echo "Loading data..."
python -m scripts.load_json

echo "Starting bot..."
python -m core.bot
