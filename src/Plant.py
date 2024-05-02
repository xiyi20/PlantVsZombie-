import pygame
import random
import Const
import math
from Source import objectType, plantType, getImageSource, getSoundEffect, screen, zombieEating_ogg, plantDead_ogg, potatoActive_ogg, potatoBoom_ogg, cherryBoom_ogg


class Plant:
    sunprice = 0
    cooling = 450
    alone = True
    image = None

    def __init__(self, col, row, gameobj) -> None:
        self.game = gameobj
        self.y = None
        self.x = None
        self.images = None
        self.image_index = None
        self.blood = 300
        self.col = gameobj.colload[col]
        self.row = gameobj.rowload[row]
        self.update = None
        self.rect = None
        self.tick = 0
        self.interval = 80

    @classmethod
    def getprice(cls):
        return cls.sunprice

    @classmethod
    def getimage(cls):
        return getImageSource(cls.image)

    @classmethod
    def getcooltime(cls):
        return cls.cooling

    @classmethod
    def getalone(cls):
        return cls.alone

    def shot(self):
        pass

    def switchimg(self):
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x + 13, self.y + 5))
        self.tick += 1

    def draw(self):
        self.switchimg()

    def hurt(self, damm):
        self.blood -= damm
        random.choice(zombieEating_ogg).play()
        if self.blood < 0:
            self.game.lawns[self.row - 1][self.col - 1].displanting()
            plantDead_ogg.play()
            return True


class SunFlower(Plant):
    sunprice = Const.SUNFLOWER_PRICE
    image = 'img/向日葵/0.png'

    def __init__(self, pos, gameobj):
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.image_index = 0
        self.images = plantType[0]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.suntime = random.randint(180, 720)

    def draw(self):
        from Object import Sun
        self.switchimg()
        self.suntime -= 1
        if self.suntime == 0:
            self.game.Suns.append(
                Sun(50, (self.x + 44, self.y + 25), self.game))
            self.suntime = random.randint(1200, 1800)


class PeaShooter(Plant):
    sunprice = Const.PEASHOOTER_PRICE
    image = 'img/豌豆射手/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = gameobj.rowload[self.y]
        self.damm = 20
        self.image_index = 0
        self.images = plantType[1]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())

    def shot(self):
        from Object import Peas
        if self.game.zombiesInroad[self.row]:
            for zombie in self.game.zombiesInroad[self.row]:
                if self.x - 30 <= zombie.x <= 700:
                    if self.tick % self.interval == 0:
                        self.game.Peass.append(
                            Peas(self.x, self.y, self.game, self.damm))
                        break


class Repeater(Plant):
    sunprice = Const.REPEATER_PRICE
    image = 'img/双重射手/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = self.game.rowload[self.y]
        self.damm = 20
        self.update = GatlingPea
        self.image_index = 0
        self.images = plantType[2]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())

    def shot(self):
        from Object import Peas
        if self.game.zombiesInroad[self.row]:
            for zombie in self.game.zombiesInroad[self.row]:
                if self.x - 30 <= zombie.x <= 700:
                    if self.tick % self.interval in [0, 10]:
                        self.game.Peass.append(
                            Peas(self.x, self.y, self.game, self.damm))
                        break


class GatlingPea(Plant):
    sunprice = Const.GATLINGPEA_PRICE
    cooling = 3000
    alone = False
    image = 'img/机枪射手/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = self.game.rowload[self.y]
        self.damm = 20
        self.image_index = 0
        self.images = plantType[9]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())

    def draw(self):
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x + 13, self.y - 5))
        self.tick += 1

    def shot(self):
        from Object import Peas
        if self.game.zombiesInroad[self.row]:
            for zombie in self.game.zombiesInroad[self.row]:
                if self.x - 30 <= zombie.x <= 700:
                    if self.tick % self.interval in [0, 10, 20, 30]:
                        self.game.Peass.append(
                            Peas(self.x, self.y, self.game, self.damm))
                        break


class SpicyChili(Plant):
    sunprice = Const.SPICYCHILI_PRICE
    cooling = 3000
    image = 'img/火爆辣椒/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = self.game.rowload[self.y]
        self.col = self.game.colload[self.x]
        self.damm = 1800
        self.booming = False
        self.spicy_ogg = getSoundEffect('aud/jalapeno.ogg')
        self.image_index = 0
        self.images = plantType[3]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.boom_index = 0
        self.boomimages = plantType[4]
        self.boomRect = pygame.Rect(
            50, self.y, 730, self.images[0].get_height())

    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(
                self.image_index)], (self.x + 10, self.y - 5))
            self.image_index += 0.25
            if self.image_index == len(self.images):
                self.booming = True
                self.spicy_ogg.play()
                for zombie in self.game.zombiesInroad[self.row]:
                    if zombie.blood > 0:
                        zombie.blood -= self.damm
                        if zombie.blood <= 0:
                            zombie.dieimages = objectType[8]
                            zombie.dead = 2
        else:
            screen.blit(self.boomimages[math.floor(
                self.boom_index)], (25, self.y - 40))
            self.boom_index += 0.25
            if self.boom_index == len(self.boomimages):
                self.game.lawns[self.row - 1][self.col - 1].displanting()


