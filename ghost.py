from imagerect import ImageRect
from pygame.sprite import Sprite
import pygame
from vector import Vec2d


class Ghost(Sprite):

    def __init__(self, ghost_type, p_man, screen, maze, row, col, blinky = None):
        super(Ghost, self).__init__()
        self.type = ghost_type
        self.p_man = p_man
        self.maze = maze
        self.row = row
        self.col = col



        self.blinky_lvl = 0

        self.blinky = blinky
        if self.type == 'b':
            self.filename = "g_red_"
            self.targetcol = self.p_man.col
            self.targetrow = self.p_man.row
            self.scattercol = 26
            self.scatterrow = 0
            self.nextrow = self.row
            self.nextcol = self.col - 1
            self.awake = True
        elif self.type == 'p':
            self.filename = "g_pink_"
            self.targetcol = self.p_man.col + 4
            self.targetrow = self.p_man.row
            self.scattercol = 0
            self.scatterrow = 0
            self.nextrow = self.row
            self.nextcol = self.col - 1
            self.awake = False
        elif self.type == 'i':
            self.filename = 'g_teal_'
            self.targetcol = 26
            self.targetrow = 30
            self.scattercol = 26
            self.scatterrow = 30
            self.nextrow = self.row
            self.nextcol = self.col - 1
            self.awake = False
        elif self.type == 'c':
            self.filename = 'g_orng_'
            self.targetcol = 0
            self.targetrow = 30
            self.scattercol = 0
            self.scatterrow = 30
            self.nextrow = self.row
            self.nextcol = self.col - 1
            self.awake = False

        self.screen = screen
        self.target = None
        self.speed = 200
        self.leave = 0

        self.state = 1
        self.dir = 'left'
        self.nextdir = 'left'
        self.im = ImageRect(self.screen, self.filename+self.dir+'_'+str(self.state), 18, 18)

        self.im.rect.centerx = col * 10 + 5
        self.im.rect.centery = row * 10 + 5
        self.rect = self.im.rect
        self.walls = ['T', 'B', 'R', 'L', 'G', 'M', 'N', 'O', 'Y', 'Z', 'W', 'X', 'S']
        self.timer = pygame.time.get_ticks()
        self.frightened = False

    def update(self, move):
        if not self.awake:
            if self.type == 'p':
                if pygame.time.get_ticks() > 2500:
                    self.leave_house()
            elif self.type == 'i':
                if len(self.maze.dots.sprites()) <= 202:
                    self.leave_house()
            elif self.type == 'c':
                if len(self.maze.dots.sprites()) <= 154:
                    self.leave_house()

        if pygame.time.get_ticks() - self.timer >= self.speed and self.awake:
            if move:
                self.col = self.nextcol
                self.row = self.nextrow
                self.dir = self.nextdir
            next_space = {}
            if self.dir == 'up':
                next_space = {'row': self.row - 1, 'col': self.col}
            elif self.dir == 'left':
                next_space = {'row': self.row, 'col': self.col - 1}
            elif self.dir == 'down':
                next_space = {'row': self.row + 1, 'col': self.col}
            elif self.dir == 'right':
                next_space = {'row': self.row, 'col': self.col + 1}

            adj_spaces = [{'row': next_space['row'] - 1, 'col': next_space['col'], 'dir': 'up'},
                          {'row': next_space['row'], 'col': next_space['col'] - 1, 'dir': 'left'},
                          {'row': next_space['row'] + 1, 'col': next_space['col'], 'dir': 'down'},
                          {'row': next_space['row'], 'col': next_space['col'] + 1, 'dir': 'right'}]
            behind = ''
            options = []
            if self.dir == 'left':
                behind = 'right'
            elif self.dir == 'right':
                behind = 'left'
            elif self.dir == 'up':
                behind = 'down'
            elif self.dir == 'down':
                behind = 'up'

            for space in adj_spaces:
                if space['dir'] == behind:
                    continue
                temp = self.maze.rows[space['row']]
                val = temp[space['col']]
                if val not in self.walls:
                    options.append(space)
                if len(options) > 1:
                    self.update_target()

                target = Vec2d(self.targetcol, self.targetrow)
                min_distance = 28*36
                for o in options:
                    opt_vec = Vec2d(o['col'], o['row'])
                    o['dist'] = opt_vec.get_distance(Vec2d(target))
                    if o['dist'] < min_distance:
                        self.nextdir = o['dir']
                        min_distance = o['dist']
                self.nextrow = next_space['row']
                self.nextcol = next_space['col']
                if self.state == 1:
                    self.state = 2
                elif self.state == 2:
                    self.state = 1
                self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                self.im.rect.centerx = self.col * 10 + 5
                self.im.rect.centery = self.row * 10 + 5
                self.rect = self.im.rect

            self.timer = pygame.time.get_ticks()

            self.im.blitme()

    def find_target(self):
        if self.type == 'b':
            self.targetrow = self.p_man.row
            self.targetcol = self.p_man.col
            if len(self.maze.dots.sprites()) < 131 >= 65 and self.blinky_lvl == 0:
                self.speed *= 1.05
                self.blinky_lvl = 1
            elif len(self.maze.dots.sprites()) < 65 and self.blinky_lvl == 1:
                self.speed *= 1.05
                self.blinky_lvl = 2
        elif self.type == 'p':
            if self.p_man.dir == 'up':
                self.targetrow = self.p_man.row - 4
                self.targetcol = self.p_man.col - 4
            elif self.p_man.dir == 'down':
                self.targetrow = self.p_man.row + 4
                self.targetcol = self.p_man.col
            elif self.p_man.dir == 'left':
                self.targetcol = self.p_man.col - 4
                self.targetrow = self.p_man.row
            elif self.p_man.dir == 'right':
                self.targetcol = self.p_man.col + 4
                self.targetrow = self.p_man.row
            print(str(self.targetcol) + ' ' + str(self.targetrow))
        elif self.type == 'i':
            p_vec = Vec2d(self.p_man.col, self.p_man.row)
            if self.p_man.dir == 'up':
                p_vec.x -= 2
                p_vec.y -= 2
            elif self.p_man.dir == 'down':
                p_vec += 2
            elif self.p_man.dir == 'right':
                p_vec.x += 2
            elif self.p_man.dir == 'left':
                p_vec.x -= 2
            b_vec = Vec2d(self.blinky.col, self.blinky.row)

            col_vec = p_vec - b_vec
            col_vec *= 2
            r_vec = b_vec + col_vec
            self.targetcol = r_vec.x
            self.targetrow = r_vec.y
        elif self.type == 'c':
            p_vec = Vec2d(self.p_man.col, self.p_man.row)
            c_vec = Vec2d(self.col, self.row)

            dist = c_vec.get_distance(p_vec)

            if dist > 8:
                self.targetrow = self.p_man.row
                self.targetcol = self.p_man.col
            else:
                self.targetcol = 0
                self.targetrow = 30

    def update_target(self):
        if self.frightened:
            self.targetrow = self.scatterrow
            self.targetcol = self.scattercol
        elif pygame.time.get_ticks() < 7000:
            self.targetrow = self.scatterrow
            self.targetcol = self.scattercol
        elif pygame.time.get_ticks() <= 27000:
            self.find_target()
        elif pygame.time.get_ticks() <= 34000:
            self.targetrow = self.scatterrow
            self.targetcol = self.scattercol
        elif pygame.time.get_ticks() <= 54000:
            self.find_target()
        elif pygame.time.get_ticks() <= 59000:
            self.targetrow = self.scatterrow
            self.targetcol = self.scattercol
        elif pygame.time.get_ticks() <= 79000:
            self.find_target()
        elif pygame.time.get_ticks() <= 84000:
            self.targetrow = self.scatterrow
            self.targetcol = self.scattercol

        else:
            self.find_target()

    def leave_house(self):
        if self.type == 'p':
            if self.leave < 3:
                if pygame.time.get_ticks() - self.timer >= self.speed:
                    self.row -= 1
                    self.leave += 1
                    self.timer = pygame.time.get_ticks()
                    self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                    self.im.rect.centerx = self.col * 10 + 5
                    self.im.rect.centery = self.row * 10 + 5
                    self.rect = self.im.rect
            else:
                self.awake = True
                self.nextrow = self.row
                self.nextcol = self.col - 1
        if self.type == 'i':
            if pygame.time.get_ticks() - self.timer >= self.speed:
                if self.leave < 2:
                    self.col += 1
                    self.leave += 1
                    self.timer = pygame.time.get_ticks()
                    self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                    self.im.rect.centerx = self.col * 10 + 5
                    self.im.rect.centery = self.row * 10 + 5
                    self.rect = self.im.rect
                elif self.leave <= 4:
                    self.row -= 1
                    self.leave += 1
                    self.timer = pygame.time.get_ticks()
                    self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                    self.im.rect.centerx = self.col * 10 + 5
                    self.im.rect.centery = self.row * 10 + 5
                    self.rect = self.im.rect
                else:
                    self.awake = True
                    self.nextrow = self.row
                    self.nextcol = self.col - 1
        if self.type == 'c':
            if pygame.time.get_ticks() - self.timer >= self.speed:
                if self.leave < 2:
                    self.col -= 1
                    self.leave += 1
                    self.timer = pygame.time.get_ticks()
                    self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                    self.im.rect.centerx = self.col * 10 + 5
                    self.im.rect.centery = self.row * 10 + 5
                    self.rect = self.im.rect
                elif self.leave <= 4:
                    self.row -= 1
                    self.leave += 1
                    self.timer = pygame.time.get_ticks()
                    self.im = ImageRect(self.screen, self.filename + self.dir + '_' + str(self.state), 18, 18)
                    self.im.rect.centerx = self.col * 10 + 5
                    self.im.rect.centery = self.row * 10 + 5
                    self.rect = self.im.rect
                else:
                    self.awake = True
                    self.nextrow = self.row
                    self.nextcol = self.col - 1


    def blitme(self):
        self.im.blitme()
