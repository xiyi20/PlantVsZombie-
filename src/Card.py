import pygame
import Const
from Source import objectType, getImageSource, priceText, screen


class Card:
    def __init__(self, img, plant, price, cooltime, gameObj, x, y=7) -> None:
        self.rect = None
        self.img = img
        self.plant = plant
        self.selected = None
        self.active = False
        self.price = str(price)
        self.coolimage = objectType[11]
        self.cooltime = str(cooltime)
        self.interval = Const.CARD_HEIGHT / cooltime
        self.curTime = '0'
        self.game = gameObj
        self.x = x
        self.y = y

    def draw(self):
        self.rect = pygame.Rect(
            self.x, self.y, Const.CARD_WIDTH, Const.CARD_HEIGHT)
        plantcard = pygame.transform.scale(getImageSource(
            'img/widget/卡槽.png'), (Const.CARD_WIDTH, Const.CARD_HEIGHT))
        plantimage = pygame.transform.scale(getImageSource(
            self.img), (Const.CARD_IMG_SIZE, Const.CARD_IMG_SIZE))
        screen.blit(plantcard, (self.x, self.y))
        screen.blit(plantimage, (self.x + 7, self.y + 15))
        color = (255, 0, 0) if int(
            self.price) > self.game.playSun and not self.game.selectFlag else (0, 0, 0)
        screen.blit(priceText.render(self.price, True, color),
                    (self.x + 2, self.y + 55))
        if self.selected:
            screen.blit(self.selected, (self.x, self.y + 1))
        if self.curTime != '0':
            screen.blit(pygame.transform.scale(self.coolimage, (50, int(self.curTime) * self.interval)),
                        (self.x, self.y))
            self.curTime = str(int(self.curTime) - 1)
