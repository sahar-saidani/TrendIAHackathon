#!/bin/bash

echo "Starting TrendAI Backend..."

if [ ! -f "backend/bot_detector.pkl" ]; then
    echo "Warning: bot_detector.pkl not found. Some features may not work."
fi

cd "$(dirname "$0")"
python integrated_api.py
