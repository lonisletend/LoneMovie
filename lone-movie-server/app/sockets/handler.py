from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask import current_app as app
from ..exts.result import Ret
from ..exts.redis_util import RedisUtil
from ..exts.enum import ErrCode, RedisKey
from ..models.room import Room

LOG_PARAM_PATTERN = '[EVENT:({0})] PARAM: {1}'


def init_handlers(socketio: SocketIO):
    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected!')

    @socketio.on('join')
    def on_join(data):
        app.logger.info(LOG_PARAM_PATTERN.format('join', str(data)))
        roomId = data['id']
        room_info = RedisUtil.hgetall(RedisKey.ROOM_ID_INFO.value.format(roomId))
        room = Room.parse(room_info)
        check = False
        if 'password' in data:
            check = room.check_password(data['password'])
        if 'key' in data:
            check = room.check_key(data['key'])
        if not check:
            ret = Ret.error_msg_dict(ErrCode.AUTHENTICATION_FAILED.value, "权限校验失败!")
            emit('notice', ret)
        else:
            join_room(roomId)
            ret = Ret.success_msg_dict('欢迎{0}进入房间!'.format(data['username']))
            emit('notice', ret, to=roomId)

    @socketio.on('echo')
    def on_echo(data):
        app.logger.info(LOG_PARAM_PATTERN.format('echo', str(data)))
        emit('echo', data, to=data['id'])
