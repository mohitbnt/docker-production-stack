"""Employees blueprint."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..schemas import EmployeeSchema
from ..services import EmployeeService

bp = Blueprint("employees", __name__)


@bp.get("")
@jwt_required()
def list_employees():
    q = request.args.get("q", type=str)
    items = EmployeeService.search(q)
    return jsonify([e.to_dict() for e in items])


@bp.post("")
@jwt_required()
def create_employee():
    data = EmployeeSchema().load(request.get_json(silent=True) or {})
    e = EmployeeService.create(data)
    return jsonify(e.to_dict()), 201


@bp.get("/<int:eid>")
@jwt_required()
def get_employee(eid: int):
    return jsonify(EmployeeService.get(eid).to_dict())


@bp.put("/<int:eid>")
@jwt_required()
def update_employee(eid: int):
    data = EmployeeSchema(partial=True).load(request.get_json(silent=True) or {})
    e = EmployeeService.update(eid, data)
    return jsonify(e.to_dict())


@bp.delete("/<int:eid>")
@jwt_required()
def delete_employee(eid: int):
    EmployeeService.delete(eid)
    return jsonify({"message": "Employee deleted"})
