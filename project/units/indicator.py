from base import Base
from auxiliary_tools.flag_manager import FlagManager


class Indicator(Base):
    def __init__(self):
        super().__init__()
        self.flag = FlagManager()

    def get_effect(self):
        pass
