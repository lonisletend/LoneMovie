from flask_socketio import SocketIO, emit, send, join_room, leave_room

def init_handlers(socketio: SocketIO):

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    @socketio.on('join')
    def on_join(data):
        print('[EVENT:join] param: {}'.format(str(data)))
        roomId = data['roomId']
        join_room(roomId)
        data['message'] = "我加入房间啦!!!"
        emit('join', data, to=roomId)

    @socketio.on('leave')
    def on_leave(data):
        print('[EVENT:leave] param: {}'.format(str(data)))
        roomId = data['roomId']
        leave_room(roomId)
        data['message'] = "我退出房间啦!!!"
        send('leave', to=roomId)

    @socketio.on('msg')
    def handle_msg(msgInfo):
        print('[EVENT:msg] param: {}'.format(str(msgInfo)))
        emit('msg', msgInfo, to=msgInfo['roomId'])

    @socketio.on('message')
    def handle_message(message):
        print('received message: ' + message)
        # emit('Test server response!', broadcast=True)
        send(message, broadcast=True)

    @socketio.on('syncTime')
    def handle_time_sync(time):
        print('received time: ' + time)
        emit('syncTime', time, broadcast=True)

    @socketio.on('syncPlay')
    def handle_sync_play(currTime):
        print('received play: ' + currTime)
        emit('syncPlay', currTime, broadcast=True)

    @socketio.on('syncPause')
    def handle_sync_pause(currTime):
        print('received pause: ' + currTime)
        emit('syncPause', currTime, broadcast=True)