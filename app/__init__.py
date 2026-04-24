from flask import Flask
from flask_restful import Api
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    api = Api(app)
    register_routes(api)
    return app

app = create_app()