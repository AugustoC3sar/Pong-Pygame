import pygame
import config as cfg
from enum import Enum
from random import choice


class Direction(Enum):
    TR = 1      # TOP RIGHT
    TL = 2      # TOP LEFT
    BR = 3      # BOTTOM RIGHT
    BL = 4      # BOTTOM LEFT

    def directions():
        ds = (Direction.TR, Direction.TL, Direction.BR, Direction.BL)
        return ds


class Ball:
    def __init__(self):
        self._x = cfg.WIDTH//2 - cfg.BALL_SIZE//2
        self._y = cfg.HEIGHT//2 - cfg.BALL_SIZE//2
        self._direction = choice(Direction.directions())
        self._hitbox = pygame.Rect(self._x, self._y, cfg.BALL_SIZE, cfg.BALL_SIZE)
    
    def x(self):
        return self._x
    
    def y(self):
        return self._y
    
    def hitbox(self):
        return self._hitbox
    
    def update_hitbox(self):
        self._hitbox.update(self._x, self._y, cfg.BALL_SIZE, cfg.BALL_SIZE)
    
    def check_collision(self, player1, player2):
        collision = False
        if player1.hitbox().colliderect(self.hitbox()):
            collision = True
            if self._direction == Direction.TL:
                self._direction = Direction.TR
            else:
                self._direction = Direction.BR
        if player2.hitbox().colliderect(self.hitbox()):
            collision = True
            if self._direction == Direction.TR:
                self._direction = Direction.TL
            else:
                self._direction = Direction.BL
        return collision
        

    def move(self, speed):
        if self._direction == Direction.TR:
            self._x += speed
            self._y -= speed
            if self._y <= 0:
                self._direction = Direction.BR
        if self._direction == Direction.BR:
            self._x += speed
            self._y += speed
            if self._y >= cfg.HEIGHT-cfg.BALL_SIZE:
                self._direction = Direction.TR
        if self._direction == Direction.TL:
            self._x -= speed
            self._y -= speed
            if self._y <= 0:
                self._direction = Direction.BL
        if self._direction == Direction.BL:
            self._x -= speed
            self._y += speed
            if self._y >= cfg.HEIGHT-cfg.BALL_SIZE:
                self._direction = Direction.TL
        self.update_hitbox()

    def reset_position(self):
        self._x = cfg.WIDTH//2 - cfg.BALL_SIZE//2
        self._y = cfg.HEIGHT//2 - cfg.BALL_SIZE//2
        self._direction = choice(Direction.directions())
        self.update_hitbox()
