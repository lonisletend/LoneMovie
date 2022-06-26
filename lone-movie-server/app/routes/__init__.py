from flask import Flask
from .room import room
from .movie import movie


def init_routes(app: Flask):
    app.register_blueprint(room, url_prefix='/room')
    app.register_blueprint(movie, url_prefix='/movie')
