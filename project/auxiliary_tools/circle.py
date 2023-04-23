import math


class Circle:
    def __init__(self, left, top, radius):
        self.left = left
        self.top = top
        self.radius = radius

    def load_from_rect(self, rect, radius):
        left = rect.left + rect.width / 2 - radius
        top = rect.top + rect.height / 2 - radius
        self.left = left
        self.top = top
        self.radius = radius

    def center(self):
        return [self.left + self.radius, self.top + self.radius]

    # 在计算与矩形的距离时，对于矩形角落附近的计算是不精确的，尤其当圆形比较大的时候
    def distance(self, c_object):
        if type(c_object) == type(self):
            center001 = self.center()
            center002 = c_object.center()
            return math.sqrt((center001[0] - center002[0]) ** 2 + (center001[1] - center002[1]) ** 2) - self.radius - \
                   c_object.radius
        else:
            center001 = self.center()
            left = c_object.left - self.radius
            top = c_object.top - self.radius
            width = c_object.width + self.radius * 2
            height = c_object.height + self.radius * 2
            if left + width > center001[0] > left and top + height > center001[1] > top:
                x_different = left + width - center001[0] if left + width - center001[0] > center001[0] - left else \
                    center001[0] - left
                y_different = top + height - center001[1] if top + height - center001[1] > center001[1] - top else \
                    center001[1] - top
                return -x_different if x_different > y_different else -y_different
            else:
                x_different = abs(left + width - center001[0]) if abs(left + width - center001[0]) > \
                                                                  abs(center001[0] - left) else abs(center001[0] - left)
                y_different = abs(top + height - center001[1]) if abs(top + height - center001[1]) > \
                                                                  abs(center001[1] - top) else abs(center001[1] - top)
                return x_different if x_different > y_different else y_different

    def x_distance(self, circle):
        return abs(self.center()[0] - circle.center()[0]) - self.radius - circle.radius

    def y_distance(self, circle):
        return abs(self.center()[1] - circle.center()[1]) - self.radius - circle.radius

    def center_distance(self, c_object):
        if type(c_object) == type(self):
            center001 = self.center()
            center002 = c_object.center()
            return math.sqrt((center001[0] - center002[0]) ** 2 + (center001[1] - center002[1]) ** 2)
        else:
            center001 = self.center()
            center002 = [c_object.left + c_object.width / 2, c_object.top + c_object.height / 2]
            return math.sqrt((center001[0] - center002[0]) ** 2 + (center001[1] - center002[1]) ** 2)

    def collide(self, c_object):
        return self.distance(c_object) < 0

    def collide_list(self, object_list):
        collide_list = []
        for i in range(len(object_list)):
            if self.collide(object_list[i]):
                collide_list.append(i)
        return collide_list
