from auxiliary_tools.ballistic import Ballistic
import math


class UpperParabola(Ballistic):
    def __init__(self, upper_y):
        self.upper_y = upper_y

    @staticmethod
    def calculate_det(a11, a12, a13, a21, a22, a23, a31, a32, a33):
        return a11 * a22 * a33 + a12 * a23 * a31 + a21 * a32 * a13 - a11 * a23 * a32 - a12 * a21 * a33 - a13 * a22 * a31

    @staticmethod
    def calculate_abc(point001, point002, point003):
        a1 = point001[0] ** 2
        a2 = point002[0] ** 2
        a3 = point003[0] ** 2
        b1 = point001[0]
        b2 = point002[0]
        b3 = point003[0]
        c1 = c2 = c3 = 1
        d1 = point001[1]
        d2 = point002[1]
        d3 = point003[1]

        delta = __class__.calculate_det(a1, b1, c1, a2, b2, c2, a3, b3, c3)
        delta_a = __class__.calculate_det(d1, b1, c1, d2, b2, c2, d3, b3, c3)
        delta_b = __class__.calculate_det(a1, d1, c1, a2, d2, c2, a3, d3, c3)
        delta_c = __class__.calculate_det(a1, b1, d1, a2, b2, d2, a3, b3, d3)

        a = delta_a / delta
        b = delta_b / delta
        c = delta_c / delta

        return a, b, c

    def calculate(self, speed, now_c, target_c, bullet_width=25, start_point=(0, 0), start=False):
        point1 = start_point
        point2 = target_c
        point3 = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2 - self.upper_y]

        abc = self.calculate_abc(point1, point2, point3)
        a = abc[0]
        b = abc[1]
        c = abc[2]

        dy = 2 * a * start_point[0] + b
        x_d = math.cos(math.atan(dy)) * speed if now_c[0] < target_c[0] else -math.cos(math.atan(dy)) * speed

        dy2 = 2 * a * now_c[0] + b

        x = target_c[0] if now_c[0] < target_c[0] < now_c[0] + x_d or now_c[0] > target_c[0] > now_c[0] + x_d else now_c[0] + x_d
        y = a * x**2 + b * x + c

        distance = ((x - target_c[0])**2 + (y - target_c[1])**2)**0.5 - bullet_width

        result = dict()
        result["move"] = (x - now_c[0], y - now_c[1])
        result["arrive"] = distance < x_d
        result["angle"] = math.atan(dy2) / math.pi * 180
        if now_c[0] > target_c[0]:
            result["angle"] += 180
        return result
