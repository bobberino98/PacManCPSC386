import pygame
import sys



class EventLoop:
    
    def __init__(self, p_man, maze, ghosts, stats, pb):

        self.finished = False
        self.won = False
        self.p_man = p_man
        self.maze = maze
        self.ghosts = ghosts
        self.stats = stats
        self.pb = pb
        self.start_time = 0
        self.eat_timer = 0
        self.counter = 1

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)

    def check_play_button(self, mouse_x, mouse_y):
        button_clicked = self.pb.rect.collidepoint(mouse_x, mouse_y)

        if button_clicked and not self.stats.game_active:
            pygame.mouse.set_visible(False)
            self.stats.game_active = True
            self.start_time = pygame.time.get_ticks()

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
            self.p_man.create_portal(1)
        elif event.key == pygame.K_e:
            self.p_man.create_portal(2)
        elif event.key == pygame.K_ESCAPE:
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

        if len(self.maze.dots.sprites()) == 0 and len(self.maze.pills.sprites()) == 0:
            self.won = True

        collisions = pygame.sprite.spritecollide(self.p_man, self.ghosts, False)
        if collisions:
            for sprite in collisions:
                if sprite.frightened and not sprite.eaten:
                    sprite.eaten = True
                    temp = pygame.mixer.Sound("sounds/eating_ghost.wav")
                    temp.set_volume(1)

                    temp.play()

                    if pygame.time.get_ticks() - self.eat_timer < 500:
                        self.counter += 1
                    else:
                        self.counter = 1
                    self.stats.score += self.counter * 200
                    self.eat_timer = pygame.time.get_ticks()

                elif not sprite.eaten:
                    self.p_man.dead = True
