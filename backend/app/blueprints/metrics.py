"""Metrics blueprint (Prometheus)."""
from flask import Blueprint

from ..metrics import metrics_response

bp = Blueprint("metrics", __name__)


@bp.get("/metrics")
def metrics():
    return metrics_response()
