import pygame
import random
import time

from pygame.locals import *
from settings import *

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
        self.vx = 0
        self.vy = 0
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 7

    def events(self):
        if self.game.touchscreeen:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.x = mouse_pos[0] - TILESIZE / 2
            self.rect.y = mouse_pos[1] - TILESIZE / 2
        else:
            keys = pygame.key.get_pressed()
            self.vy = 0
            self.vx = 0
            if keys[K_UP] or keys[K_w]:
                self.vy = -self.speed
            if keys[K_DOWN] or keys[K_s]:
                self.vy = self.speed
            if keys[K_LEFT] or keys[K_a]:
                self.vx = -self.speed
            if keys[K_RIGHT] or keys[K_d]:
                self.vx = self.speed

            self.rect.x += self.vx * self.game.dt
            self.rect.y += self.vy * self.game.dt

    def update(self):
        self.events()
        self.rect.x = min(self.rect.x, WIDTH - TILESIZE)
        self.rect.y = min(self.rect.y, HEIGHT- TILESIZE)
        self.rect.x = max(self.rect.x, 0)
        self.rect.y = max(self.rect.y, 0)

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
            self.game.deaths += 1
            self.game.score = 0
            self.game.run()
        if self.rect.y >= HEIGHT:
            self.kill()

        self.rect.y += (self.game.score + 1500) / 300 * self.game.dt


class EnemyWall(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((WIDTH / 2, 50))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.x = int(random.uniform(0, WIDTH))
        self.rect.x = self.x
        self.y = 0

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.deaths += 1
            self.game.score = 0
            self.game.run()
        if self.rect.y >= HEIGHT:
            self.kill()

        self.rect.y += (self.game.score + 1500) / 300 * self.game.dt


class EnemyMoving(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE * 1.5, TILESIZE * 1.50))
        self.image.fill(ENEMY_COLOR_MOVING)
        self.rect = self.image.get_rect()
        self.y = 0

        if random.choice([True, False]):
            self.dir = 'right'
            self.x = 0
        else:
            self.dir = 'left'
            self.x = WIDTH

        self.rect.x = self.x

        self.speed = random.uniform(1, 10)

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.deaths += 1
            self.game.score = 0
            self.game.run()
        if self.rect.y >= HEIGHT or self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()

        self.rect.y += (self.game.score + 1500) / 300 * self.game.dt

        if self.dir == 'right':
            self.rect.x += self.speed * self.game.dt
        if self.dir == 'left':
            self.rect.x -= self.speed * self.game.dt
