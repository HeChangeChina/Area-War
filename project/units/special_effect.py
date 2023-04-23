from display.normal_display import NormalDisplay
import pygame


class SpecialEffect(NormalDisplay):
    def __init__(self, effect_name, size, follow=False, fps_level=0, auto_clear=True, path=None, index=11,
                 blend_color=None):
        self.follow = follow
        self.follow_obj = None
        self.auto_clear = auto_clear
        self.index = index
        c_rect = pygame.Rect(0, 0, size[0], size[1])
        path = path if path is not None else "./data/img/effect/"
        super().__init__(path + effect_name, effect_name, c_rect, fps_level=fps_level)

        if blend_color is not None:
            self.shader.set_blend_color(blend_color)

        if self.auto_clear:
            self.animate_controler.play_action("defeat", end_recall=self.clear, lock=True)
        else:
            self.animate_controler.change_loop_action("defeat")
        self.update()

    def set_follow_obj(self, obj):
        self.follow_obj = obj
        if type(obj) is not tuple and type(obj) is not list:
            center_x = self.follow_obj.c_rect.left + self.follow_obj.c_rect.width / 2
            center_y = self.follow_obj.c_rect.top + self.follow_obj.c_rect.height / 2
            self.c_rect.left = center_x - self.c_rect.width / 2
            self.c_rect.top = center_y - self.c_rect.height / 2
        else:
            center_x = obj[0]
            center_y = obj[1]
            self.c_rect.left = center_x - self.c_rect.width / 2
            self.c_rect.top = center_y - self.c_rect.height / 2

    def update(self):
        if self.follow and self.follow_obj is not None:
            center_x = self.follow_obj.c_rect.left + self.follow_obj.c_rect.width / 2
            center_y = self.follow_obj.c_rect.top + self.follow_obj.c_rect.height / 2
            self.c_rect.left = center_x - self.c_rect.width / 2
            self.c_rect.top = center_y - self.c_rect.height / 2

    def clear(self):
        super().clear()
        self.follow_obj = None
