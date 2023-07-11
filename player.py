import pygame
import config as cfg


class Player:
    def __init__(self, x):
        self._x = x
        self._y = cfg.HEIGHT/2 - cfg.P_HEIGHT//2
        self._score = 0
        self._hitbox = pygame.Rect(self._x, self._y, cfg.P_WIDTH, cfg.P_HEIGHT)
    
    def score(self):
        return self._score
    
    def increase_score(self):
        self._score += 1

    def hitbox(self):
        return self._hitbox
    
    def update_hitbox(self):
        self._hitbox.update(self._x, self._y, cfg.P_WIDTH, cfg.P_HEIGHT)

    def move_up(self):
        if self._y > 10:
            self._y -= cfg.MOVE_VEL
            self.update_hitbox()
    
    def move_down(self):
        if self._y < cfg.HEIGHT-cfg.P_HEIGHT-10:
            self._y += cfg.MOVE_VEL
            self.update_hitbox()
    
    def reset_position(self):
        self.__y = cfg.HEIGHT/2 - cfg.P_HEIGHT/2
        self.update_hitbox()
