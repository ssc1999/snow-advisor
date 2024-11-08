# app/__init__.py
from flask import Flask, jsonify
from flask_cors import CORS
# Import and register blueprints
from .api.routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Apply CORS to the app

    # Register the blueprint with a URL prefix
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
