from base import Base
from auxiliary_tools.message_manager import MessageManager


class IndicatorDrawer(Base):
    def __init__(self):
        super().__init__()
        self.now_indicator = []
        self.message_require("add_indicator", self.add_indicator)
        self.message_require("update_60", self.update)

    def add_indicator(self, indicator):
        for i in self.now_indicator:
            if indicator.flag.contain_flag(i, must_have_all=True):
                return
        self.now_indicator.append(indicator.flag.flag)

        MessageManager.send_message("add_display", indicator.get_effect())

    def update(self, data):
        self.now_indicator = []

    def clear(self):
        super().clear()
        self.now_indicator = []
