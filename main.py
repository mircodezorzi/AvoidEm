import operator, pygame, random, string, os, sys, time
from pygame.locals import *
from threading import *
from settings import *
from sprites import *
from os import path

pygame.init()
pygame.display.set_caption(TITLE)

class Game:

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.game_font = pygame.font.Font('roboto.ttf', 40)
        self.pause_button = Button(self.screen, 0, 850, 90, 50, BACKGROUND_COLOR, BACKGROUND_COLOR, 'Pause', 'roboto', 20)

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
            if   temp >= 1 and temp <= 3 and self.counter <= 0: EnemyWall(self); self.counter = 10
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
        self.screen.blit(self.score_label, (10, 10))
        self.highscore_label = self.game_font.render('Highscore: ' + str(self.highscore), 1, BLACK)
        self.screen.blit(self.highscore_label, (10, 60))
        self.deaths_label = self.game_font.render('Deaths: ' + str(self.deaths), 1, BLACK)
        self.screen.blit(self.deaths_label, (10, 110))
        pygame.display.update()

    def run(self):
        self.all_sprites.empty()
        self.player = Player(self, WIDTH / 2, HEIGHT * 4 / 5)
        while True:
            try:
                # If the player pauses the game, this sets dt to normal
                self.dt = self.clock.tick(FPS) / 10
                if self.dt >= 5:
                    self.dt = 1.6

                self.events()
                self.update()
                self.draw()
            except:
                # The game is finished
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
            #self.touchscreeen = bool(1)
        except:
            self.highscore = 0
            self.deaths = 0
            #self.touchscreeen = True

    def reset_data(self):
        file = open('data.txt', 'w')
        file_str = file.write('0;0;0;')
        self.load_data()

class Main_Menu:

    def __init__(self):

        # Pygame stuff
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))


        self.settings_menu = False
        self.app_quit = False

        # Main Menu
        self.button_start = Button(self.screen, 50, 600, 400, 80, GRAY, LIGHT_GRAY, 'START', 'roboto-black', 50, WHITE)
        self.button_settings = Button(self.screen, 50, 700, 400, 80, GRAY, LIGHT_GRAY, 'OPTIONS', 'roboto-black', 50, WHITE)
        self.button_quit = Button(self.screen, 50, 800, 400, 80, GRAY, LIGHT_GRAY, 'QUIT', 'roboto-black', 50, WHITE)

        # Settings Menu
        self.button_touchscreen = Button(self.screen, 500, 700, 400, 80, WHITE, WHITE, 'TOUCHSCREEN', 'roboto-black', 50, WHITE)
        self.button_back = Button(self.screen, 500, 800, 400, 80, GRAY, LIGHT_GRAY, 'BACK', 'roboto-black', 50, WHITE)

        # Title
        self.font = path.join('roboto-black.ttf')
        self.title_font = pygame.font.Font(self.font, 200)
        self.title = self.title_font.render('Avoid Em', 1, WHITE)
        self.title_shadow = self.title_font.render('Avoid Em', 1, BLACK)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_quit.is_clicked(mouse_pos):
                    game.save_data()
                    pygame.quit()
                    sys.exit()
                if self.button_start.is_clicked(mouse_pos):
                    self.settings_menu = False
                    game.run()
                if self.button_settings.is_clicked(mouse_pos):
                    self.settings_menu = True
                if self.button_touchscreen.is_clicked(mouse_pos) and self.settings_menu:
                    game.touchscreeen = not game.touchscreeen
                if self.button_back.is_clicked(mouse_pos) and self.settings_menu:
                    self.settings_menu = False
                    game.save_data()

    def updates(self):
        if game.touchscreeen and self.settings_menu:
            self.button_touchscreen.set_new_color(GREEN, LIGHT_GREEN)
        else:
            self.button_touchscreen.set_new_color(RED, LIGHT_RED)

    def draw(self):
        game.screen.fill(BACKGROUND_COLOR)
        self.button_start.draw()
        self.button_settings.draw()
        self.button_quit.draw()
        if self.settings_menu:
            self.button_touchscreen.draw()
            self.button_back.draw()
            #self.button_colors.draw()
        self.screen.blit(self.title_shadow, (385, 105))
        self.screen.blit(self.title, (380, 100))
        pygame.display.update()

    def run(self):
        game.load_data()
        while True:
            self.dt =  self.clock.tick(FPS) / 10
            self.events()
            self.updates()
            self.draw()

