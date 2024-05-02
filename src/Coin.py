import pygame
import Const
from RWconfig import rwconfig
from Source import objectType, coinfall_ogg, screen, diamondfall_ogg, coinpick_ogg, diamondpick_ogg

class Coin:
    def __init__(self, x, y, gameobj, type=0) -> None:
        self.x = x
        self.y = y
        self.val = 50
        self.pick = False
        self.first = True
        self.xspeed = 0
        self.yspeed = 0
        self.game = gameobj
        self.tick = 0
        self.fall_ogg = coinfall_ogg if type == 0 else diamondfall_ogg
        self.pick_ogg = coinpick_ogg
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
                self.xspeed = (10 - self.x) / Const.COIN_SPEED
                self.yspeed = (580 - self.y) / Const.COIN_SPEED
            self.x += self.xspeed
            self.y += self.yspeed
            if self.rect.colliderect(self.endRect):
                self.pickup()
        self.tick += 1
        screen.blit(self.image, (self.x, self.y))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.tick == Const.COIN_LIFE:
            self.game.Coins.remove(self)

    def pickup(self):
        self.game.money += self.val
        rwconfig.wconfig('user', 'money', self.game.money)
        self.game.Coins.remove(self)


class SilverCoin(Coin):
    def __init__(self, x, y, gameobj) -> None:
        super().__init__(x, y, gameobj)


class GoldCoin(Coin):
    def __init__(self, x, y, gameobj) -> None:
        super().__init__(x, y, gameobj)
        self.val = 100
        self.image = objectType[13]


class Diamond(Coin):
    def __init__(self, x, y, gameobj) -> None:
        super().__init__(x, y, gameobj, 1)
        self.val = 300
        self.fall_ogg = diamondfall_ogg
        self.pick_ogg = diamondpick_ogg
        self.image = objectType[14]
