from flask import Flask
from .config import Config


def init_config(app: Flask):
    app.config.from_object(Config)
