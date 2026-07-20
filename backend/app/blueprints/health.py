"""Health blueprint: /api/health and /api/health/ready."""
import logging
from flask import Blueprint, jsonify, current_app
from sqlalchemy import text

from ..extensions import db
from ..cache import cache

bp = Blueprint("health", __name__)
logger = logging.getLogger(__name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": current_app.config["APP_NAME"]})


@bp.get("/health/ready")
def ready():
    checks = {"database": False, "redis": False}
    http_status = 200
    try:
        db.session.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception as exc:
        logger.warning("healthcheck_db_failed", extra={"error": str(exc)})
        http_status = 503
    try:
        checks["redis"] = cache.is_available()
    except Exception:
        checks["redis"] = False
    if not checks["redis"]:
        # redis is a soft dependency for readiness (cache degrades gracefully)
        pass
    return jsonify({"status": "ok" if http_status == 200 else "degraded", "checks": checks}), http_status
