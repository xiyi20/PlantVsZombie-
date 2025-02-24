import pygame

from src import Const
from src.Source import objectType, getImageSource, priceText, screen


class Card:
    def __init__(self, img, plant, price, cooldown, gameObj, x, y=7) -> None:
        self.rect = None
        self.img = img
        self.plant = plant
        self.selected = None
        self.active = False
        self.price = str(price)
        self.coolImage = objectType[11]
        self.coolTime = str(cooldown)
        self.interval = Const.CARD_HEIGHT / cooldown
        self.curTime = '0'
        self.game = gameObj
        self.x = x
        self.y = y

    def draw(self):
        self.rect = pygame.Rect(
            self.x, self.y, Const.CARD_WIDTH, Const.CARD_HEIGHT)
        plantCard = pygame.transform.scale(getImageSource(
            'img/widget/卡槽.png'), (Const.CARD_WIDTH, Const.CARD_HEIGHT))
        plantImage = pygame.transform.scale(getImageSource(
            self.img), (Const.CARD_IMG_SIZE, Const.CARD_IMG_SIZE))
        screen.blit(plantCard, (self.x, self.y))
        screen.blit(plantImage, (self.x + 4, self.y + 12))
        color = (255, 0, 0) if int(
            self.price) > self.game.curSun and not self.game.selectFlag else (0, 0, 0)
        screen.blit(priceText.render(self.price, True, color),
                    (self.x + 2, self.y + 55))
        if self.selected:
            screen.blit(self.selected, (self.x, self.y + 1))
        if self.curTime != '0':
            screen.blit(pygame.transform.scale(self.coolImage, (50, int(self.curTime) * self.interval)),
                        (self.x, self.y))
            self.curTime = str(int(self.curTime) - 1)
