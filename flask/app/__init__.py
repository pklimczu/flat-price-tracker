import os
from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    from . import views
    app.register_blueprint(views.bp)

    return app