from pygame.sprite import Sprite
from imagerect import ImageRect


class Dot(Sprite):

    def __init__(self, screen, rect):
        super(Dot, self).__init__()
        self.im = ImageRect(screen, "dot", 10, 10)
        self.screen = screen
        self.im.rect = rect
        self.rect = self.im.rect

    def update(self):
        self.im.blitme()


class Pill(Sprite):
    def __init__(self, screen, rect):
        super(Pill, self).__init__()
        self.im = ImageRect(screen, "pill", 10, 10)
        self.screen = screen
        self.im.rect = rect
        self.rect = self.im.rect

    def update(self):
        self.im.blitme()
