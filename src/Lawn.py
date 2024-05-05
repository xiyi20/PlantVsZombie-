import Const
import pygame
import random
from Source import plant_ogg


class Lawn:
    def __init__(self, x, y, gameObj):
        self.plant = None
        self.game = gameObj
        self.x = x
        self.y = y
        self.row = self.game.rowRoad[self.y]
        self.rect = pygame.Rect(x, y, Const.LAWN_WIDTH, Const.LAWN_HEIGHT)

    def getpos(self):
        return self.x, self.y

    def planting(self, plant, pos):
        def setPlant():
            self.plant = plant(pos, self.game)
            self.game.Plants.append(self.plant)
            self.game.plantsInroad[self.row].append(self.plant)
            random.choice(plant_ogg).play()

        if not self.plant and plant.getalone():
            setPlant()
            return True
        elif self.plant and self.plant.update == plant:
            self.game.Plants.remove(self.plant)
            self.game.plantsInroad[self.row].remove(self.plant)
            setPlant()
            return True
        return False

    def Eradicate(self):
        if self.plant:
            self.game.Plants.remove(self.plant)
            self.game.plantsInroad[self.row].remove(self.plant)
            self.plant = None
