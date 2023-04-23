from unit_tools.sight import Sight
from pygame.transform import rotate
from pygame.rect import Rect
from auxiliary_tools.circle import Circle
from auxiliary_tools.message_manager import MessageManager


class FollowSight(Sight):
    def __init__(self, atlas, rotation_speed=0, coll="circle", coll_range=50):
        super().__init__(atlas)
        self.rotation_speed = rotation_speed
        self.rotation = 0
        self.coll_type = coll
        self.coll_range = coll_range
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

    def start_draw(self):
        self.c_rect.width = self.atlas["defeat"][0][0].get_width()
        self.c_rect.height = self.atlas["defeat"][0][0].get_height()

    def end_draw(self):
        self.visible = False
        for i in self.range_unit:
            i.shader.remove_blend_color("sight_chosen")
        self.range_unit = list()

    def draw(self, target):
        if type(target) is not tuple and type(target) is not list:
            self.visible = True
            self.rotation += self.rotation_speed
            self.surface = self.atlas["defeat"][0][0] if self.rotation == 0 else \
                rotate(self.atlas["defeat"][0][0], self.rotation)
            left = target.c_rect.left + target.c_rect.width / 2
            top = target.c_rect.top + target.c_rect.height / 2
            self.c_rect.left = left - self.surface.get_width() / 2
            self.c_rect.top = top - self.surface.get_height() / 2
            coll = None
            if self.coll_type == "circle":
                coll = Circle(left - self.c_rect.width / 2 - self.coll_range, top - self.c_rect.height / 2, self.coll_range)
            elif self.coll_type == "range":
                coll = Rect(left - self.coll_range, 0, self.coll_range * 2, 1080)
            if coll is not None:
                MessageManager.send_message("search_range", (coll, self))
        else:
            self.receive_unit_list(list())
            self.visible = False
