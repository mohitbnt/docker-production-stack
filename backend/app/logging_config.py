"""Structured JSON logging configuration."""
import json
import logging
import os
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        for k, v in record.__dict__.items():
            if k in ("args", "msg", "levelname", "levelno", "pathname", "filename",
                     "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
                     "created", "msecs", "relativeCreated", "thread", "threadName",
                     "processName", "process", "name", "message"):
                continue
            try:
                json.dumps(v)
                payload[k] = v
            except (TypeError, ValueError):
                payload[k] = str(v)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(app):
    level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"), logging.INFO)
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.setLevel(level)
    root.addHandler(handler)
    root.setLevel(level)

    log_dir = app.config.get("LOG_DIR")
    if log_dir and os.path.isdir(log_dir) and os.access(log_dir, os.W_OK):
        file_handler = logging.FileHandler(os.path.join(log_dir, "opsportal.log"))
        file_handler.setFormatter(JsonFormatter())
        file_handler.setLevel(level)
        root.addHandler(file_handler)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    app.logger.setLevel(level)
