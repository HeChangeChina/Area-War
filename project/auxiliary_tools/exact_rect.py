import pygame


class ERect:
    def __init__(self, left=0, top=0, width=0, height=0):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def load_rect(self, rect):
        self.left = rect.left
        self.top = rect.top
        self.width = rect.width
        self.height = rect.height

    def rect(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)
