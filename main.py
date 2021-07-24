import pygame
from pygame.constants import *
import random


WIDTH, HEIGHT = 900, 500
FPS = 60
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 80
BALL_DIMENSION = 20
MOVE_VEL = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
DIRECTIONS = ('TOP-RIGHT','BOTTOM-RIGHT','TOP-LEFT','BOTTOM-LEFT')
game_speed = 3


class Engine:
    def __init__(self):
        self.__player1 = Player(10)
        self.__player2 = Player(WIDTH-PLAYER_WIDTH-10)
        self.__ball = Ball()
        self.__root = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__run = True
        self.__end = False

    def game_loop(self):
        clock = pygame.time.Clock()
        while self.__run:
            clock.tick(FPS)
            self.__root.fill(BLACK)
            if self.__end:
                pass
            else:
                self.draw_ball()
                self.draw_players()
                self.draw_line()
                self.get_key()
                self.__ball.move()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__run = False
            
            pygame.display.update()

    def draw_players(self):
        pygame.draw.rect(self.__root, WHITE, self.__player1.hitbox)
        pygame.draw.rect(self.__root, WHITE, self.__player2.hitbox)

    def draw_ball(self):
        pygame.draw.rect(self.__root, WHITE, self.__ball.hitbox)

    def draw_line(self):
        pygame.draw.line(self.__root, WHITE, (WIDTH/2,0), (WIDTH/2,HEIGHT), 1)

    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.__player1.move_up()
        elif keys[K_s]:
            self.__player1.move_down()
        if keys[K_UP]:
            self.__player2.move_up()
        elif keys[K_DOWN]:
            self.__player2.move_down()

class Player:
    def __init__(self, x):
        self.__score = 0
        self.__x = x
        self.__y = HEIGHT/2 - PLAYER_HEIGHT/2
        self.__hitbox = pygame.Rect(self.__x, self.__y, PLAYER_WIDTH, PLAYER_HEIGHT)

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_score):
        self.__score = new_score

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def hitbox(self):
        return self.__hitbox

    def update_hitbox(self):
        self.__hitbox.update(self.__x, self.__y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move_up(self):
        if self.__y > 10:
            self.__y -= MOVE_VEL
            self.update_hitbox()

    def move_down(self):
        if self.__y < HEIGHT-PLAYER_HEIGHT-10:
            self.__y += MOVE_VEL
            self.update_hitbox()


class Ball:
    def __init__(self):
        self.__x = WIDTH/2 - BALL_DIMENSION/2
        self.__y = HEIGHT/2 - BALL_DIMENSION/2
        self.__direction = random.choice(DIRECTIONS)
        self.__hitbox = pygame.Rect(self.__x, self.__y, BALL_DIMENSION, BALL_DIMENSION)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def direction(self):
        return self.__direction

    @property
    def hitbox(self):
        return self.__hitbox

    def update_hitbox(self):
        self.__hitbox = pygame.Rect(self.__x, self.__y, BALL_DIMENSION, BALL_DIMENSION)

    def move(self):
        if self.__direction == 'TOP-RIGHT':
            self.__x += game_speed
            self.__y -= game_speed
            if self.__y == 0:
                self.__direction = 'BOTTOM-RIGHT'
        elif self.__direction == 'BOTTOM-RIGHT':
            self.__x += game_speed
            self.__y += game_speed
            if self.__y == HEIGHT-BALL_DIMENSION:
                self.__direction = 'TOP-RIGHT'
        elif self.__direction == 'TOP-LEFT':
            self.__x -= game_speed
            self.__y -= game_speed
            if self.__y == 0:
                self.__direction = 'BOTTOM-LEFT'
        else:
            self.__x -= game_speed
            self.__y += game_speed
            if self.__y == HEIGHT-BALL_DIMENSION:
                self.__direction = 'TOP-LEFT'
        self.update_hitbox()


game = Engine()
game.game_loop()