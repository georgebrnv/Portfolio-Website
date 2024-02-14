# gunicorn_config.py

# Number of worker processes
workers = 2

# Bind address
bind = '0.0.0.0:8000'

# Maximum number of requests a worker will process before restarting
# max_requests = 1000

# Maximum number of seconds a worker will run
# timeout = 30

# Log level
# loglevel = 'info'

# Enable access log
# accesslog = '-'  # Log to stdout