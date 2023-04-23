from auxiliary_tools.ballistic import Ballistic


class Fall(Ballistic):
    def __init__(self, width=200):
        self.width = width
        super().__init__()

    def calculate(self, speed, now_c, target_c, bullet_width=25, start_point=(0, 0), start=False):
        move_x = - now_c[0] + target_c[0]
        move_y = speed if start is False else -400 - now_c[1]

        result = dict()
        result["move"] = (move_x, move_y)
        result["arrive"] = abs(now_c[1] + self.width - target_c[1]) < speed
        result["angle"] = 0
        return result
