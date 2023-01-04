import os
from flask import Flask

from config.settings import (
    db, migrate, cors, socket, jwt
)
from config.config import DevConfig, BASE_DIR_P


def create_app():
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR_P, 'templates'))
    app.config.from_object(DevConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    socket.init_app(app)
    jwt.init_app(app)
    from api import register_views
    register_views(app)
    return app
