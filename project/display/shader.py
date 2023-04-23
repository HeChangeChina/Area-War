import pygame
from base import Base


class Shader(Base):
    def __init__(self):
        super().__init__()
        self.img = None
        self.surface = pygame.Surface((0, 0))
        self.op_surface = self.surface
        self.blend_color = dict()
        self.flash_time = 0
        self.alpha = 255

        self.width = 1
        self.height = 1

        self.c_width = 0
        self.c_height = 0

    def flash(self):
        self.flash_time = 2
        self.update_surface()

    def set_surface(self, surface):
        self.surface = surface
        self.c_width = surface.get_width()
        self.c_height = surface.get_height()
        self.update_surface()

    def get_surface(self):
        return self.op_surface

    def set_blend_color(self, color, flag="defeat"):
        already_have = self.blend_color.get(flag) is not None
        self.blend_color[flag] = color
        if not already_have:
            self.update_surface()

    def remove_blend_color(self, flag="defeat"):
        if self.blend_color.get(flag) is not None:
            self.blend_color.pop(flag)

    def get_blend_color(self):
        blend_color = [0, 0, 0]
        for i in self.blend_color:
            blend_color[0] += self.blend_color[i][0]
            blend_color[1] += self.blend_color[i][1]
            blend_color[2] += self.blend_color[i][2]
        if len(self.blend_color) > 0:
            blend_color[0] /= len(self.blend_color)
            blend_color[1] /= len(self.blend_color)
            blend_color[2] /= len(self.blend_color)
            blend_color[0] = int(blend_color[0])
            blend_color[1] = int(blend_color[1])
            blend_color[2] = int(blend_color[2])
            return tuple(blend_color)
        else:
            return (255, 255, 255)

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.update_surface()

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.update_surface()

    def update_surface(self):
        blend_color = self.get_blend_color()
        if self.flash_time > 0:
            self.flash_time -= 1
            self.op_surface = self.surface.copy()
            self.op_surface.fill((155, 0, 0), special_flags=pygame.BLENDMODE_BLEND)
        elif blend_color != (255, 255, 255):
            self.op_surface = self.surface.copy()
            self.op_surface.fill(blend_color, special_flags=pygame.BLEND_RGB_MULT)
        else:
            self.op_surface = self.surface

        if self.alpha != self.op_surface.get_alpha():
            self.op_surface.set_alpha(self.alpha)

        if self.width != 1 or self.height != 1:
            self.op_surface = pygame.transform.scale(self.op_surface, (int(self.c_width * self.width), int(self.c_height * self.height)))
