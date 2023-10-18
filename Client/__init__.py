import os
from flask import Flask
from flask_session import Session
from .routes import bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.register_blueprint(bp)
    Session(app)
    return app
