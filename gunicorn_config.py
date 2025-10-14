# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Worker processes - reduce workers to avoid memory issues with large uploads
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # Max 4 workers
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeout settings for large file uploads
# Allow override via environment variable for Zeabur
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '600'))  # Default 10 minutes
graceful_timeout = int(os.environ.get('GUNICORN_GRACEFUL_TIMEOUT', '120'))  # Default 2 minutes
keepalive = 5

# Log the actual timeout values being used
import sys
sys.stderr.write(f"[GUNICORN CONFIG] timeout={timeout}s, graceful_timeout={graceful_timeout}s\n")
sys.stderr.flush()

# Request settings
limit_request_line = 0  # No limit on request line size
limit_request_fields = 100
limit_request_field_size = 0  # No limit on request field size

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'ai_story_app'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in future)
keyfile = None
certfile = None
