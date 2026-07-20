"""Marshmallow schemas for request validation."""
from marshmallow import Schema, fields, validate

STATUS_VALUES = ["available", "assigned", "in_repair", "retired"]


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=1, max=255))


class DepartmentSchema(Schema):
    code = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(load_default=None, allow_none=True)


class EmployeeSchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    phone = fields.String(load_default=None, allow_none=True, validate=validate.Length(max=50))
    position = fields.String(load_default=None, allow_none=True, validate=validate.Length(max=120))
    department_id = fields.Integer(load_default=None, allow_none=True)


class AssetSchema(Schema):
    tag = fields.String(required=True, validate=validate.Length(min=1, max=80))
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    category = fields.String(load_default=None, allow_none=True, validate=validate.Length(max=120))
    status = fields.String(load_default="available", validate=validate.OneOf(STATUS_VALUES))
    assigned_to_id = fields.Integer(load_default=None, allow_none=True)
    purchased_at = fields.Date(load_default=None, allow_none=True)


class ProfileUpdateSchema(Schema):
    name = fields.String(load_default=None, allow_none=True, validate=validate.Length(max=255))
    password = fields.String(load_default=None, allow_none=True, validate=validate.Length(min=8, max=255))
