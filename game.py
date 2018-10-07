import pygame
from eventloop import EventLoop
from maze import Maze


class Game:
    BLACK = (0, 0, 0)
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((460, 510))
        pygame.display.set_caption("Pacman Portal")
        
        self.maze = Maze(self.screen, 'mazefile.txt', 'brick', 'portal', 'shield', 'pill', "dot")
        
    def update_screen(self):
        self.screen.fill(Game.BLACK)
        self.maze.blitme()
        pygame.display.flip()
    
    def play(self):
        loop = EventLoop(finished = False)
        
        while not loop.finished:
            loop.check_events()
            self.update_screen()


game = Game()
game.play()
