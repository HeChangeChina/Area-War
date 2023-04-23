from base import Base


class KeyListener(Base):
    keys = list()

    def __init__(self):
        super().__init__()
        self.message_require("key_down", self.key_down)
        self.message_require("key_up", self.key_up)

    @staticmethod
    def key_down(data):
        __class__.keys.append(data[0])

    @staticmethod
    def key_up(data):
        __class__.keys.remove(data[0])

    @classmethod
    def get_key(cls, key):
        return key in cls.keys
