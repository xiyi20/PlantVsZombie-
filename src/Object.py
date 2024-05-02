import pygame
import Const
import random
from Source import objectType, screen, car_ogg, shoot_ogg


class Object:
    def __init__(self) -> None:
        self.y = None
        self.x = None
        self.images = None
        self.tick = 0
        self.image_index = 0
        self.distorypos = screen.get_width() - 30

    def draw(self):
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x, self.y + 20))
        self.tick += 1


class Car(Object):
    def __init__(self, x, y, gameobj) -> None:
        super().__init__()
        self.speed = 4
        self.x = x
        self.y = y
        self.game = gameobj
        self.active = False
        self.canplay = True
        self.image = objectType[0]
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())

    def draw(self):
        for zombie in self.game.zombiesInroad[self.game.rowload[self.y - 35]]:
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
        if self.x >= self.distorypos:
            self.game.Cars.remove(self)


class Sun(Object):
    def __init__(self, val, pos, gameobj, falling=False):
        super().__init__()
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.cury = 50
        self.targety = pos[1]
        self.game = gameobj
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
            if self.falling and self.tick % 2 == 0 and self.cury < self.targety:
                self.cury += 1.5
                self.y = self.cury
            else:
                self.y = self.cury if self.falling else self.targety
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
        self.game.playSun += self.val
        self.game.Suns.remove(self)


class Peas(Object):
    def __init__(self, x, y, gameobj, damm=20) -> None:
        super().__init__()
        self.x = x + 35
        self.y = y + 5
        self.game = gameobj
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
        for zombie in self.game.zombiesInroad[self.game.rowload[self.y - 5]]:
            if zombie.rect.colliderect(self.rect) and zombie.blood > 0:
                zombie.blood -= self.damm
                random.choice(zombie.hiteffect).play()
                self.game.Peass.remove(self)
                if zombie.blood <= 0:
                    zombie.dead = 1
                break
        if self.x >= self.distorypos and self in self.game.Peass:
            self.game.Peass.remove(self)
