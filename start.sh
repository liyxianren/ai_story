#!/bin/bash
# Startup script with explicit timeout configuration

echo "=================================================="
echo "Starting AI Story App with custom configuration"
echo "Gunicorn timeout: 600 seconds (10 minutes)"
echo "Graceful timeout: 120 seconds (2 minutes)"
echo "=================================================="

# Export environment variables
export GUNICORN_TIMEOUT=600
export GUNICORN_GRACEFUL_TIMEOUT=120

# Start gunicorn with explicit parameters
exec gunicorn app:app \
  --config gunicorn_config.py \
  --timeout 600 \
  --graceful-timeout 120 \
  --log-level info \
  --bind 0.0.0.0:${PORT:-8080} \
  --workers ${GUNICORN_WORKERS:-4} \
  --worker-class sync
