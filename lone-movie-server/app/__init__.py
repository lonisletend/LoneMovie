from flask import Flask
from flask_cors import CORS

def create_app():
    from . import configs, sockets, routes, exts
    app = Flask(__name__)
    configs.init_config(app)
    sockets.init_sockets(app)
    routes.init_routes(app)
    exts.init_logger(app)
    exts.init_redis_client(app)
    CORS(app, supports_credentials=True)

    return app
