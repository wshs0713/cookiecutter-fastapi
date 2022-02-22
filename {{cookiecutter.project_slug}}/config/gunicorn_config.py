"""Gunicorn config."""
import os

host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', '8000')

# Gunicorn parameters
# Server socket
bind = os.getenv('BIND', f'{host}:{port}')
backlog = 1024
chdir = '/app'

# Worker processes
workers = 2
worker_connections = 1000
timeout = 900
graceful_timeout = 120
keepalive = 30

# Logging
# Refer to https://docs.gunicorn.org/en/stable/settings.html#access-log-format
accesslog = os.getenv('ACCESS_LOG', '-')
errorlog = os.getenv('ERROR_LOG', '-')
loglevel = os.getenv('LOG_LEVEL', 'INFO')

access_log_format = '''
    [%(t)s] [%(p)s] %({x-forwarded-for}i)s %(l)s %(u)s "%(r)s" %(s)s %(T)s %(b)s "%(f)s" "%(a)s"
'''

# Server Mechanics
preload_app = True
forwarded_allow_ips = '*'
