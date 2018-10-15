import pygame
from eventloop import EventLoop
from maze import Maze
from pac_man import PacMan
from ghost import Ghost
from pygame.sprite import Group


class Game:
    BLACK = (0, 0, 0)
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((280, 360))
        pygame.display.set_caption("Pacman Portal")

        self.maze = Maze(self.screen, 'mazefile1.txt', 'brick', 'portal', 'shield', 'pill')
        self.p_man = PacMan(self.screen, 22, 13, self.maze)
        self.pinky = Ghost('p', self.p_man, self.screen, self.maze, 10, 14)
        self.blinky = Ghost('b', self.p_man, self.screen, self.maze, 16, 14)
        self.ghosts = Group()
        self.ghosts.add(self.blinky)
        self.ghosts.add(self.pinky)

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

        pygame.display.flip()
    
    def play(self):
        loop = EventLoop(False, self.p_man, self.maze, self.ghosts)
        
        while not loop.finished:
            loop.check_events()
            loop.check_collisions()
            self.update_screen()


game = Game()
game.play()
