from base import Base


class Effect(Base):
    def __init__(self, **data):
        super().__init__()
        self.data = data

    def take_effect(self, target, trigger):
        self.effect(target, trigger)

    def effect(self, target, trigger):
        pass
