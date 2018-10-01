import pygame


class Settings:
    def __init__(self):
        self.myfont = pygame.font.SysFont('Comic Sans Ms', 30)
        self.player_moving_up = False
        self.player_moving_down = False
        self.player_moving_left = False
        self.player_moving_right = False
        self.game_running = False
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 200
        self.LINETHICKNESS = 10
        self.PADDLESIZE = 50
        self.PADDLEOFFSET = 20
        self.FONTSIZE = 20
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
        self.HALFSCREEN = (self.WIDTH // 2)
        self.ballDirX = -1.0
        self.ballDirY = -1.0
        self.human_score = 0
        self.ai_score = 0
        self.velocity = 1
        self.AI_detection = self.HALFSCREEN
        self.VICTORY = 'YOU WIN!'
        self.DEFEAT = 'AI WINS!'
        # Colors
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREY = (100, 100, 100)
