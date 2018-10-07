from imagerect import ImageRect
import pygame


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 10

    def __init__(self, screen, mazefile, brickfile, portalfile, shieldfile, pillfile, dotfile):
        self.screen = screen
        self.filename = mazefile

        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.bricks = []
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.deltax = self.deltay = Maze.BRICK_SIZE

        self.build()

    def build(self):
        r = self.brick.rect
        w, h = r.width, r.height
        dx, dy, = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'X':
                    self.bricks.append(pygame.Rect(ncol*dx, nrow*dy, w, h))

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
