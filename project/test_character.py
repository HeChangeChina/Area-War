import base


class TestCharacter(base.Base):
    def __init__(self):
        super().__init__()
        self.add_flag(["1","2","3","4"])
        self.add_flag("6")
        self.remove_flag(["1","2"])
        self.remove_flag("4")
        print(self.flag)
        self.start_update()

    def update(self):
        print("Receive Message")
