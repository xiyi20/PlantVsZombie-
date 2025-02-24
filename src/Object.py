import math
import random

import pygame

from src import Const
from src.Source import objectType, screen, car_ogg, shoot_ogg


class Object:
    def __init__(self) -> None:
        self.y = None
        self.x = None
        self.images = None
        self.tick = 0
        self.image_index = 0
        self.destroyPos = screen.get_width() - 30

    def draw(self):
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x, self.y + 20))
        self.tick += 1


class Car(Object):
    def __init__(self, x, y, gameObj) -> None:
        super().__init__()
        self.speed = 4
        self.x = x
        self.y = y
        self.game = gameObj
        self.active = False
        self.canplay = True
        self.image = objectType[0]
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())

    def draw(self):
        for zombie in self.game.zombiesInroad[self.game.rowRoad[self.y - 35]]:
            if self.rect.colliderect(zombie.rect):
                zombie.dead = 1
                self.active = True
        if self.active:
            self.x += self.speed
            if self.canplay:
                car_ogg.play()
                self.canplay = False
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())
        screen.blit(self.image, (self.x, self.y))
        if self.x >= self.destroyPos:
            self.game.Cars.remove(self)


class Sun(Object):
    def __init__(self, val, pos, gameObj, falling=False):
        super().__init__()
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.curY = 50
        self.targetY = pos[1]
        self.game = gameObj
        self.falling = falling
        self.image_index = 0
        self.life = Const.SUN_LIFE
        self.tick = 0
        self.pick = False
        self.images = objectType[1]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.endRect = pygame.Rect(0, 0, 20, 20)

    def draw(self):
        if not self.pick:
            if self.falling and self.tick % 2 == 0 and self.curY < self.targetY:
                self.curY += 1.5
                self.y = self.curY
            else:
                self.y = self.curY if self.falling else self.targetY
        else:
            self.x += (-self.x) / Const.SUN_SPEED
            self.y += (-10 - self.y) / Const.SUN_SPEED
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        if self.rect.colliderect(self.endRect):
            self.pickup()
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.tick += 1
        if self.tick == self.life:
            self.game.Suns.remove(self)
        screen.blit(self.images[self.image_index], (self.x, self.y + 20))

    def pickup(self):
        self.game.curSun += self.val
        self.game.Suns.remove(self)


class Peas(Object):
    def __init__(self, x, y, gameObj, damm=20) -> None:
        super().__init__()
        self.x = x + 35
        self.y = y + 5
        self.game = gameObj
        self.damm = damm
        self.speed = Const.PEAS_SPEED
        self.images = objectType[2]
        self.rect = pygame.Rect(self.x, self.y, 23, 10)
        random.choice(shoot_ogg).play()

    def draw(self):
        if self.tick % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x, self.y))
        self.tick += 1
        self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), 10)
        for zombie in self.game.zombiesInroad[self.game.rowRoad[self.y - 5]]:
            if self.attack(zombie): break
        if self.x >= self.destroyPos and self in self.game.Peas:
            self.game.Peas.remove(self)

    def attack(self, zombie):
        if zombie.rect.colliderect(self.rect) and zombie.blood > 0:
            zombie.blood -= self.damm
            random.choice(zombie.hitEffect).play()
            self.game.Peas.remove(self)
            if zombie.blood <= 0:
                zombie.dead = 1
            return True
        return False


class TrackPea(Peas):
    def __init__(self, x, y, gameObj, damm=20) -> None:
        super().__init__(x, y, gameObj, damm)
        self.speed = 150
        self.sina, self.cosa = 1, 1

    def draw(self):
        if self.tick % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x, self.y))
        self.tick += 1
        if self.game.Zombies:
            target = self.game.Zombies[0]
            tx = target.x + 80
            ty = target.y + 85
            distance = math.sqrt((tx - self.x) ** 2 + (ty - self.y) ** 2)
            self.sina = (tx - self.x) / distance
            self.cosa = (ty - self.y) / distance
        self.x += self.speed / 60 * self.sina
        self.y += self.speed / 60 * self.cosa
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), 10)
        for zombie in self.game.Zombies:
            if self.attack(zombie): break
        if (self.x >= self.destroyPos or self.y < 0 or self.y > 600) and self in self.game.Peas:
            self.game.Peas.remove(self)
