from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask import current_app as app
from ..exts.result import Ret
from ..exts.redis_util import RedisUtil
from ..exts.enum import ErrCode, RedisKey
from ..models.room import Room

LOG_PARAM_PATTERN = '[EVENT:({0})] PARAM: {1}'

AUTH_FAILED_RET = Ret.error_msg_dict(ErrCode.AUTHENTICATION_FAILED.value, "权限校验失败!")

def init_handlers(socketio: SocketIO):
    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected!')

    def get_room_by_id(room_id):
        room_info = RedisUtil.hgetall(RedisKey.ROOM_ID_INFO.value.format(room_id))
        room = Room.parse(room_info)
        return room

    def check_room_info(room, data):
        check = False
        if room is None:
            return check
        if 'password' in data:
            check = room.check_password(data['password'])
        if 'key' in data:
            check = room.check_key(data['key'])
        return check

    @socketio.on('join')
    def on_join(data):
        app.logger.info(LOG_PARAM_PATTERN.format('join', str(data)))
        room_id = data['id']
        room = get_room_by_id(room_id)
        if not check_room_info(room, data):
            emit('notice', AUTH_FAILED_RET)
        join_room(room_id)
        ret = Ret.success_msg_dict('欢迎{0}进入房间!'.format(data['username']))
        emit('notice', ret, to=room_id)

    @socketio.on('syncSource')
    def on_sync_source(data):
        app.logger.info(LOG_PARAM_PATTERN.format('syncSource', str(data)))
        room_id = data['id']
        room = get_room_by_id(room_id)
        if not check_room_info(room, data):
            emit('notice', AUTH_FAILED_RET)
        RedisUtil.hset(RedisKey.ROOM_ID_INFO.value.format(room_id), 'source', data['source'])
        emit('syncSource', Ret.success_ret_dict(data['source']), to=room_id)

    @socketio.on('syncPlay')
    def on_sync_play(data):
        app.logger.info(LOG_PARAM_PATTERN.format('syncPlay', str(data)))
        room_id = data['id']
        room = get_room_by_id(room_id)
        if not check_room_info(room, data):
            emit('notice', AUTH_FAILED_RET)
        emit('syncPlay', Ret.success_ret_dict(data['currTime']), to=room_id)

    @socketio.on('syncPause')
    def on_sync_pause(data):
        app.logger.info(LOG_PARAM_PATTERN.format('syncPause', str(data)))
        room_id = data['id']
        room = get_room_by_id(room_id)
        if not check_room_info(room, data):
            emit('notice', AUTH_FAILED_RET)
        emit('syncPause', Ret.success_ret_dict(data['currTime']), to=room_id)

    @socketio.on('echo')
    def on_echo(data):
        app.logger.info(LOG_PARAM_PATTERN.format('echo', str(data)))
        emit('echo', data, to=data['id'])
