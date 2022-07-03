from enum import Enum


class UserGroup(Enum):
    ADMIN = 0
    NORMAL = 1


class ErrCode(Enum):
    INVALID_ARGUMENTS = 1001
    RESOURCES_NOT_EXIST = 1002
    RESOURCES_UNIQUE_EXIST = 1003
    AUTHENTICATION_FAILED = 1004
    ILLEGAL_REQUEST = 1005
    REQUEST_TOO_FREQUENTLY = 1006

    BIZ_EXCEPTION = 1100


class ConfigType(Enum):
    STRING = 0
    NUMBER = 1
    JSON = 2


class RedisKey(Enum):
    ROOM_INCREMENT_ID = 'lonemovie:room:increment_id'
    ROOM_ID_INFO = 'lonemovie:room:id:{0}'


class RedisExpire(Enum):
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800


class LimitCount(Enum):
    CAPTCHA_IP_REQUEST_DAY_LIMIT = 10
    CAPTCHA_EMAIL_REQUEST_DAY_LIMIT = 3
    CAPTCHA_EMAIL_INVALID_DAY_LIMIT = 10
