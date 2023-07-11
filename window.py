import pygame
import config as cfg


class Window:
    def __init__(self):
        self._window = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    
    def draw_maze(self):
        # Top line
        pygame.draw.line(self._window, cfg.WHITE, (0, 0), (cfg.WIDTH, 0), 5)
        # Bottom line
        pygame.draw.line(self._window, cfg.WHITE, (0, cfg.HEIGHT), (cfg.WIDTH, cfg.HEIGHT), 5)
        # Left line
        pygame.draw.line(self._window, cfg.WHITE, (0, 0), (0, cfg.HEIGHT), 5)
        # Right line
        pygame.draw.line(self._window, cfg.WHITE, (cfg.WIDTH, 0), (cfg.WIDTH, cfg.HEIGHT), 5)
        # Middle line
        pygame.draw.line(self._window, cfg.WHITE, (cfg.WIDTH//2, 0), (cfg.WIDTH//2, cfg.HEIGHT), 5)

    def draw_start(self):
        start = cfg.FONT.render('Press R to start the game', False, cfg.WHITE)
        start_rect = start.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))

        self._window.blit(start, start_rect)

    def draw_pause_screen(self):
        bg = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA)
        bg.fill((0,0,0,128))
        
        pause = cfg.FONT.render('PAUSED', False, cfg.WHITE)
        pause_rect = pause.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))

        self._window.blit(bg, (0,0))
        self._window.blit(pause, pause_rect)

    def draw_end_game_screen(self, winner):
        end_info = cfg.FONT.render(f'GAME OVER! Player {winner} wins!', False, cfg.WHITE)
        end_rect = end_info.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)-50))
        
        restart = cfg.FONT.render('Press R to play again!',False, cfg.WHITE)
        restart_rect = restart.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))
        
        game_quit = cfg.FONT.render('Press Q to quit',False, cfg.WHITE)
        game_quit_rect = game_quit.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)+50))

        self._window.blit(end_info, end_rect)
        self._window.blit(restart, restart_rect)
        self._window.blit(game_quit, game_quit_rect)

    def draw_object(self, object):
        pygame.draw.rect(self._window, cfg.WHITE, object.hitbox())

    def draw_scores(self, p1, p2):
        s1 = cfg.FONT.render(f'{p1.score()}', False, cfg.WHITE)
        s2 = cfg.FONT.render(f'{p2.score()}', False, cfg.WHITE)
        self._window.blit(s1, ((cfg.WIDTH//2)-35, 10))
        self._window.blit(s2, ((cfg.WIDTH//2)+20, 10))

    def display(self, player1, player2, ball, game_in_progress, paused, finished, winner, count, goal):
        self._window.fill(cfg.BG_COLOR)
        if game_in_progress:
            if count:
                self.display_countdown(count)
            elif goal:
                self.display_goal()
            else:
                self.draw_maze()
                self.draw_object(player1)
                self.draw_object(player2)
                self.draw_object(ball)
                self.draw_scores(player1, player2)
            if paused:
                self.draw_pause_screen()
        else:
            if finished:
                self.draw_end_game_screen(winner)
            else:
                self.draw_start()
        pygame.display.update()
    
    def display_countdown(self, c):
        countdown = cfg.FONT.render(f'{c}', False, cfg.WHITE)
        countdown_rect = countdown.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))

        self._window.blit(countdown, countdown_rect)
        pygame.display.update()
    
    def display_goal(self):
        goal = cfg.FONT.render('GOOOOOOOAL!', False, cfg.WHITE)
        goal_rect = goal.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))

        self._window.blit(goal, goal_rect)
        pygame.display.update()
