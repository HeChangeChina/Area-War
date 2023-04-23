from unit_tools.sight import Sight
from auxiliary_tools.message_manager import MessageManager
from pygame import Rect


class RangeSight(Sight):
    def __init__(self, r):
        self.R = r
        self.range_unit = list()
        super().__init__()

    def end_draw(self):
        self.visible = False
        for i in self.range_unit:
            i.shader.remove_blend_color("sight_chosen")
        self.range_unit = list()

    def receive_unit_list(self, unit):
        new_unit = list()
        for i in unit:
            if i not in self.range_unit:
                i.shader.set_blend_color((180, 180, 255), flag="sight_chosen")
                new_unit.append(i)
        for i in self.range_unit:
            if i not in unit:
                i.shader.remove_blend_color("sight_chosen")
                self.range_unit.remove(i)
        for i in new_unit:
            self.range_unit.append(i)

    def draw(self, target):
        center_x = target[0] if type(target) is list or type(target) is tuple else \
            target.c_rect.left + target.c_rect.width / 2

        coll = Rect(center_x - self.R, 0, self.R * 2, 1080)
        MessageManager.send_message("search_range", (coll, self))
        MessageManager.send_message("ellipse_draw", [center_x, self.R, (60, 60, 255), 2, 5])
