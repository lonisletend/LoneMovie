from flask import Flask
from logging.handlers import RotatingFileHandler
import logging
import os
from .base import redis_client


def init_logger(app: Flask):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/lonemovie.log', maxBytes=2 * 1024 * 1024, backupCount=20)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: [%(pathname)s:%(lineno)d] %(message)s '))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('LoneMovie startup')


def init_redis_client(app: Flask):
    redis_client.init_app(app)
