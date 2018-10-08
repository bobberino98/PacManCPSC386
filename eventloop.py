import pygame
import sys


class EventLoop:
    
    def __init__(self, finished, p_man, maze):
        
        self.finished = finished
        self.p_man = p_man
        self.maze = maze


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
        elif event.key == pygame.K_LEFT:
            self.p_man.moving_left = True
        elif event.key == pygame.K_UP:
            self.p_man.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.p_man.moving_down = True
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

        collisions = pygame.sprite.spritecollide(self.p_man, self.maze.pills, True)

        if collisions:
            for sprite in collisions: 
                self.maze.pills.remove(sprite)

        for brick in self.maze.bricks:
            if self.p_man.rect.colliderect(brick):
                if self.p_man.moving_down:
                    self.p_man.moving_down = False
                    self.p_man.im.rect.y = brick.top - 1 - self.p_man.rect.height
                elif self.p_man.moving_up:
                    self.p_man.moving_up = False
                    self.p_man.im.rect.y = brick.bottom + 1
                elif self.p_man.moving_left:
                    self.p_man.moving_left = False
                    self.p_man.im.rect.x = brick.right + 1
                elif self.p_man.moving_right:
                    self.p_man.moving_right = False
                    self.p_man.im.rect.x = brick.left - 1 - self.p_man.rect.width
        s_rect = self.p_man.screen.get_rect()
        if self.p_man.rect.x < 0:
            self.p_man.rect.x = s_rect.width
        elif self.p_man.rect.x > s_rect.width:
            self.p_man.rect.x = 0




