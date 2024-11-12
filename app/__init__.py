# app/__init__.py
from flask import Flask, jsonify
from flask_cors import CORS
# Import and register blueprints
from .api.weather.routes import bp as weather_bp
from .api.resorts.routes import bp as resort_bp
from .api.advisory.routes import bp as advisory_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Apply CORS to the app

    # Register the blueprint with a URL prefix
    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(resort_bp, url_prefix="/api/resorts")
    app.register_blueprint(advisory_bp, url_prefix="/api/advisory")

    return app
