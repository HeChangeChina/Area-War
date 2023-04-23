from base import Base
import os
import pygame


class Atlas(Base):
    atlas_dict = {}

    def __init__(self, path, unit_name):
        super().__init__()
        self.atlas_dict = Atlas.load(path, unit_name)

    @classmethod
    def load(cls, path, unit_name):
        if cls.atlas_dict.get(unit_name) is None:
            path = os.path.abspath(path)
            unit_name = unit_name
            l_dict = {}
            for root, dirs, files in os.walk(path):
                for file in files:
                    img_info = os.path.splitext(file)[0].split("_")
                    if img_info[0] == unit_name:
                        img = pygame.image.load(path + "/" + file).convert_alpha()
                        if l_dict.get(img_info[1]) is not None:
                            l_dict[img_info[1]].append([img, pygame.transform.flip(img, True, False)])
                        else:
                            l_dict[img_info[1]] = [[img, pygame.transform.flip(img, True, False)]]
            cls.atlas_dict[unit_name] = l_dict
            return l_dict
        else:
            return cls.atlas_dict[unit_name]
