from flask import Flask, jsonify
from .extensions import db, migrate, jwt, init_redis
from .api import api_bp
from .web import web_bp
from .models import *  # noqa: F401,F403


def create_app(config_class: str | None = None) -> Flask:
    app = Flask(__name__)

    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        # Default to DevelopmentConfig
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    init_redis(app)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(web_bp)

    # Basic healthcheck
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    # Global error handlers (example)
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"message": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({"message": "Bad request"}), 400

    return app
