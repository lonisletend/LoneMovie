class IllegalArgumentError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SimpleError(Exception):
    def __init__(self, message="Simple Error!"):
        super().__init__(message)


class ObjectNotFoundError(SimpleError):
    def __init__(self, message="Object not found!"):
        super().__init__(message)


class ObjectStatusError(SimpleError):
    def __init__(self, message="Object status error!"):
        super().__init__(message)


class RollbackError(Exception):
    def __init__(self, message="Rollback Error!"):
        super().__init__(message)


class DbOptionError(RollbackError):
    def __init__(self, message="DbOption Error!"):
        super().__init__(message)


class RedisOptException(Exception):
    def __init__(self, message="Redis Operation Error!"):
        super().__init__(message)
