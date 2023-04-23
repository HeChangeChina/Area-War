from base import Base
from auxiliary_tools.flag_manager import FlagManager
from unit_tools.attribute_revise import AttributeRevise
from display.atlas import Atlas
from pygame import Rect


class Behavior(Base):
    def __init__(self):
        super().__init__()
        self.manager = None
        self.unit = None
        self.flag = FlagManager()
        self.flag.add_flag("behavior")
        self.last_frame = -1
        self.polarity = "None"
        self.attribute_revise = None

        # 以下属性仅影响视觉效果
        self.icon = "behavior"
        self.icon_visible = False
        self.describe = "未知的效果"
        self.name = "未知状态"

        self.surface = None
        self.animate_added = True
        self.animate_frame = 0
        self.animate_length = 0
        self.animate_flag = "defeat"
        self.animation = None
        self.fps_level = 0
        self.frame = 0
        self.shifting = (0, 0)
        self.rect = Rect(0, 0, 0, 0)
        self.atlas = dict()

    def add_animation(self, animation, flag, shifting=(0, 0)):
        self.animation = animation
        self.atlas = Atlas.load("./data/img/behaviors/" + animation, animation)["defeat"]
        self.animate_flag = flag
        self.animate_length = len(self.atlas)
        self.animate_frame = 0
        self.frame = 0
        self.shifting = shifting
        self.surface = self.atlas[0][0]
        self.rect = Rect(0, 0, 0, 0)
        self.animate_added = False

    def add_attribute_revise(self, attribute, value, flag):
        if self.attribute_revise is None and self.unit is not None:
            self.attribute_revise = AttributeRevise()
            self.unit.attribute_manager.attribute_revise_manager.add(self.attribute_revise)
        self.attribute_revise.add(attribute, value, flag)

    def set_attribute_revise(self, flag, value):
        self.attribute_revise.set(flag, value)

    def remove_attribute_revise(self, flag):
        self.attribute_revise.remove(flag)

    def add_level(self):
        pass

    def set_manager(self, manager):
        self.manager = manager
        self.unit = self.manager.unit
        self.start()

    def start(self):
        pass

    def hurt(self, value, hurt_type):
        pass

    def magic_use(self, value):
        pass

    def health_recovery(self, value):
        pass

    def magic_recovery(self, value):
        pass

    def base_update_60(self):
        if self.animate_added is False and self.unit is not None:
            self.animate_added = True
            left = (self.unit.c_rect.width - self.surface.get_width()) / 2 + self.shifting[0]
            top = (self.unit.c_rect.height - self.surface.get_height()) / 2 + self.shifting[1]
            self.rect = Rect(left, top, self.surface.get_width(), self.surface.get_height())
            self.unit.add_surface(self.surface, self.rect, self.animate_flag)

        if self.animate_length > 0:
            self.frame += 1
            frame_level = 1
            if self.fps_level == 0:
                frame_level = 10
            elif self.fps_level == 1:
                frame_level = 4
            if self.frame >= frame_level:
                self.frame = 0
                self.animate_frame += 1 if self.animate_frame + 1 < self.animate_length else -self.animate_frame
                self.surface = self.atlas[self.animate_frame][0]
                self.unit.replace_surface(self.surface, self.rect, self.animate_flag)

        if self.last_frame > 0:
            self.last_frame -= 1
            self.update_60()
        elif self.last_frame == 0:
            self.manager.remove_from_flag(self.flag.flag)
        else:
            self.update_60()

    def update_15(self):
        pass

    def update_60(self):
        pass

    def clear(self):
        super().clear()
        if self.attribute_revise is not None:
            self.attribute_revise.clear()
            self.attribute_revise = None
        if self.animate_length > 0:
            self.unit.remove_surface(self.animate_flag)
        self.unit = None
        self.manager = None
