from flask import Flask
from flask_socketio import SocketIO
from .handler import init_handlers


def init_sockets(app: Flask):
    socketio = SocketIO(app, cors_allowed_origins="*")
    init_handlers(socketio)

