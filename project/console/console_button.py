from base import Base
from display.font import StaticFontSurface
from display.font import FontSurface
from display.atlas import Atlas
import pygame


class ConsoleButton(Base):
    def __init__(self, c_xy, img_source="./data/img/skill_icon", img="skill", frame="DefeatFrame", corner=None,
                 text=None, size=(60, 60), corner_color=(230, 230, 200), text_shift=0):
        super().__init__()
        self.size = size
        self.c_rect = pygame.Rect(c_xy[0], c_xy[1], size[0], size[1])
        self.surface = pygame.Surface((size[0], size[1]))
        self.surface.set_colorkey((0, 0, 0))
        self.corner = corner
        self.corner_color = corner_color
        self.text_shift = text_shift
        self.change(img_source, img, frame, corner)

        self.mouse_on = False
        self.mouse_on_judge()
        self.if_mouse_down = pygame.mouse.get_pressed(3)[0]
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self.change_text(text)

    def move_to(self, x, y):
        self.c_rect = pygame.Rect(x, y, self.size[0], self.size[1])
        self.change_text(self.text)

    def change(self, img_source="./data/img/skill_icon", img="skill", frame="DefeatFrame", corner=None):
        self.surface.blit(Atlas.load(img_source, img)["defeat"][0][0], [0, 0])
        self.surface.blit(Atlas.load("./data/img/console", frame)["defeat"][0][0], [0, 0])
        self.corner = corner
        if corner is not None:
            corner_surface = FontSurface(corner, 13, self.corner_color).surface
            self.surface.blit(corner_surface, [6, -19 + self.size[1]])

    def change_surface(self, surface, frame="DefeatFrame"):
        self.surface.blit(surface, (0, 0))
        if frame is not None:
            self.surface.blit(Atlas.load("./data/img/console", frame)["defeat"][0][0], [0, 0])
        if self.corner is not None:
            corner_surface = FontSurface(self.corner, 13, self.corner_color).surface
            self.surface.blit(corner_surface, [6, -19 + self.size[1]])

    def change_text(self, text):
        self.text = text
        if text is not None:
            text_surface = StaticFontSurface.get(text, 16, color=(230, 230, 230))
            self.text_surface = pygame.Surface((160, text_surface.get_height() + 10))
            self.text_surface.fill((100, 100, 150))
            pygame.draw.rect(self.text_surface, (240, 210, 160), pygame.Rect(0, 0, 160, self.text_surface.get_height()), 3)
            self.text_surface.blit(text_surface, [7, 7])
            self.text_rect = pygame.Rect(self.c_rect.left - 50 + self.text_shift, self.c_rect.top - 10 -
                                         self.text_surface.get_height(), 160, self.text_surface.get_height())
        else:
            self.text_surface = pygame.Surface((0, 0))
            self.text_rect = pygame.Rect(0, 0, 0, 0)

    def get_surface(self):
        if self.text is not None and self.mouse_on:
            return [[self.surface, self.c_rect], [self.text_surface, self.text_rect]]
        else:
            return [[self.surface, self.c_rect]]

    def mouse_on_judge(self):
        mouse = pygame.mouse.get_pos()
        if self.c_rect.left + self.size[0] > mouse[0] > self.c_rect.left and \
                self.c_rect.top + self.size[1] > mouse[1] > self.c_rect.top:
            self.mouse_on = True
        else:
            self.mouse_on = False

    def update(self):
        self.mouse_on_judge()

        mouse_down = pygame.mouse.get_pressed(3)[0]
        if mouse_down and self.if_mouse_down is False and self.mouse_on:
            self.mouse_down()
        elif mouse_down is False and self.if_mouse_down and self.mouse_on:
            self.mouse_up()
        self.if_mouse_down = mouse_down

    def mouse_down(self):
        pass

    def mouse_up(self):
        pass
