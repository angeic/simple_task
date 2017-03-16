from flask import Flask, redirect, url_for
from webapp.config import DevConfig
from .models import db, User, Task


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Welcome to Simple Task!'

    return app