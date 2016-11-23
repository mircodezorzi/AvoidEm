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

try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

pygame.init()
pygame.display.set_caption(TITLE)
game_folder = path.dirname(__file__)

class game:

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.game_font = pygame.font.Font('origami.ttf', 40)
        self.soundtrack = pygame.mixer.Sound('soundtrack.wav')

        self.pause_button = Button(self.screen, 0, 1200, 100, 200, BACKGROUND_COLOR, BACKGROUND_COLOR, 'Pause', 'origami', 20)

        self.game_over = False
        self.game_paused = False
        self.highscore = 0
        self.score = 0
        self.speed = 1
        self.deaths = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            self.player.x = mouse_pos[0]

            if event.type == MOUSEBUTTONDOWN:
                if self.pause_button.is_clicked(mouse_pos):
                    self.game_paused = True
                    pause_menu.run()

    def update(self):
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
        self.screen.blit(self.deaths_label, (400, 0))
        pygame.display.update()

    def run(self):
        self.all_sprites.empty()
        self.player = Player(self, WIDTH / 2, HEIGHT * 4 / 5)
        while not self.game_over:
            try:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
            except:
                pass

    def save_data(self):
        file = open('data.txt', 'w')
        file_str = file.write(str(self.highscore) + ';' + str(self.deaths) + ';')

    def load_data(self):
        file = open('data.txt', 'r')
        file_str = file.read()
        try:
            self.highscore = int(file_str[0 : file_str.find(';')])
            self.deaths = int(file_str[file_str.find(';') + 1 : file_str.find(';', file_str.find(';') + 1,)])
        except:
            self.highscore = 0
            self.deaths = 0

    def reset_data(self):
        file = open('data.txt', 'w')
        file_str = file.write('0;0;')
        self.load_data()

class Main_Menu:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.start_button = Button(self.screen, 25, 100, 665, 120, BLACK, BLACK, 'Start', 'origami', 90, BACKGROUND_COLOR)
        self.settings_button = Button(self.screen, 25, 250, 665, 120, BLACK, BLACK, 'Settings', 'origami', 90, BACKGROUND_COLOR)
        self.quit_button = Button(self.screen, 25, 400, 665, 120, BLACK, BLACK, 'Quit', 'origami', 90, BACKGROUND_COLOR)

        self.reset_stats_button = Button(self.screen, 500, 1200, 215, 60, BLACK, BLACK, 'Reset Stats', 'origami', 20, BACKGROUND_COLOR)

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
                    try:
                        create_enemy.start()
                    except:
                        pass
                    game.game_over = False
                    game.run()
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
        game.soundtrack.play(loops = 100)
        while True:
            self.events()
            self.draw()

class Pause_Menu():

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.back_button = Button(self.screen, 25, 250, 665, 120, BLACK, BLACK, 'Back', 'origami', 90, BACKGROUND_COLOR)
        self.quit_button = Button(self.screen, 25, 400, 665, 120, BLACK, BLACK, 'Quit', 'origami', 90, BACKGROUND_COLOR)

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
                    game.game_paused = False
                if self.quit_button.is_clicked(mouse_pos):
                    main_menu.run()

    def update(self):
        pass

    def draw(self):
        self.back_button.draw()
        self.quit_button.draw()
        pygame.display.update()

    def run(self):
        self.screen.blit(self.overlay_menu, (0, 0))
        while game.game_paused:
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
        self.screen.blit(self.label, (self.x + 20, self.y + 20))

    def is_clicked(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

class Create_Enemy(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            while not game.game_paused:
                time.sleep((game.score + 1) / game.speed)
                Enemy(game)


class Save_Data(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(10)
            game.save_data()

if __name__ == '__main__':

    game = game()
    main_menu = Main_Menu()
    pause_menu = Pause_Menu()
    create_enemy = Create_Enemy()
    save_data = Save_Data()

    main_menu.run()
