import operator
import pygame
import random
import string
import time
import sys
import os

from pygame.locals import *
from threading import *
from settings import *
from sprites import *
from os import path

pygame.init()
pygame.display.set_caption(TITLE)
game_folder = path.dirname(__file__)


class Game:

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.game_font = pygame.font.Font('Roboto-Thin.ttf', 40)

        self.pause_button = Button(self.screen, 0, 650, 120, 50, BACKGROUND_COLOR, BACKGROUND_COLOR, 'Pause', 'Roboto-Thin', 20)

        self.game_over = False
        self.touchscreeen = True

        self.highscore = 0
        self.score = 0
        self.speed = 1
        self.deaths = 0
        self.counter = 0

    def events(self):
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pause_menu.run()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                if self.pause_button.is_clicked(mouse_pos):
                    pause_menu.run()

    def update(self):
        # Each time the score is a multiple of 10 the game spawns an Enemy
        # 3/20 of chance that the enemy is a wall
        # 5/20 of chance that the enemy is moving
        if not operator.mod(self.score, 10):
            temp = int(random.uniform(0, 20))
            if   temp >= 1 and temp <= 3 and self.counter <= 0: EnemyWall(self); self.counter = 5
            elif temp >= 3 and temp <= 8:                       EnemyMoving(self)
            else:                                               Enemy(self)
            self.counter -= 1

        # Each time the score is a multiple of 1000 the game automatically saves the data
        if not operator.mod(self.score, 1000):
            self.save_data()

        self.all_sprites.update()
        self.score += 1
        self.speed = self.score ** 1.2
        if self.highscore <= self.score: self.highscore = self.score

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        self.pause_button.draw()
        self.score_label = self.game_font.render('Score: ' + str(self.score), 1, BLACK)
        self.screen.blit(self.score_label, (0, 0))
        self.highscore_label = self.game_font.render('Highscore: ' + str(self.highscore), 1, BLACK)
        self.screen.blit(self.highscore_label, (0, 50))
        self.deaths_label = self.game_font.render('Deaths: ' + str(self.deaths), 1, BLACK)
        self.screen.blit(self.deaths_label, (0, 100))
        pygame.display.update()

    def run(self):
        self.all_sprites.empty()
        self.player = Player(self, WIDTH / 2, HEIGHT * 4 / 5)
        while not self.game_over:
            try:
                # If the player pauses the game, this sets dt to normal
                self.dt = self.clock.tick(FPS) / 10
                if self.dt >= 5:
                    self.dt = 1.6

                self.events()
                self.update()
                self.draw()
            except:
                raise

    def save_data(self):
        file = open('data.txt', 'w')
        file_str = file.write(str(self.highscore) + ';' + str(self.deaths) + ';' + str(self.touchscreeen) + ';')

    def load_data(self):
        file = open('data.txt', 'r')
        file_str = file.read()
        try:
            self.highscore = int(file_str[0 : file_str.find(';')])
            self.deaths = int(file_str[file_str.find(';') + 1 : file_str.find(';', file_str.find(';') + 1,)])
            self.touchscreeen = bool(1)
        except:
            self.highscore = 0
            self.deaths = 0
            self.touchscreeen = True

    def reset_data(self):
        file = open('data.txt', 'w')
        file_str = file.write('0;0;0;')
        self.load_data()

class Main_Menu:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.start_button = Button(self.screen, 25, 100, 665, 120, BLACK, BLACK, 'Start', 'Roboto-Thin', 90, BACKGROUND_COLOR)
        self.settings_button = Button(self.screen, 25, 250, 665, 120, BLACK, BLACK, 'Options', 'Roboto-Thin', 90, BACKGROUND_COLOR)
        self.quit_button = Button(self.screen, 25, 400, 665, 120, BLACK, BLACK, 'Quit', 'Roboto-Thin', 90, BACKGROUND_COLOR)

        self.reset_stats_button = Button(self.screen, 500, 1200, 215, 60, BLACK, BLACK, 'Reset Stats', 'Roboto-Thin', 20, BACKGROUND_COLOR)

        self.app_quit = False


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.quit_button.is_clicked(mouse_pos):
                    game.save_data()
                    pygame.quit()
                    sys.exit()
                if self.start_button.is_clicked(mouse_pos):
                    game.game_over = False
                    game.run()
                if self.settings_button.is_clicked(mouse_pos):
                    settings_munu.run()
                if self.reset_stats_button.is_clicked(mouse_pos):
                    game.reset_data()

    def draw(self):
        game.screen.fill(BACKGROUND_COLOR)
        self.start_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()
        self.reset_stats_button.draw()
        pygame.display.update()

    def run(self):
        try:
            save_data.start()
        except:
            pass
        game.load_data()
        while True:
            self.events()
            self.draw()

class Settings_Menu:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.touchscreeen_button = Button(self.screen, 25, 100, 665, 120, BLACK, BLACK, 'Touchscreeen', 'Roboto-Thin', 90, BACKGROUND_COLOR)
        self.back_button = Button(self.screen, 25, 250, 665, 120, BLACK, BLACK, 'Back', 'Roboto-Thin', 90, BACKGROUND_COLOR)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.touchscreeen_button.is_clicked(mouse_pos):
                    game.touchscreeen = not game.touchscreeen
                if self.back_button.is_clicked(mouse_pos):
                    game.save_data()
                    main_menu.run()

    def draw(self):
        game.screen.fill(BACKGROUND_COLOR)
        self.touchscreeen_button.draw()
        self.back_button.draw()
        pygame.display.update()

    def run(self):
        game.load_data()
        while True:
            self.events()
            self.draw()

class Pause_Menu:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.back_button = Button(self.screen, 25, 250, 665, 120, BLACK, BLACK, 'Back', 'Roboto-Thin', 90, BACKGROUND_COLOR)
        self.quit_button = Button(self.screen, 25, 400, 665, 120, BLACK, BLACK, 'Quit', 'Roboto-Thin', 90, BACKGROUND_COLOR)

        self.overlay_menu = pygame.Surface(self.screen.get_size())
        self.overlay_menu.set_alpha(150)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self.paused = False
                if self.quit_button.is_clicked(mouse_pos):
                    main_menu.run()

    def update(self):
        pass

    def draw(self):
        self.back_button.draw()
        self.quit_button.draw()
        pygame.display.update()

    def run(self):
        self.paused = True
        self.screen.blit(self.overlay_menu, (0, 0))
        while self.paused:
            self.events()
            self.update()
            self.draw()

class Button(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, w, h, button_color_active, button_color_inactive, text, font, size = 50, text_color = BLACK):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.button_color_active = button_color_active
        self.button_color_inactive = button_color_inactive
        self.text = text
        self.font = path.join(game_folder, font + '.ttf')
        self.size = size
        self.text_color = text_color

        self.button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.button_font = pygame.font.Font(self.font, self.size)
        self.label = self.button_font.render(self.text, 1, self.text_color)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.button_color_inactive, self.button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_color_active, self.button_rect)
        self.screen.blit(self.label, (self.x + 20, self.y + 0))

    def is_clicked(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

if __name__ == '__main__':

    game = Game()
    main_menu = Main_Menu()
    pause_menu = Pause_Menu()
    settings_munu = Settings_Menu()

    main_menu.run()
