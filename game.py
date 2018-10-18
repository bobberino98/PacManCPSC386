import pygame
from eventloop import EventLoop
from maze import Maze
from pac_man import PacMan
from ghost import Ghost
from pygame.sprite import Group
from stats import GameStats
from scoreboard import Scoreboard
from button import Button


class Game:
    BLACK = (0, 0, 0)
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((280, 360))
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 25)
        self.won = False
        self.lost = False
        pygame.display.set_caption("Pacman Portal")
        self.clock = pygame.time.Clock()
        self.maze = Maze(self.screen, 'mazefile1.txt')
        self.p_man = PacMan(self.screen, 25, 13, self.maze)
        self.pinky = Ghost('p', self.p_man, self.screen, self.maze, 16, 14)
        self.blinky = Ghost('b', self.p_man, self.screen, self.maze, 13, 14)
        self.inky = Ghost('i', self.p_man, self.screen, self.maze, 16, 12, self.blinky)
        self.clyde = Ghost('c', self.p_man, self.screen, self.maze, 16, 16)
        self.ghosts = Group()
        self.ghosts.add(self.blinky)
        self.ghosts.add(self.pinky)
        self.ghosts.add(self.inky)
        self.ghosts.add(self.clyde)
        self.stats = GameStats()
        self.pb = Button(self.screen, "Play", 150)
        self.sb = Scoreboard(self.screen, self.stats)
        self.menu_timer = pygame.time.get_ticks()

    def update_screen(self):

        self.screen.fill(Game.BLACK)
        if self.stats.game_active:

            self.maze.blitme()
            if not self.p_man.dead:
                self.blinky.update_target()
                self.pinky.update_target()
                self.inky.update_target()
                self.clyde.update_target()
                self.ghosts.update(True)
                self.pinky.blitme()
                self.inky.blitme()
                self.blinky.blitme()
                self.clyde.blitme()

            self.p_man.update()
            self.p_man.blitme()
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.show_score()

        elif self.won:
            surface = self.font.render("YOU WIN!", True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centerx))
            self.screen.blit(surface, text_rect)
            surface = self.font2.render("YOUR SCORE:" + str(self.stats.score), True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centerx + 50))
            self.screen.blit(surface, text_rect)
            surface = self.font2.render("HIGH SCORE:" + str(self.stats.high_score), True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centerx + 100))
            self.screen.blit(surface, text_rect)
        elif self.lost:
            surface = self.font.render("GAME OVER", True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centerx))
            self.screen.blit(surface, text_rect)
            surface = self.font2.render("YOUR SCORE:" + str(self.stats.score), True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centerx + 50))
            self.screen.blit(surface, text_rect)
            surface = self.font2.render("HIGH SCORE:" + str(self.stats.high_score), True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centerx + 100))
            self.screen.blit(surface, text_rect)
        else:

            surface = self.font.render("PacMan", True, (255, 255, 255))
            text_rect = surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.top + 25))
            self.screen.blit(surface, text_rect)
            self.pb.draw_button()
            if pygame.time.get_ticks() - self.menu_timer >= 500:
                surface = self.font2.render('"BLINKY"', True, (255, 255, 255))
                text_rect = surface.get_rect(center=(self.screen_rect.centerx + 20, self.screen_rect.top +75))
                self.screen.blit(surface, text_rect)
                b_image = self.blinky.im.image
                b_rect = b_image.get_rect()
                b_rect.centery = self.screen_rect.top + 75
                b_rect.centerx = self.screen_rect.centerx - 50
                self.screen.blit(b_image, b_rect)
            if pygame.time.get_ticks() - self.menu_timer >= 1500:
                surface = self.font2.render('"PINKY"', True, (255, 255, 255))
                text_rect = surface.get_rect(center=(self.screen_rect.centerx + 20, self.screen_rect.top + 100))
                self.screen.blit(surface, text_rect)
                p_image = self.pinky.im.image
                p_rect = p_image.get_rect()
                p_rect.centery = self.screen_rect.top + 100
                p_rect.centerx = self.screen_rect.centerx - 50
                self.screen.blit(p_image, p_rect)
            if pygame.time.get_ticks() - self.menu_timer >= 2500:
                surface = self.font2.render('"INKY"', True, (255, 255, 255))
                text_rect = surface.get_rect(center=(self.screen_rect.centerx + 20, self.screen_rect.top + 125))
                self.screen.blit(surface, text_rect)
                i_image = self.inky.im.image
                i_rect = i_image.get_rect()
                i_rect.centery = self.screen_rect.top + 125
                i_rect.centerx = self.screen_rect.centerx - 50
                self.screen.blit(i_image, i_rect)
            if pygame.time.get_ticks() - self.menu_timer >= 3500:
                surface = self.font2.render('"CLYDE"', True, (255, 255, 255))
                text_rect = surface.get_rect(center=(self.screen_rect.centerx + 20, self.screen_rect.top + 150))
                self.screen.blit(surface, text_rect)
                c_image = self.clyde.im.image
                c_rect = c_image.get_rect()
                c_rect.centery = self.screen_rect.top + 150
                c_rect.centerx = self.screen_rect.centerx - 50
                self.screen.blit(c_image, c_rect)
        pygame.display.flip()

    def play(self):
        loop = EventLoop(self.p_man, self.maze, self.ghosts, self.stats, self.pb)

        while not loop.finished:
            loop.check_events()
            if self.stats.game_active:
                self.pinky.start(loop.start_time)
                self.inky.start(loop.start_time)
                self.blinky.start(loop.start_time)
                self.clyde.start(loop.start_time)
                loop.check_collisions()
            self.update_screen()
            self.clock.tick(60)
            self.lost = self.p_man.finished
            self.won = loop.won
            if self.won:
                self.stats.game_active = False
            elif self.lost:
                self.stats.game_active = False


game = Game()
game.play()
game.stats.write()
