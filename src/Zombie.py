import pygame
import Const
import math
import random
from Coin import SilverCoin, GoldCoin, Diamond
from Source import objectType, zombieType, screen, splat_ogg, zombie_falling_ogg, ironHit_ogg


class Zombie:
    def __init__(self, y, zombie, gameobj, type: int) -> None:
        self.y = None
        self.x = Const.ZOMBIE_X
        self.xoffset = 10
        self.yoffset = 20
        self.speed = 0.25
        self.blood = Const.NOMALZOMBIE_BLOOD
        self.sunval = 0
        self.game = gameobj
        self.damm = 100
        self.tick = 0
        self.dead = 0
        self.deadanimation = True
        self.deadindex = 0
        self.row = gameobj.loadzombies[y]
        self.eating = None
        self.eat_count = 0
        self.state = 'walk'
        self.fps = 4
        self.rect = None
        self.hiteffect = splat_ogg
        self.laststate = None
        self.game.zombiesInroad[self.row].append(zombie)
        self.images = None
        self.image_index = None
        self.type = zombieType[type]
        self.dieimages = objectType[7]
        self.head = objectType[9]

    def draw(self):
        if self.dead == 0:
            self.state = 'eat' if self.eating else 'walk'
            for plant in self.game.plantsInroad[self.row]:
                if self.rect.colliderect(plant.rect):
                    self.eating = plant
                    self.state = 'eat'
                    self.resetstate()
                    break
            if self.state == 'walk':
                self.images = self.type[0]
                self.x -= self.speed
                self.rect = pygame.Rect(
                    self.x + 100, self.y, 20, self.images[0].get_height())
            else:
                self.images = self.type[1]
                if self.game.lawns[self.eating.row - 1][self.eating.col - 1].plant:
                    if self.eat_count % 60 == 0:
                        if self.eating.hurt(self.damm):
                            self.state = 'walk'
                            self.resetstate()
                            self.eating = None
                    self.eat_count += 1
                else:
                    self.eat_count = 60
                    self.state = 'walk'
                    self.resetstate()
                    self.eating = None
            if self.tick % self.fps == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            self.tick += 1
            screen.blit(self.images[self.image_index],
                        (self.x + self.xoffset, self.y + self.yoffset))
        else:
            if self.deadanimation:
                self.dieanimation()
            else:
                self.distory()

    def resetstate(self):
        if self.laststate != self.state:
            self.image_index = 0
            self.laststate = self.state

    def dieanimation(self):
        if self.deadindex < len(self.dieimages):
            curindex = math.floor(self.deadindex)
            bodyframe = self.dieimages[curindex]
            if self.dead == 1:
                headframe = self.head[math.floor(self.deadindex + 0.05)]
                screen.blit(headframe, (self.x + 60, self.y + 5))
                screen.blit(bodyframe, (self.x + 10, self.y + 20))
            elif self.dead == 2:
                screen.blit(bodyframe, (self.x + 70, self.y + 55))
            self.deadindex += 0.15
        else:
            self.distory()
            random.choice(zombie_falling_ogg).play()

    def distory(self):
        from Object import Sun
        choose = random.randrange(100)
        if 0 < choose <= 10:
            money = None
            if 5 < choose <= 10:
                money = SilverCoin(self.x + 60, self.y + 120, self.game)
            elif 3 < choose <= 5:
                money = GoldCoin(self.x + 60, self.y + 120, self.game)
            elif 0 < choose <= 3:
                money = Diamond(self.x + 60, self.y + 120, self.game)
            self.game.Coins.append(money)
        if self.sunval != 0:
            self.game.Suns.append(
                Sun(self.sunval, (self.x + 45, self.y + 80), self.game))
        self.game.Zombies.remove(self)
        self.game.zombiesInroad[self.game.loadzombies[self.y]].remove(self)
        self.game.curScore += 1
        self.game.wonpos = [self.x + 30, self.y + 90]


class NomalZ(Zombie):
    def __init__(self, y, gameobj) -> None:
        super().__init__(y, self, gameobj, 0)
        self.y = y
        self.game = gameobj
        self.image_index = 0
        self.fps = 4.5
        self.rect = pygame.Rect(self.x + 100, self.y, 20, 48)


class RoadZ(Zombie):
    def __init__(self, y, gameobj) -> None:
        super().__init__(y, self, gameobj, 1)
        self.y = y
        self.game = gameobj
        self.blood = Const.ROADZOMBIE_BLOOD
        self.fps = 5.5
        self.image_index = 0
        self.rect = pygame.Rect(self.x + 100, self.y, 20, 48)


class IronBZ(Zombie):
    def __init__(self, y, gameobj) -> None:
        super().__init__(y, self, gameobj, 2)
        self.y = y
        self.game = gameobj
        self.blood = Const.IRONZOMBIE_BLOOD
        self.fps = 5.5
        self.image_index = 0
        self.hiteffect = ironHit_ogg
        self.rect = pygame.Rect(self.x + 100, self.y, 20, 48)


class RugbyZ(Zombie):
    def __init__(self, y, gameobj) -> None:
        super().__init__(y, self, gameobj, 3)
        self.y = y
        self.blood = Const.RUGBYZOMBIE_BLOOD
        self.speed = 0.5
        self.yoffset = 0
        self.game = gameobj
        self.image_index = 0
        self.fps = 4.5
        self.dieimages = objectType[16]
        self.rect = pygame.Rect(self.x + 100, self.y, 20, 48)
