import pygame
import random

from pygame.locals import *
from settings import *
from main import *

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE + 10, TILESIZE + 10))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.x = random.uniform(0, WIDTH - TILESIZE)
        self.rect.x = self.x
        self.y = 0

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.deaths += 1
            self.game.score = 0
            self.game.run()
        self.rect.y += (self.game.score + 500) / 50
        if self.rect.y >= HEIGHT:
            self.image.delete()
