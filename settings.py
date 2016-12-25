import math

from os import path; game_folder = path.dirname(__file__)

TITLE = "AvoidEm!"
HEIGHT = 900
WIDTH = math.floor(HEIGHT * (16 / 9))

TILESIZE = 32
FPS = 60

BACKGROUND_COLOR = (237, 225, 192)
ENEMY_COLOR = (66, 64, 59)
ENEMY_COLOR_WALL = (124, 4, 94)
ENEMY_COLOR_MOVING = (226, 36, 36)
PLAYER_COLOR = (68, 133, 237)

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
LIGHT_BLACK = (30, 30, 30)
LIGHTER_BLACK = (50, 50, 50)

GRAY = (30, 30, 30)
LIGHT_GRAY = (60, 60, 60)

RED = (255, 0, 0)
LIGHT_RED = (255, 30, 30)

GREEN = (0, 200, 0)
LIGHT_GREEN = (30, 200, 30)
