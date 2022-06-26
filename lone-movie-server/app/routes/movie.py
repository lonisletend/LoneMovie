import traceback

from flask import Blueprint, request, current_app as app

from ..exts.redis_util import RedisUtil
from ..exts.enum import ErrCode
from ..exts.result import Ret

movie = Blueprint('/movie', __name__)


@movie.route('/')
def index():
    return Ret.success_msg("movie test!")


@movie.route('/getKey/<key>')
def test_redis(key):
    return Ret.success_ret(RedisUtil.get(key))

