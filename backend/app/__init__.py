from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

from .config import SUPPORTED_PRODUCT_DOMAINS
from .api.predictor import predictor_bp
from .api.deals import deals_bp
from .api.workspace import workspace_bp


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config:
        app.config.update(test_config)

    # Register blueprints
    app.register_blueprint(predictor_bp)
    app.register_blueprint(deals_bp)
    app.register_blueprint(workspace_bp)

    @app.route('/')
    def index():
        return jsonify({
            "status": "running",
            "service": "Pricevana REST API",
            "supported_domains": SUPPORTED_PRODUCT_DOMAINS
        })

    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "service": "Pricevana REST API",
            "timestamp": datetime.utcnow().isoformat()
        })

    return app


app = create_app()
