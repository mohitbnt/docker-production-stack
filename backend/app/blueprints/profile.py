"""Profile blueprint (current user)."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..schemas import ProfileUpdateSchema
from ..repositories import UserRepo
from ..services import ProfileService
from ..errors import UnauthorizedError

bp = Blueprint("profile", __name__)


@bp.get("")
@jwt_required()
def get_profile():
    uid = get_jwt_identity()
    user = UserRepo.by_id(int(uid))
    if not user:
        raise UnauthorizedError("User not found")
    return jsonify(user.to_dict())


@bp.put("")
@jwt_required()
def update_profile():
    uid = get_jwt_identity()
    user = UserRepo.by_id(int(uid))
    if not user:
        raise UnauthorizedError("User not found")
    data = ProfileUpdateSchema().load(request.get_json(silent=True) or {})
    user = ProfileService.update(user, data)
    return jsonify(user.to_dict())
