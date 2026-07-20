"""Assets blueprint."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..schemas import AssetSchema
from ..services import AssetService

bp = Blueprint("assets", __name__)


@bp.get("")
@jwt_required()
def list_assets():
    return jsonify([a.to_dict() for a in AssetService.list_all()])


@bp.post("")
@jwt_required()
def create_asset():
    data = AssetSchema().load(request.get_json(silent=True) or {})
    a = AssetService.create(data)
    return jsonify(a.to_dict()), 201


@bp.get("/<int:aid>")
@jwt_required()
def get_asset(aid: int):
    return jsonify(AssetService.get(aid).to_dict())


@bp.put("/<int:aid>")
@jwt_required()
def update_asset(aid: int):
    data = AssetSchema(partial=True).load(request.get_json(silent=True) or {})
    a = AssetService.update(aid, data)
    return jsonify(a.to_dict())


@bp.delete("/<int:aid>")
@jwt_required()
def delete_asset(aid: int):
    AssetService.delete(aid)
    return jsonify({"message": "Asset deleted"})
