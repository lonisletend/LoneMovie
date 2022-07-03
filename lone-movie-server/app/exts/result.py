from flask import jsonify


class Ret:
    status = True
    code = 0
    msg = ''
    data = None

    def __init__(self, status, code, msg, data):
        self.status = status
        self.code = code
        self.msg = msg
        self.data = data

    def serialize(self):
        return jsonify({
            'status': self.status,
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        })

    def as_dict(self):
        return dict(
            status=self.status,
            code=self.code,
            msg=self.msg,
            data=self.data
        )

    @staticmethod
    def success_ret(data=None):
        ret = Ret(True, 0, '', data)
        return ret.serialize()

    @staticmethod
    def success_msg(msg):
        ret = Ret(True, 0, msg, None)
        return ret.serialize()

    @staticmethod
    def success_msg_dict(msg):
        ret = Ret(True, 0, msg, None)
        return ret.as_dict()

    @staticmethod
    def error_ret(code=1, data=None, msg="error"):
        ret = Ret(False, code, msg, data)
        return ret.serialize()

    @staticmethod
    def error_msg(code=1, msg="error"):
        ret = Ret(False, code, msg, None)
        return ret.serialize()

    @staticmethod
    def error_msg_dict(code=1, msg="error"):
        ret = Ret(False, code, msg, None)
        return ret.as_dict()