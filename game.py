import pygame
from eventloop import EventLoop
from maze import Maze
from pac_man import PacMan


class Game:
    BLACK = (0, 0, 0)
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((460, 560))
        pygame.display.set_caption("Pacman Portal")
        self.p_man = PacMan(self.screen)

        self.maze = Maze(self.screen, 'mazefile.txt', 'brick', 'portal', 'shield', 'pill', self.p_man)

    def update_screen(self):
        self.screen.fill(Game.BLACK)
        self.maze.blitme()
        self.p_man.update()
        self.p_man.blitme()
        pygame.display.flip()
    
    def play(self):
        loop = EventLoop(False, self.p_man, self.maze)
        
        while not loop.finished:
            loop.check_events()
            loop.check_collisions()
            self.update_screen()


game = Game()
game.play()
