import pygame
from pygame.constants import *
import config as cfg
from window import Window
from player import Player
from ball import Ball


class Controller:
    def __init__(self):
        self._window = Window()
        # Game Objects
        self._player1 = Player(10)
        self._player2 = Player(cfg.WIDTH-cfg.P_WIDTH-10)
        self._ball = Ball()
        # Game Control
        self._game_speed = 3
        self._running = False
        self._game_in_progress = False
        self._count = 0
        self._goal = False
        self._paused = False
        self._finished = False
        self._winner = None
    
    def run(self):
        self._running = True
        clock = pygame.time.Clock()
        while self._running:
            clock.tick(cfg.FPS)
            self.keyboard_input()
            self._window.display(self._player1, self._player2, self._ball, self._game_in_progress, self._paused, self._finished, self._winner, self._count, self._goal)
            if self._game_in_progress:
                if self._count:
                    self._count -= 1
                    pygame.time.delay(1000)
                elif self._goal:
                    self.reset_positions()
                    self._goal = False
                    self._count = 3
                    pygame.time.delay(2000)
                else:
                    if not self._paused:
                        self._ball.move(self._game_speed)
                        self.check_goal()
                        self.check_collisions()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
                if event.type == KEYDOWN:
                    if pygame.key.get_pressed()[K_p]:
                        if self._paused:
                            self.unpause()
                        else:
                            self.pause()


    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if self._game_in_progress:
            if not self._paused and not self._count:
                if keys[K_w]:
                    self._player1.move_up()
                elif keys[K_s]:
                    self._player1.move_down()
                if keys[K_UP]:
                    self._player2.move_up()
                elif keys[K_DOWN]:
                    self._player2.move_down()
        else:
            if keys[K_q]:
                exit(1)
            if keys[K_r]:
                if not self._game_in_progress:
                    if self._finished:
                        self.restart()
                    else:
                        self.start()

    def start(self):
        self._game_in_progress = True
        self._count = 3

    def pause(self):
        self._paused = True
    
    def unpause(self):
        self._paused = False

    def restart(self):
        self._player1 = Player(10)
        self._player2 = Player(cfg.WIDTH-cfg.P_WIDTH-10)
        self._ball = Ball()
        self._game_in_progress = True
        self._finished = False
        self._goal = False
        self._count = 3

    def reset_positions(self):
        self._ball.reset_position()
        self._player1.reset_position()
        self._player2.reset_position()
        self._game_speed = 3

    def check_goal(self):
        if self._ball.x() > cfg.WIDTH:
            self._player1.increase_score()
            self._goal = True
        if self._ball.x()+cfg.BALL_SIZE < 0:
            self._player2.increase_score()
            self._goal = True
        self.check_end_game()

    def check_end_game(self):
        if self._player1.score() == cfg.WIN:
            self._finished = True
            self._game_in_progress = False
            self._winner = 1
        if self._player2.score() == cfg.WIN:
            self._finished = True
            self._game_in_progress = False
            self._winner = 2

    def check_collisions(self):
        if (self._ball.check_collision(self._player1, self._player2)):
            self._game_speed += 0.01




        