from flask import Flask
from flask_restful import Api
from app.db import init_db
from .routes import register_routes
from .db import init_db

def create_app():
    app = Flask(__name__)
    api = Api(app)
    register_routes(api)
    with app.app_context():
        init_db()
    return app

app = create_app()