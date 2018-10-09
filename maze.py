from imagerect import ImageRect
import pygame
from pygame.sprite import Group
from dot import Dot, Pill
from pac_man import PacMan
from ghost import Ghost


class Intersection:
    def __init__(self, up, down, left, right, rect):
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.rect = rect


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 10

    def __init__(self, screen, mazefile, brickfile, portalfile, shieldfile, pillfile, p_man):
        self.screen = screen
        self.filename = mazefile

        with open(self.filename, 'r') as f:
            self.rows = f.read().splitlines()
        self.p_man = p_man

        self.bricks = []
        self.dots = Group()
        self.pills = Group()
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.blinky = Ghost('b', self.brick.rect, self.p_man, self.screen, self)
        self.deltax = self.deltay = Maze.BRICK_SIZE
        self.intersections = []

        self.build()

    def build(self,):
        r = self.brick.rect
        w, h = r.width, r.height
        dx, dy, = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'X':
                    self.bricks.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'd':
                    self.dots.add(Dot(self.screen, pygame.Rect(ncol*dx, nrow*dy, 10, 10)))
                elif col == 'P':
                    self.p_man.im.rect = pygame.Rect(ncol*dx, nrow*dy-7, 25, 25)
                elif col == '+':
                    self.pills.add(Pill(self.screen, pygame.Rect(ncol*dx, nrow*dy, 10, 10)))
                elif col == 'b':
                    self.blinky = Ghost('b', pygame.Rect(ncol*dx, nrow*dy-7, 25, 25), self.p_man, self.screen,
                                        self)
                elif col == '1':
                    self.intersections.append(Intersection(True, True, True, True,
                                                           (pygame.Rect(ncol*dx, nrow*dy, w, h))))
                elif col == '2':
                    self.intersections.append(Intersection(False, True, True, True,
                                                           (pygame.Rect(ncol * dx, nrow * dy, w, h))))
                elif col == '3':
                    self.intersections.append(Intersection(True, False, True, True,
                                                           (pygame.Rect(ncol * dx, nrow * dy, w, h))))
                elif col == '4':
                    self.intersections.append(Intersection(True, True, False, True,
                                                           (pygame.Rect(ncol * dx, nrow * dy, w, h))))
                elif col == '5':
                    self.intersections.append(Intersection(True, True, True, False,
                                                           (pygame.Rect(ncol * dx, nrow * dy, w, h))))
                elif col == '6':
                    self.intersections.append(Intersection(False, False, True, True,
                                                           (pygame.Rect(ncol * dx, nrow * dy, w, h))))

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        self.dots.update()
        self.blinky.update()
        self.p_man.blitme()
        self.pills.update()
