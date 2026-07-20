"""Application factory."""
import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify

# Load .env from backend dir if present
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from .config import get_config
from .extensions import db, migrate, jwt, cors
from .logging_config import configure_logging
from .errors import register_error_handlers
from .cache import cache
from .metrics import init_metrics

logger = logging.getLogger(__name__)


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or get_config())

    configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
                  supports_credentials=False)
    cache.init_app(app)

    # Import models so Flask-Migrate sees them
    from .models import user, employee, department, asset  # noqa: F401

    # Register blueprints
    from .blueprints.auth import bp as auth_bp
    from .blueprints.employees import bp as employees_bp
    from .blueprints.departments import bp as departments_bp
    from .blueprints.assets import bp as assets_bp
    from .blueprints.dashboard import bp as dashboard_bp
    from .blueprints.profile import bp as profile_bp
    from .blueprints.health import bp as health_bp
    from .blueprints.metrics import bp as metrics_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(employees_bp, url_prefix="/api/employees")
    app.register_blueprint(departments_bp, url_prefix="/api/departments")
    app.register_blueprint(assets_bp, url_prefix="/api/assets")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(metrics_bp, url_prefix="/api")

    register_error_handlers(app)
    init_metrics(app)

    @app.route("/api")
    def api_root():
        return jsonify({
            "name": app.config["APP_NAME"],
            "env": app.config["APP_ENV"],
            "status": "ok",
        })

    # JWT error handlers -> JSON
    @jwt.unauthorized_loader
    def _missing_token(reason):
        return jsonify({"error": f"Missing Authorization header: {reason}"}), 401

    @jwt.invalid_token_loader
    def _invalid_token(reason):
        return jsonify({"error": f"Invalid token: {reason}"}), 401

    @jwt.expired_token_loader
    def _expired_token(jwt_header, jwt_payload):
        return jsonify({"error": "Token expired"}), 401

    @jwt.revoked_token_loader
    def _revoked_token(jwt_header, jwt_payload):
        return jsonify({"error": "Token revoked"}), 401

    logger.info("app_ready", extra={"env": app.config["APP_ENV"]})
    return app
