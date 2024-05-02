import Const
import pygame
import random


class Lawn:
    def __init__(self, x, y, gameobj):
        self.plant = None
        self.game = gameobj
        self.x = x
        self.y = y
        self.row = self.game.rowload[self.y]
        self.rect = pygame.Rect(x, y, Const.LAWN_WIDTH, Const.LAWN_HEIGHT)

    def getpos(self):
        return self.x, self.y

    def planting(self, plant, pos):
        def setplant():
            self.plant = plant(pos, self.game)
            self.game.Plants.append(self.plant)
            self.game.plantsInroad[self.row].append(self.plant)

        if not self.plant and plant.getalone():
            setplant()
            from Source import plant_ogg
            random.choice(plant_ogg).play()
            return True
        elif self.plant and self.plant.update == plant:
            self.game.Plants.remove(self.plant)
            self.game.plantsInroad[self.row].remove(self.plant)
            setplant()
            return True
        return False

    def displanting(self):
        if self.plant:
            self.game.Plants.remove(self.plant)
            self.game.plantsInroad[self.row].remove(self.plant)
            self.plant = None