class NutsWall(Plant):
    sunprice = Const.NUTSWALL_PRICE
    cooling = 1800
    image = 'img/坚果/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = gameobj.rowload[self.y]
        self.col = gameobj.colload[self.x]
        self.image_index = 0
        self.blood = 5000
        self.images = plantType[5]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())


class PotatoMine(Plant):
    sunprice = Const.POTATOMINE_PRICE
    cooling = 1800
    image = 'img/土豆地雷/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0] + 30
        self.y = pos[1] + 45
        self.game = gameobj
        self.damm = 1800
        self.row = gameobj.rowload[pos[1]]
        self.col = gameobj.colload[pos[0]]
        self.image_index = 0
        self.active = False
        self.booming = False
        self.boomtime = 0
        self.boom1 = objectType[3]
        self.boom2 = objectType[4]
        self.images0 = objectType[5]
        self.images1 = plantType[6]
        self.images = self.images0
        self.rect = pygame.Rect(
            pos[0], pos[1], self.images1[0].get_width(), self.images1[0].get_height())

    def draw(self):
        willdie = []
        if not self.booming:
            if self.tick % 13 == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            if self.tick == 900:
                self.active = True
                potatoActive_ogg.play()
                self.x, self.y = self.x - 18, self.y - 20
                self.images = self.images1
            screen.blit(self.images[self.image_index], (self.x, self.y))
            self.tick += 1
            for zombie in self.game.zombiesInroad[self.row]:
                if self.rect.colliderect(zombie.rect) and self.active:
                    self.booming = True
                    potatoBoom_ogg.play()
                    for deadzombie in self.game.zombiesInroad[self.row]:
                        if -45 < deadzombie.x - self.x < 45:
                            willdie.append(deadzombie)
                    for i in willdie:
                        if i.blood > 0:
                            i.blood -= self.damm
                            if i.blood <= 0:
                                i.deadanimation = False
                                i.dead = 1
                    break
        else:
            if self.boomtime <= 60:
                screen.blits([
                    (self.boom2, (self.x - 30, self.y - 25)),
                    (self.boom1, (self.x - 45, self.y - 55))
                ])
                self.boomtime += 1
            else:
                self.game.lawns[self.row - 1][self.col - 1].displanting()


class CherryBomb(Plant):
    sunprice = Const.CHERRYBOMB_PRICE
    cooling = 3000
    image = 'img/樱桃炸弹/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = self.game.rowload[self.y]
        self.col = self.game.colload[self.x]
        self.damm = 1800
        self.booming = False
        self.image_index = 0
        self.images = plantType[7]
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.boomtime = 0
        self.boomimage = objectType[6]
        self.boomRect = pygame.Rect(self.x - 70, self.y - 30, 200, 130)

    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(
                self.image_index)], (self.x - 10, self.y - 5))
            self.image_index += 0.25
            if self.image_index == len(self.images):
                self.booming = True
                cherryBoom_ogg.play()
                for zombie in self.game.Zombies:
                    if self.boomRect.colliderect(zombie.rect) and zombie.blood > 0:
                        zombie.blood -= self.damm
                        if zombie.blood <= 0:
                            zombie.dieimages = objectType[8]
                            zombie.dead = 2
        else:
            if self.boomtime <= 30:
                screen.blit(self.boomimage, (self.x - 70, self.y - 30))
                self.boomtime += 1
            else:
                self.game.lawns[self.row - 1][self.col - 1].displanting()


class Torchwood(Plant):
    sunprice = Const.TORCHWOOD_PRICE
    image = 'img/火炬树桩/0.png'

    def __init__(self, pos, gameobj) -> None:
        super().__init__(pos[0], pos[1], gameobj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameobj
        self.row = gameobj.rowload[self.y]
        self.col = gameobj.colload[self.x]
        self.image_index = 0
        self.images = plantType[8]
        self.rect = pygame.Rect(self.x + 20, self.y, 55, 80)

    def draw(self):
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x + 16, self.y - 10))
        self.tick += 1
        for peas in self.game.Peass:
            if self.rect.colliderect(peas.rect):
                peas.damm == 65
                peas.images = objectType[17]
