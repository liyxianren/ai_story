# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'

# Timeout settings for large file uploads
timeout = 300  # 5 minutes - enough time for 30MB audio file uploads
graceful_timeout = 30
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
