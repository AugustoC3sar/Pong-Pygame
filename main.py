import pygame
from pygame.constants import *
import random


pygame.font.init()

WIDTH, HEIGHT = 700, 500
FPS = 60
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 80
BALL_DIMENSION = 20
MOVE_VEL = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
DIRECTIONS = ('TOP-RIGHT','BOTTOM-RIGHT','TOP-LEFT','BOTTOM-LEFT')
MAIN_FONT = pygame.font.SysFont('Helvetica', 30)
game_speed = 3


class Engine:
    def __init__(self):
        self.__player1 = Player(10)
        self.__player2 = Player(WIDTH-PLAYER_WIDTH-10)
        self.__ball = Ball()
        self.__root = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__collisions = 0
        self.__run = True
        self.__end = False
        self.__goal = False
        self.__winner = 'NONE'
        self.__mouse_pos = (0,0)

    def game_loop(self):
        clock = pygame.time.Clock()
        self.__root.fill(BLACK)
        self.draw_all()
        pygame.display.update()
        pygame.time.delay(2000)
        while self.__run:
            clock.tick(FPS)
            self.__root.fill(BLACK)
            if self.__end:
                self.end_game_screen()
            else:
                self.draw_all()
                self.get_key()
                self.__ball.move()
                self.check_collisions()
                if self.__goal:
                    self.reset_positions()
                    self.__root.fill(BLACK)
                    self.draw_all()
                    pygame.display.update()
                    self.__goal = False
                    pygame.time.delay(2000)
                self.check_goal()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__run = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.__mouse_pos = pygame.mouse.get_pos()
            
            pygame.display.update()

    def draw_all(self):
        self.draw_ball()
        self.draw_players()
        self.draw_line()
        self.draw_scores()

    def draw_players(self):
        pygame.draw.rect(self.__root, WHITE, self.__player1.hitbox)
        pygame.draw.rect(self.__root, WHITE, self.__player2.hitbox)

    def draw_ball(self):
        pygame.draw.rect(self.__root, WHITE, self.__ball.hitbox)

    def draw_line(self):
        pygame.draw.line(self.__root, WHITE, (WIDTH/2,0), (WIDTH/2,HEIGHT))

    def draw_scores(self):
        player1 = MAIN_FONT.render(f'{self.__player1.score}', False, WHITE)
        player2 = MAIN_FONT.render(f'{self.__player2.score}', False, WHITE)
        self.__root.blit(player1, ((WIDTH/2)-30, 5))
        self.__root.blit(player2, ((WIDTH/2)+15, 5))

    def check_collisions(self):
        global game_speed
        if self.__player1.hitbox.colliderect(self.__ball.hitbox):
            if self.__ball.direction == 'TOP-LEFT':
                self.__ball.direction = 'TOP-RIGHT'
            else:
                self.__ball.direction = 'BOTTOM-RIGHT'
            self.__collisions += 1
        if self.__player2.hitbox.colliderect(self.__ball.hitbox):
            if self.__ball.direction == 'TOP-RIGHT':
                self.__ball.direction = 'TOP-LEFT'
            else:
                self.__ball.direction = 'BOTTOM-LEFT'
            self.__collisions += 1
        if self.__collisions == 5:
            self.__collisions = 0
            game_speed += 0.5

    def check_goal(self):
        if self.__ball.x > WIDTH:
            self.__player1.score += 1
            self.__goal = True
        if self.__ball.x + BALL_DIMENSION < 0:
            self.__player2.score += 1
            self.__goal = True
        self.check_end_game()

    def check_end_game(self):
        if self.__player1.score == 5:
            self.__end = True
            self.__winner = 'Player 1'
        if self.__player2.score == 5:
            self.__end = True
            self.__winner = 'Player 2'

    def end_game_screen(self):
        winner_msg = MAIN_FONT.render(f'Winner: {self.__winner}!',False,(255,255,255))
        winner_rect = winner_msg.get_rect(center=((WIDTH/2),(HEIGHT/2)-50))
        play_again = MAIN_FONT.render('Play Again?',False,(255,255,255))
        play_again_rect = play_again.get_rect(center=((WIDTH/2),(HEIGHT/2)))
        yes = MAIN_FONT.render('YES', False, (255,255,255))
        yes_rect = yes.get_rect(center=((WIDTH/2)-50, (HEIGHT/2)+50))
        no = MAIN_FONT.render('NO',False,(255,255,255))
        no_rect = no.get_rect(center=((WIDTH/2)+50, (HEIGHT/2)+50))
        self.__root.blit(winner_msg, winner_rect)
        self.__root.blit(play_again, play_again_rect)
        self.__root.blit(yes, yes_rect)
        self.__root.blit(no, no_rect)
        if no_rect.collidepoint(self.__mouse_pos):
            self.__run = False
        elif yes_rect.collidepoint(self.__mouse_pos):
            self.__end = False
            self.reset_game()

    def reset_positions(self):
        global game_speed
        self.__ball.reset_position()
        self.__player1.reset_position()
        self.__player2.reset_position()
        game_speed = 3
        self.__collisions = 0

    def reset_game(self):
        self.reset_positions()
        self.__player1.score = 0
        self.__player2.score = 0
        self.__root.fill(BLACK)
        self.draw_all()
        self.__mouse_pos = (0,0)
        pygame.display.update()
        pygame.time.delay(2000)

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

    def reset_position(self):
        self.__y = HEIGHT/2 - PLAYER_HEIGHT/2
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

    @direction.setter
    def direction(self, new_dir):
        self.__direction = new_dir

    @property
    def hitbox(self):
        return self.__hitbox

    def update_hitbox(self):
        self.__hitbox = pygame.Rect(self.__x, self.__y, BALL_DIMENSION, BALL_DIMENSION)

    def move(self):
        if self.__direction == 'TOP-RIGHT':
            self.__x += game_speed
            self.__y -= game_speed
            if self.__y <= 0:
                self.__direction = 'BOTTOM-RIGHT'
        if self.__direction == 'BOTTOM-RIGHT':
            self.__x += game_speed
            self.__y += game_speed
            if self.__y >= HEIGHT-BALL_DIMENSION:
                self.__direction = 'TOP-RIGHT'
        if self.__direction == 'TOP-LEFT':
            self.__x -= game_speed
            self.__y -= game_speed
            if self.__y <= 0:
                self.__direction = 'BOTTOM-LEFT'
        if self.__direction == 'BOTTOM-LEFT':
            self.__x -= game_speed
            self.__y += game_speed
            if self.__y >= HEIGHT-BALL_DIMENSION:
                self.__direction = 'TOP-LEFT'
        self.update_hitbox()

    def reset_position(self):
        self.__x = WIDTH/2 - BALL_DIMENSION/2
        self.__y = HEIGHT/2 - BALL_DIMENSION/2
        self.__direction = random.choice(DIRECTIONS)
        self.update_hitbox()


game = Engine()
game.game_loop()
