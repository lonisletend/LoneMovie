from .base import redis_client
from .error import RedisOptException


def decode(b):
    return b.decode("utf-8")

def decode_redis(src):
    if isinstance(src, list):
        rv = []
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = {}
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " + type(src))


class RedisUtil:
    @staticmethod
    def get(key):
        ret = redis_client.get(key)
        return decode(ret) if ret is not None else None

    @staticmethod
    def set(key, value):
        ret = redis_client.set(key, value)
        if not ret:
            raise RedisOptException("Redis set failed!")

    @staticmethod
    def set_with_expire(key, value, expire):
        ret = redis_client.set(key, value, expire)
        if not ret:
            raise RedisOptException("Redis set with expire failed!")

    @staticmethod
    def incr(key):
        return redis_client.incr(key)

    @staticmethod
    def expire(key, times):
        ret = redis_client.expire(key, times)
        if ret != 1:
            raise RedisOptException("Redis expire failed!")

    @staticmethod
    def validate_incr_max_with_expire(key, expire, max_count):
        count = RedisUtil.incr(key)
        if count == 1:
            RedisUtil.expire(key, expire)
        return count <= max_count

    @staticmethod
    def hmset(key, value):
        ret = redis_client.hmset(key, value)
        if not ret:
            raise RedisOptException("Redis hmset failed!")

    @staticmethod
    def hset(key, field, value):
        ret = redis_client.hset(key, field, value)

    @staticmethod
    def hmset_with_expire(key, value, expire):
        RedisUtil.hmset(key, value)
        RedisUtil.expire(key, expire)

    @staticmethod
    def hgetall(key):
        ret = redis_client.hgetall(key)
        return decode_redis(ret) if ret is not None else {}
