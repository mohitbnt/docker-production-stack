"""Auth blueprint: login, refresh, logout, me."""
import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt,
)

from ..schemas import LoginSchema
from ..services import AuthService
from ..repositories import UserRepo
from ..errors import UnauthorizedError
from ..cache import cache

bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


def _revoke_key(jti: str) -> str:
    return f"opsportal:revoked:{jti}"


@bp.post("/login")
def login():
    data = LoginSchema().load(request.get_json(silent=True) or {})
    user = AuthService.authenticate(data["email"], data["password"])
    access = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh = create_refresh_token(identity=str(user.id))
    logger.info("login_success", extra={"user_id": user.id, "email": user.email})
    return jsonify({"access_token": access, "refresh_token": refresh, "user": user.to_dict()})


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = get_jwt_identity()
    user = UserRepo.by_id(int(uid))
    if not user or not user.is_active:
        raise UnauthorizedError("User no longer active")
    access = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"access_token": access})


@bp.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt().get("jti")
    if jti and cache.is_available():
        cache.set(_revoke_key(jti), True, ttl=3600)
    return jsonify({"message": "Logged out"})


@bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = UserRepo.by_id(int(uid))
    if not user:
        raise UnauthorizedError("User not found")
    return jsonify(user.to_dict())
