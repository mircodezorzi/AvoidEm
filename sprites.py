import pygame
import random
import time

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
        self.image = pygame.Surface((TILESIZE * 1.5, TILESIZE * 1.50))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.x = random.uniform(0, WIDTH - TILESIZE)
        self.rect.x = self.x
        self.y = 0

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.all_sprites_list = []
            self.game.deaths += 1
            self.game.score = 0
            self.game.run()

        self.rect.y += (self.game.score + 1500) / 50

        for i in range(1, len(self.game.all_sprites_list)):
            try:
                print (len(self.game.all_sprites_list))
                if self.game.all_sprites_list[i].rect.y >= HEIGHT:
                    self.game.all_sprites_list.pop(1)
            except:
                pass

    def draw(self):
        pygame.draw.rect(self.game.screen, ENEMY_COLOR, self.rect)
