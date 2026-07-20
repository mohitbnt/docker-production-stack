"""Dashboard blueprint (Redis cached stats)."""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from ..services import DashboardService

bp = Blueprint("dashboard", __name__)


@bp.get("/stats")
@jwt_required()
def stats():
    return jsonify(DashboardService.stats())


@bp.post("/cache/invalidate")
@jwt_required()
def invalidate():
    DashboardService.invalidate()
    return jsonify({"message": "Dashboard cache invalidated"})
