from flask import Flask
from .routes import api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    CORS(app)
    return app