import pygame


WIDTH, HEIGHT = 1080, 500
FPS = 60
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 50
BALL_DIMENSION = 20



class Engine:
    def __init__(self):
        self.__player1 = Player(10)
        self.__player2 = Player(WIDTH-PLAYER_WIDTH-10)
        self.__ball = Ball()
        self.__run = True
        self.__end = False


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


class Ball:
    def __init__(self):
        self.__x = WIDTH/2 - BALL_DIMENSION
        self.__y = HEIGHT/2 - BALL_DIMENSION
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
    def hitbox(self):
        return self.__hitbox

    def update_hitbox(self):
        self.__hitbox = pygame.Rect(self.__x, self.__y, BALL_DIMENSION, BALL_DIMENSION)


game = Engine()