class Pause_Menu:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.button_back = Button(self.screen, 25, 250, 665, 120, BLACK, BLACK, 'Back', 'roboto', 90, BACKGROUND_COLOR)
        self.button_quit = Button(self.screen, 25, 400, 665, 120, BLACK, BLACK, 'Quit', 'roboto', 90, BACKGROUND_COLOR)

        self.overlay_menu = pygame.Surface(self.screen.get_size())
        self.overlay_menu.set_alpha(150)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_data()
                pygame.quit()
                quit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_back.is_clicked(mouse_pos):
                    self.paused = False
                if self.button_quit.is_clicked(mouse_pos):
                    main_menu.run()

    def draw(self):
        self.button_back.draw()
        self.button_quit.draw()
        pygame.display.update()

    def run(self):
        self.paused = True
        self.screen.blit(self.overlay_menu, (0, 0))
        while self.paused:
            self.events()
            self.draw()

class Button:

    def __init__(self, screen, x, y, w, h, button_color_active, button_color_inactive, text, font, size = 50, text_color = BLACK):
        self.screen = screen

        self.game_folder = path.dirname(__file__)
        self.font = path.join(self.game_folder, font + '.ttf')

        self.x, self.y, self.w, self.h = x, y, w, h
        self.button_color_active = button_color_active
        self.button_color_inactive = button_color_inactive

        self.text, self.size = text, size
        self.text_color = text_color

        self.button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.button_font = pygame.font.Font(self.font, self.size)
        self.label = self.button_font.render(self.text, 1, self.text_color)

    def draw(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.button_color_inactive, self.button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_color_active, self.button_rect)
        self.screen.blit(self.label, (self.x + 20, self.y + 5))

    def is_clicked(self, mouse_pos):
        return bool(self.button_rect.collidepoint(mouse_pos))

    def set_new_color(self, active_color, inactive_color):
        self.button_color_active = active_color
        self.button_color_inactive = inactive_color

class PlusMinusControl:

    def __init__(self, screen, x, y, variable = ''):
        self.screen = screen
        self.variable = variable
        self.variable_area_size = 240

        self.x = x
        self.y = y

        self.plus_button = pygame.Rect(x, y, 80, 80)
        self.variable_area = pygame.Rect(x + 80, y, self.variable_area_size, 80)
        self.minus_button = pygame.Rect(x + self.variable_area_size + 80, y, 80, 80)

        self.font = path.join('roboto-black.ttf')
        self.label_font = pygame.font.Font(self.font, 100)
        self.plus_label = self.label_font.render('+', 1, WHITE)
        self.minus_label = self.label_font.render('_', 1, WHITE)

        self.variable_font = pygame.font.Font(self.font, 70)
        self.label = self.variable_font.render(str(self.variable), 1, WHITE)

    def draw(self):
        if self.plus_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, LIGHT_BLACK, self.plus_button)
        else:
            pygame.draw.rect(self.screen, LIGHTER_BLACK, self.plus_button)

        if self.minus_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, LIGHT_BLACK, self.minus_button)
        else:
            pygame.draw.rect(self.screen, LIGHTER_BLACK, self.minus_button)

        pygame.draw.rect(self.screen, LIGHT_GRAY, self.variable_area)
        self.screen.blit(self.plus_label, (self.x + 12, self.y - 30))
        self.screen.blit(self.minus_label, (self.x + self.variable_area_size + 100, self.y - 70))
        self.screen.blit(self.label, (self.x + 130, self.y - 8))

        self.update()

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.plus_button.collidepoint(pygame.mouse.get_pos()) and self.variable < 100:
                self.variable += 1
            if self.minus_button.collidepoint(pygame.mouse.get_pos()) and self.variable > 0:
                self.variable -= 1
        self.label = self.variable_font.render(str(self.variable), 1, WHITE)

if __name__ == '__main__':

    game = Game()
    main_menu = Main_Menu()
    pause_menu = Pause_Menu()

    main_menu.run()
