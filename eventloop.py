import pygame
import sys


class EventLoop:
    
    def __init__(self, finished, p_man, maze, ghosts, stats):
        
        self.finished = finished
        self.p_man = p_man
        self.maze = maze
        self.ghosts = ghosts
        self.stats = stats

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.p_man.moving_right = True
            self.p_man.moving_left = False
            self.p_man.moving_up = False
            self.p_man.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.p_man.moving_left = True
            self.p_man.moving_right = False
            self.p_man.moving_up = False
            self.p_man.moving_down = False
        elif event.key == pygame.K_UP:
            self.p_man.moving_up = True
            self.p_man.moving_left = False
            self.p_man.moving_down = False
            self.p_man.moving_right = False

        elif event.key == pygame.K_DOWN:
            self.p_man.moving_down = True
            self.p_man.moving_left = False
            self.p_man.moving_right = False
            self.p_man.moving_up = False
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.p_man.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.p_man.moving_left = False
        elif event.key == pygame.K_UP:
            self.p_man.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.p_man.moving_down = False

    def check_collisions(self):
        collisions = pygame.sprite.spritecollide(self.p_man, self.maze.dots, True)

        if collisions:
            for sprite in collisions:
                self.maze.dots.remove(sprite)
                self.stats.score += 10

        collisions = pygame.sprite.spritecollide(self.p_man, self.maze.pills, True)

        if collisions:
            for sprite in collisions: 
                self.maze.pills.remove(sprite)
                self.stats.score += 50
                for g in self.ghosts:
                    g.frightened = True
                    g.fear_timer = pygame.time.get_ticks()

        collisions = pygame.sprite.spritecollide(self.p_man, self.ghosts, False)
        if collisions:
            for sprite in collisions:
                if sprite.frightened:
                    sprite.eaten = True

                elif not sprite.eaten:
                    self.p_man.dead = True
