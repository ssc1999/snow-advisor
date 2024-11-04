# app/__init__.py
from flask import Flask
# Import and register blueprints
from .api.routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")  # Prefix set to /api

    return app
