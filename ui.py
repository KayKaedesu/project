import pygame
import sys
from pygame.locals import *
from pygame_menu.themes import Theme
from config import BLACK, WHITE, DEFAULT_LEVEL, HUMAN, COMPUTER
import os
import pygame_menu


class Gui:
    def __init__(self):
        """ Initializes graphics. """

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Othello Boardgame")
        gameIcon = pygame.image.load("res/white.jpg")
        pygame.display.set_icon(gameIcon)
        #sounda = pygame.mixer.Sound("res/sans.mp3")
        #pygame.mixer.music.load("res/sans.mp3")
        #pygame.mixer.music.play(-1)
        #sounda.play()

        # colors
        self.BLACK = (0, 0, 0)
        self.BACKGROUND = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (192, 192, 192)

        # display
        self.SCREEN_SIZE = (1280, 960)
        self.BOARD_POS = (200, 40)
        self.BOARD = (240, 80)
        self.BOARD_SIZE = 800
        self.SQUARE_SIZE = 100
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE))

        # messages
        self.BLACK_LAB_POS = (100, self.SCREEN_SIZE[1] / 4)
        self.WHITE_LAB_POS = (1180, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Angsana New", 22)
        self.scoreFont = pygame.font.SysFont("Angsana New", 58)

        # image files (ไม่รู้จะใช้ os path ในตอนแรกๆไปทำไม)
        self.board_img = pygame.image.load(os.path.join("res", "boardbig.jpg")).convert()
        self.black_img = pygame.image.load(os.path.join("res", "blackbig.jpg")).convert()
        self.white_img = pygame.image.load(os.path.join("res", "whitebig.jpg")).convert()
        self.tip_img = pygame.image.load(os.path.join("res", "tipbig.jpg")).convert()
        self.clear_img = pygame.image.load(os.path.join("res", "blankbig.jpg")).convert()
        self.bgimage = pygame.image.load("res/gamebgbig.jpg")
        self.menubg = pygame.image.load("res/menubg.jpg")
        self.cong = pygame.image.load("res/congrat.png")

        # sfx
        self.moves = pygame.mixer.Sound("res/move.mp3")
        self.menusound = ("res/sans.mp3")


    def show_menu(self, start_cb):
        # default game menu settings
        self.level = DEFAULT_LEVEL
        self.player1 = HUMAN
        self.player2 = COMPUTER

        pygame.mixer.music.load(self.menusound)
        pygame.mixer.music.play(-1)
        self.menu = pygame_menu.Menu(960, 1280, 'Othello',
                                     theme=pygame_menu.themes.THEME_DARK)
        self.screen.blit(self.menubg, (0, 0))
        self.menu.add_button('Play', lambda: start_cb(self.player1, self.player2, self.level))
        self.menu.add_selector('First player', [[HUMAN, 1] ,[COMPUTER, 2]],
                               onchange=self.set_player_1)
        self.menu.add_selector('Second player', [[COMPUTER, 2], [HUMAN, 1]],
                               onchange=self.set_player_2)
        self.menu.mainloop(self.screen)
        pygame.mixer.music.stop()

    def set_player_1(self, value, player):
        self.player1 = [0, HUMAN, COMPUTER][player]

    def set_player_2(self, value, player):
        self.player2 = [0, HUMAN, COMPUTER][player]

    def reset_menu(self):
        self.menu.disable()
        self.menu.reset(1)

    def set_difficulty(self, value, difficulty = 2):
        self.level = difficulty

    def show_winner(self, player_color):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.menubg, (0,0))
        playerwinsound = pygame.mixer.Sound("res/win.mp3")
        font = pygame.font.SysFont("Courier New", 34)
        if player_color == WHITE:
            msg = font.render("White player wins", True, self.BLACK)
            msg2 = font.render("Congratulatons", True, self.BLACK)
        elif player_color == BLACK:
            msg = font.render("Black player wins", True, self.BLACK)
            msg2 = font.render("Congratulations", True, self.BLACK)
        else:
            msg = font.render("Tie !", True, self.BLACK)
            msg2 = font.render("Is it possible??", True, self.BLACK)
        self.screen.blit(
            msg, msg.get_rect(
                centerx=self.screen.get_width() / 2, centery=240))
        self.screen.blit(
            msg2, msg2.get_rect(
                centerx=self.screen.get_width() / 2, centery=120))
        self.screen.blit(self.cong, (0, 600))
        pygame.mixer.Sound.play(playerwinsound)
        pygame.display.flip()

    def show_game(self):
        """ Game screen. """
        self.reset_menu()

        # draws initial screen
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.blit(self.bgimage, [0, 0])
        self.score_size = 50
        self.score1 = pygame.Surface((self.score_size, self.score_size))
        self.score2 = pygame.Surface((self.score_size, self.score_size))
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS, self.board_img.get_rect())
        self.put_stone((3, 3), WHITE)
        self.put_stone((4, 4), WHITE)
        self.put_stone((3, 4), BLACK)
        self.put_stone((4, 3), BLACK)
        pygame.display.flip()

    def put_stone(self, pos, color):
        """ วางหมากขาวดำ """
        if pos == None:
            return

        pos = (pos[1], pos[0])

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        else:
            img = self.tip_img

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        self.moves.play()
        pygame.display.flip()

    def clear_square(self, pos):
        # flip orientation
        pos = (pos[1], pos[0])

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(self.clear_img, (x, y), self.clear_img.get_rect())
        pygame.display.flip()

    def get_mouse_input(self):
        """ คลิกเม้าส์, quit"""
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # คุมเม้าส์
                    if mouse_x > self.BOARD_SIZE + self.BOARD[0] or \
                       mouse_x < self.BOARD[0] or \
                       mouse_y > self.BOARD_SIZE + self.BOARD[1] or \
                       mouse_y < self.BOARD[1]:
                        continue

                    position = ((mouse_x - self.BOARD[0]) // self.SQUARE_SIZE), \
                               ((mouse_y - self.BOARD[1]) // self.SQUARE_SIZE)

                    position = (position[1], position[0])
                    return position

                elif event.type == QUIT:
                    sys.exit(0)

    def update(self, board, blacks, whites, current_player_color):
        """ updates count screen """
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    self.put_stone((i, j), board[i][j])

        blacks_str = '%02d'%int(blacks)
        whites_str = '%02d'%int(whites)
        self.showScore(blacks_str, whites_str, current_player_color)
        pygame.display.flip()

    def showScore(self, blackStr, whiteStr, current_player_color):
        black_background = self.YELLOW if current_player_color == WHITE else self.BACKGROUND
        white_background = self.YELLOW if current_player_color == BLACK else self.BACKGROUND
        text = self.scoreFont.render(blackStr, True, self.BLACK,
                                     black_background)
        text2 = self.scoreFont.render(whiteStr, True, self.WHITE,
                                      white_background)
        self.screen.blit(text,
                         (self.BLACK_LAB_POS[0], self.BLACK_LAB_POS[1] + 40))
        self.screen.blit(text2,
                         (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] + 40))

    def wait_quit(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                break

    def show_valid_moves(self, valid_moves):
        for move in valid_moves:
            self.put_stone(move, 'tip')
