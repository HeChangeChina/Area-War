import math


class Ballistic:
    @staticmethod
    def calculate(speed, now_c, target_c, bullet_width=25, start_point=(0, 0), start=False):
        distance = math.sqrt((now_c[0] - target_c[0])**2 + (now_c[1] - target_c[1])**2)
        if target_c[1] - now_c[1] != 0:
            angle = math.asin(-(target_c[1] - now_c[1]) / distance) if target_c[0] > now_c[0] else\
                math.asin((target_c[1] - now_c[1]) / distance) + math.pi
            move_y = speed * (target_c[1] - now_c[1]) / distance
        else:
            angle = math.pi if target_c[0] < now_c[0] else 0
            move_y = 0
        if target_c[0] - now_c[0] != 0:
            move_x = speed * (target_c[0] - now_c[0]) / distance
        else:
            move_x = 0

        result = dict()
        result["move"] = (move_x, move_y)
        result["arrive"] = distance - bullet_width < speed
        result["angle"] = angle / math.pi * 180
        return result
