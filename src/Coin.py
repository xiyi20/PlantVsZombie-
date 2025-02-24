import pygame

from src import Const
from src.RwConfig import rwConfig
from src.Source import objectType, coinFall_ogg, screen, diamondFall_ogg, coinPick_ogg, diamondPick_ogg


class Coin:
    def __init__(self, x, y, gameObj, coinType=0) -> None:
        self.x = x
        self.y = y
        self.val = 50
        self.pick = False
        self.first = True
        self.xSpeed = 0
        self.ySpeed = 0
        self.game = gameObj
        self.tick = 0
        self.fall_ogg = coinFall_ogg if coinType == 0 else diamondFall_ogg
        self.pick_ogg = coinPick_ogg
        self.image = objectType[12]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.endRect = pygame.Rect(48, 580, 20, 20)
        if self.fall_ogg:
            self.fall_ogg.play()

    def draw(self):
        if self.pick:
            if self.first:
                self.first = False
                if self.pick_ogg:
                    self.pick_ogg.play()
                self.xSpeed = (10 - self.x) / Const.COIN_SPEED
                self.ySpeed = (580 - self.y) / Const.COIN_SPEED
            self.x += self.xSpeed
            self.y += self.ySpeed
            if self.rect.colliderect(self.endRect):
                self.pickup()
        self.tick += 1
        screen.blit(self.image, (self.x, self.y))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.tick == Const.COIN_LIFE:
            self.game.Coins.remove(self)

    def pickup(self):
        self.game.money += self.val
        rwConfig.wConfig('user', 'money', self.game.money)
        self.game.Coins.remove(self)


class SilverCoin(Coin):
    def __init__(self, x, y, gameObj) -> None:
        super().__init__(x, y, gameObj)


class GoldCoin(Coin):
    def __init__(self, x, y, gameObj) -> None:
        super().__init__(x, y, gameObj)
        self.val = 100
        self.image = objectType[13]


class Diamond(Coin):
    def __init__(self, x, y, gameObj) -> None:
        super().__init__(x, y, gameObj, 1)
        self.val = 300
        self.fall_ogg = diamondFall_ogg
        self.pick_ogg = diamondPick_ogg
        self.image = objectType[14]
