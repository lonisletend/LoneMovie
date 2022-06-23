from re import S
from flask import Flask

def create_app():
    from . import sockets
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    sockets.init_sockets(app)
    return app
