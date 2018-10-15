import pygame
from eventloop import EventLoop
from maze import Maze
from pac_man import PacMan
from ghost import Ghost
from pygame.sprite import Group
from stats import GameStats
from scoreboard import Scoreboard

class Game:
    BLACK = (0, 0, 0)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((280, 360))
        pygame.display.set_caption("Pacman Portal")
        self.clock = pygame.time.Clock()
        self.maze = Maze(self.screen, 'mazefile1.txt', 'brick', 'portal', 'shield', 'pill')
        self.p_man = PacMan(self.screen, 25, 13, self.maze)
        self.pinky = Ghost('p', self.p_man, self.screen, self.maze, 13, 14)
        self.blinky = Ghost('b', self.p_man, self.screen, self.maze, 19, 14)
        self.ghosts = Group()
        self.ghosts.add(self.blinky)
        self.ghosts.add(self.pinky)
        self.stats = GameStats()
        self.sb = Scoreboard(self.screen, self.stats)

    def update_screen(self):
        self.screen.fill(Game.BLACK)
        self.maze.blitme()
        if not self.p_man.dead:
            self.blinky.update_target()
            self.pinky.update_target()
            self.ghosts.update(True)
            self.pinky.blitme()
            self.blinky.blitme()
        self.p_man.update()
        self.p_man.blitme()
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.show_score()


        pygame.display.flip()
    
    def play(self):
        loop = EventLoop(False, self.p_man, self.maze, self.ghosts, self.stats)
        
        while not loop.finished:
            loop.check_events()
            loop.check_collisions()
            self.update_screen()
            self.clock.tick(60)
            loop.finished = self.p_man.finished


game = Game()
game.play()
game.stats.write()
