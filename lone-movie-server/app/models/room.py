from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash


class Room:
    def __init__(self, id, name, password, key, owner, source):
        self.id = id
        self.name = name
        self.password = password
        self.key = key
        self.owner = owner
        self.source = source

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            key=self.key,
            owner=self.owner,
            source=self.source
        )

    def as_full_dict(self):
        room_dict = self.as_dict()
        room_dict['password'] = self.password
        return room_dict

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_key(self, key):
        return self.key == key

    @staticmethod
    def parse(info: dict):
        return Room(info['id'], info['name'], info.get('password', None), info.get('key', None), info['owner'], info['source'])

    @staticmethod
    def generate_password(password):
        return generate_password_hash(password)

    @staticmethod
    def generate_key(id, password):
        key = '{0}_{1}'.format(id, password)
        return md5(key.lower().encode('utf-8')).hexdigest()
