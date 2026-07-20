"""Global error handling."""
import logging
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class AppError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int = None, details=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.details = details


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class UnauthorizedError(AppError):
    status_code = 401


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        logger.info("app_error", extra={"error": e.message, "status": e.status_code})
        return jsonify({"error": e.message, "details": e.details}), e.status_code

    @app.errorhandler(ValidationError)
    def handle_validation(e: ValidationError):
        return jsonify({"error": "Validation error", "details": e.messages}), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity(e: IntegrityError):
        logger.warning("integrity_error", extra={"error": str(e.orig)})
        return jsonify({"error": "Database integrity error", "details": str(e.orig)}), 409

    @app.errorhandler(SQLAlchemyError)
    def handle_sqla(e: SQLAlchemyError):
        logger.exception("sqlalchemy_error")
        return jsonify({"error": "Database error"}), 500

    @app.errorhandler(HTTPException)
    def handle_http(e: HTTPException):
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        logger.exception("unhandled_exception")
        return jsonify({"error": "Internal server error"}), 500
