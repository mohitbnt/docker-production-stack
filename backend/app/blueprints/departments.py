"""Departments blueprint."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..schemas import DepartmentSchema
from ..services import DepartmentService

bp = Blueprint("departments", __name__)


@bp.get("")
@jwt_required()
def list_departments():
    return jsonify([d.to_dict() for d in DepartmentService.list_all()])


@bp.post("")
@jwt_required()
def create_department():
    data = DepartmentSchema().load(request.get_json(silent=True) or {})
    d = DepartmentService.create(data)
    return jsonify(d.to_dict()), 201


@bp.get("/<int:did>")
@jwt_required()
def get_department(did: int):
    return jsonify(DepartmentService.get(did).to_dict())


@bp.put("/<int:did>")
@jwt_required()
def update_department(did: int):
    data = DepartmentSchema(partial=True).load(request.get_json(silent=True) or {})
    d = DepartmentService.update(did, data)
    return jsonify(d.to_dict())


@bp.delete("/<int:did>")
@jwt_required()
def delete_department(did: int):
    DepartmentService.delete(did)
    return jsonify({"message": "Department deleted"})
