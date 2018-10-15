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

    def __init__(self, screen, mazefile, brickfile, portalfile, shieldfile, pillfile):
        self.screen = screen
        self.filename = mazefile

        with open(self.filename, 'r') as f:
            self.rows = f.read().splitlines()


        self.lwalls = []
        self.rwalls = []
        self.twalls = []
        self.bwalls = []
        self.gwalls = []
        self.mwalls = []
        self.nwalls = []
        self.owalls = []
        self.ywalls = []
        self.zwalls = []
        self.wwalls = []
        self.xwalls = []
        self.dots = Group()
        self.pills = Group()
        sz = Maze.BRICK_SIZE
        self.lwall = ImageRect(screen, "left_wall", sz, sz)
        self.rwall = ImageRect(screen, "right_wall", sz, sz)
        self.twall = ImageRect(screen, "top_wall", sz, sz)
        self.bwall = ImageRect(screen, "bottom_wall", sz, sz)
        self.gwall = ImageRect(screen, "top_right_in", sz, sz)
        self.mwall = ImageRect(screen, "top_left_in", sz, sz)
        self.nwall = ImageRect(screen, "bottom_right_in", sz, sz)
        self.owall = ImageRect(screen, "bottom_left_in", sz, sz)
        self.ywall = ImageRect(screen, "top_left_out", sz, sz)
        self.zwall = ImageRect(screen, "top_right_out", sz, sz)
        self.wwall = ImageRect(screen, "bottom_left_out", sz, sz)
        self.xwall = ImageRect(screen, "bottom_right_out", sz, sz)

        #self.blinky = Ghost('b', self.lwall.rect, self.p_man, self.screen, self)
        self.deltax = self.deltay = Maze.BRICK_SIZE
        self.intersections = []

        self.build()

    def build(self,):
        r = self.lwall.rect
        w, h = r.width, r.height
        dx, dy, = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'L':
                    self.lwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'R':
                    self.rwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'T':
                    self.twalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'B':
                    self.bwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'G':
                    self.gwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'M':
                    self.mwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'N':
                    self.nwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'O':
                    self.owalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'Y':
                    self.ywalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'Z':
                    self.zwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'W':
                    self.wwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'X':
                    self.xwalls.append(pygame.Rect(ncol*dx, nrow*dy, w, h))
                elif col == 'd':
                    self.dots.add(Dot(self.screen, pygame.Rect(ncol*dx, nrow*dy, 10, 10)))

                elif col == '+':
                    self.pills.add(Pill(self.screen, pygame.Rect(ncol*dx, nrow*dy, 10, 10)))

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
        for rect in self.twalls:
            self.screen.blit(self.twall.image, rect)
        for rect in self.bwalls:
            self.screen.blit(self.bwall.image, rect)
        for rect in self.rwalls:
            self.screen.blit(self.rwall.image, rect)
        for rect in self.lwalls:
            self.screen.blit(self.lwall.image, rect)
        for rect in self.gwalls:
            self.screen.blit(self.gwall.image, rect)
        for rect in self.mwalls:
            self.screen.blit(self.mwall.image, rect)
        for rect in self.nwalls:
            self.screen.blit(self.nwall.image, rect)
        for rect in self.owalls:
            self.screen.blit(self.owall.image, rect)
        for rect in self.ywalls:
            self.screen.blit(self.ywall.image, rect)
        for rect in self.zwalls:
            self.screen.blit(self.zwall.image, rect)
        for rect in self.wwalls:
            self.screen.blit(self.wwall.image, rect)
        for rect in self.xwalls:
            self.screen.blit(self.xwall.image, rect)
        self.dots.update()


        self.pills.update()
