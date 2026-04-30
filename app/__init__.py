from flask import Flask, render_template
from flask_restful import Api
from .routes import register_routes


def create_app():
    app = Flask(__name__)
    api = Api(app)
    register_routes(api)

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")

    return app