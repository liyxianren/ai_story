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
timeout = 600  # 10 minutes - enough time for 30MB audio file uploads and processing
graceful_timeout = 120  # 2 minutes for graceful shutdown
keepalive = 5

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
