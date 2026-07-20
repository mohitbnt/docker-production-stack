"""Gunicorn production configuration."""
import multiprocessing
import os

bind = f"{os.getenv('APP_HOST', '0.0.0.0')}:{os.getenv('APP_PORT', '8000')}"
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv("GUNICORN_THREADS", 2))
worker_class = "gthread"
timeout = int(os.getenv("GUNICORN_TIMEOUT", 60))
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("APP_LOG_LEVEL", "info").lower()
proc_name = "opsportal"
