#!/usr/bin/env python3
"""
Production startup script for AI Storytelling Platform
"""

import os
from app import app, Config, logger

if __name__ == '__main__':
    # Set production environment
    os.environ.setdefault('FLASK_ENV', 'production')
    
    # Create necessary directories
    os.makedirs('/image', exist_ok=True)
    
    # Get port from environment or default
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting AI Storytelling Platform on port {port}")
    logger.info(f"Environment: {Config.FLASK_ENV}")
    
    # Run with production settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )