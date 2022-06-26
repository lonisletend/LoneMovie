import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    REDIS_URL = os.environ.get('LONEMOVIE_REDIS_URL') or "redis://:123Abc.@localhost:6379/0"


