import traceback

from flask import Blueprint, request, current_app as app

from ..models.room import Room
from ..exts.redis_util import RedisUtil
from ..exts.enum import ErrCode, RedisKey
from ..exts.result import Ret

room = Blueprint('/room', __name__)

LOG_PATTERN = '[ROUTE:({0})] {1}'

@room.route('/')
def index():
    return Ret.success_msg("room test!")


@room.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    app.logger.info(LOG_PATTERN.format('/room/create', data))
    id = RedisUtil.incr(RedisKey.ROOM_INCREMENT_ID.value)
    password = Room.generate_password(data['password'])
    key = Room.generate_key(id, password)
    room = Room(id, data['name'], password, key, data['username'], '')
    RedisUtil.hmset(RedisKey.ROOM_ID_INFO.value.format(room.id), room.as_full_dict())

    return Ret.success_ret(room.as_dict())


@room.route('/get', methods=['POST'])
def get():
    data = request.get_json()
    app.logger.info(LOG_PATTERN.format('/room/get', data))
    room_info = RedisUtil.hgetall(RedisKey.ROOM_ID_INFO.value.format(data['id']))
    room = Room.parse(room_info)
    check = False
    if 'password' in data:
        check = room.check_password(data['password'])
    if 'key' in data:
        check = room.check_key(data['key'])
    if not check:
        return Ret.error_msg(ErrCode.AUTHENTICATION_FAILED.value, "权限校验失败!")
    return Ret.success_ret(room.as_dict())

