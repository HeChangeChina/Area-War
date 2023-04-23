from display.normal_display import DisplayObject
from display.atlas import Atlas
from pygame.surface import Surface
from pygame.rect import Rect


class Sight(DisplayObject):
    def __init__(self, atlas=None, atlas_src="./data/img/sight"):
        self.atlas = Atlas.load(atlas_src, atlas) if atlas is not None else dict()
        self.surface = Surface((0, 0))
        self.c_rect = Rect(0, 0, 0, 0)
        self.show_mode = 0
        super().__init__()

    def start_draw(self):
        pass

    def end_draw(self):
        pass

    def get_surface(self):
        return [[self.surface, self.c_rect]]

    def draw(self, target):
        pass
