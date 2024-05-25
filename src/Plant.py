import pygame
import random
import Const
import math
from Object import TrackPea, Sun, Peas
from Source import objectType, plantType, getImageSource, getSoundEffect, screen, zombieEating_ogg, plantDead_ogg, potatoActive_ogg, potatoBoom_ogg, cherryBoom_ogg


class Plant:
    sunPrice = 0
    cooling = 450
    alone = True
    image = None
    name = None

    def __init__(self, col, row, gameObj) -> None:
        self.game = gameObj
        self.x = col
        self.y = row
        self.xOffset = 13
        self.yOffset = 5
        self.fps = 4
        self.images = None
        self.image_index = None
        self.blood = 300
        self.col = gameObj.colRoad[col]
        self.row = gameObj.rowRoad[row]
        self.update = None
        self.rect = pygame.Rect(self.x, self.y, 65, 75)
        self.tick = 0
        self.interval = 80

    @classmethod
    def getname(cls):
        return cls.name

    @classmethod
    def getprice(cls):
        return cls.sunPrice

    @classmethod
    def getimage(cls, path: bool = 0):
        if path:
            return cls.image
        else:
            return getImageSource(cls.image)

    @classmethod
    def getcooltime(cls):
        return cls.cooling

    @classmethod
    def getalone(cls):
        return cls.alone

    def check(self):
        zombies = self.game.zombiesInroad[self.row]
        if zombies:
            for zombie in zombies:
                if self.x - 30 <= zombie.x <= 700:
                    return True
        return False

    def action(self):
        pass

    def switchimg(self):
        if self.tick % self.fps == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        screen.blit(self.images[self.image_index],
                    (self.x + self.xOffset, self.y + self.yOffset))
        self.tick += 1

    def draw(self):
        self.switchimg()
        self.action()

    def hurt(self, damm):
        self.blood -= damm
        random.choice(zombieEating_ogg).play()
        if self.blood < 0:
            self.game.lawns[self.row - 1][self.col - 1].Eradicate()
            plantDead_ogg.play()
            return True


class SunFlower(Plant):
    sunPrice = Const.SUNFLOWER_PRICE
    image = 'img/向日葵/0.png'
    name = '向日葵'

    def __init__(self, pos, gameObj):
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.yOffset = 3
        self.game = gameObj
        self.image_index = 0
        self.images = plantType[0]
        self.interval = random.randint(180, 720)

    def action(self):
        self.interval -= 1
        if self.interval == 0:
            self.game.Suns.append(
                Sun(50, (self.x + 44, self.y + 25), self.game))
            self.interval = random.randint(1200, 1800)


class PeaShooter(Plant):
    sunPrice = Const.PEASHOOTER_PRICE
    image = 'img/豌豆射手/0.png'
    name = '豌豆射手'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameObj
        self.row = gameObj.rowRoad[self.y]
        self.damm = 20
        self.image_index = 0
        self.images = plantType[1]

    def action(self):
        if self.check() and self.tick % self.interval == 0:
            self.game.Peas.append(
                Peas(self.x, self.y, self.game, self.damm))


class Repeater(Plant):
    sunPrice = Const.REPEATER_PRICE
    image = 'img/双重射手/0.png'
    name = '双发射手'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameObj
        self.row = self.game.rowRoad[self.y]
        self.damm = 20
        self.update = GatlingPea
        self.image_index = 0
        self.images = plantType[2]

    def action(self):
        if self.check() and self.tick % self.interval in [0, 10]:
            self.game.Peas.append(
                Peas(self.x, self.y, self.game, self.damm))


class GatlingPea(Plant):
    sunPrice = Const.GATLINGPEA_PRICE
    cooling = 3000
    alone = False
    image = 'img/机枪射手/0.png'
    name = '机枪射手'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.xOffset = 13
        self.yOffset = -5
        self.game = gameObj
        self.row = self.game.rowRoad[self.y]
        self.damm = 20
        self.image_index = 0
        self.images = plantType[9]

    def action(self):
        if self.check() and self.tick % self.interval in [0, 10, 20, 30]:
            self.game.Peas.append(
                Peas(self.x, self.y, self.game, self.damm))


class SpicyChili(Plant):
    sunPrice = Const.SPICYCHILI_PRICE
    cooling = 3000
    image = 'img/火爆辣椒/0.png'
    name = '火爆辣椒'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameObj
        self.row = self.game.rowRoad[self.y]
        self.col = self.game.colRoad[self.x]
        self.damm = 1800
        self.booming = False
        self.spicy_ogg = getSoundEffect('aud/jalapeno.ogg')
        self.image_index = 0
        self.images = plantType[3]
        self.boom_index = 0
        self.boomimages = plantType[4]
        self.boomRect = pygame.Rect(
            50, self.y, 730, self.images[0].get_height())

    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(
                self.image_index)], (self.x + 10, self.y-15))
            self.image_index += 0.25
            if self.image_index == len(self.images):
                self.booming = True
                self.spicy_ogg.play()
                for zombie in self.game.zombiesInroad[self.row]:
                    if zombie.blood > 0:
                        zombie.blood -= self.damm
                        if zombie.blood <= 0:
                            zombie.dieImages = objectType[8]
                            zombie.dead = 2
        else:
            screen.blit(self.boomimages[math.floor(
                self.boom_index)], (25, self.y - 40))
            self.boom_index += 0.25
            if self.boom_index == len(self.boomimages):
                self.game.lawns[self.row - 1][self.col - 1].Eradicate()


class NutsWall(Plant):
    sunPrice = Const.NUTSWALL_PRICE
    cooling = 1800
    image = 'img/坚果/0.png'
    name = '坚果'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameObj
        self.row = gameObj.rowRoad[self.y]
        self.col = gameObj.colRoad[self.x]
        self.image_index = 0
        self.blood = 5000
        self.images = plantType[5]


class PotatoMine(Plant):
    sunPrice = Const.POTATOMINE_PRICE
    cooling = 1800
    image = 'img/土豆地雷/0.png'
    name = '土豆地雷'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0] + 30
        self.y = pos[1] + 45
        self.game = gameObj
        self.damm = 1800
        self.row = gameObj.rowRoad[pos[1]]
        self.col = gameObj.colRoad[pos[0]]
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
                                i.deadAnimation = False
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
                self.game.lawns[self.row - 1][self.col - 1].Eradicate()


class CherryBomb(Plant):
    sunPrice = Const.CHERRYBOMB_PRICE
    cooling = 3000
    image = 'img/樱桃炸弹/0.png'
    name = '樱桃炸弹'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.game = gameObj
        self.row = self.game.rowRoad[self.y]
        self.col = self.game.colRoad[self.x]
        self.damm = 1800
        self.booming = False
        self.image_index = 0
        self.images = plantType[7]
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
                            zombie.dieImages = objectType[8]
                            zombie.dead = 2
        else:
            if self.boomtime <= 30:
                screen.blit(self.boomimage, (self.x - 70, self.y - 30))
                self.boomtime += 1
            else:
                self.game.lawns[self.row - 1][self.col - 1].Eradicate()


class Torchwood(Plant):
    sunPrice = Const.TORCHWOOD_PRICE
    image = 'img/火炬树桩/0.png'
    name = '火炬树桩'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.x = pos[0]
        self.y = pos[1]
        self.xOffset = 16
        self.yOffset = -10
        self.game = gameObj
        self.row = gameObj.rowRoad[self.y]
        self.col = gameObj.colRoad[self.x]
        self.image_index = 0
        self.images = plantType[8]
        self.rect = pygame.Rect(self.x + 20, self.y, 55, 80)

    def action(self):
        for pea in self.game.Peas:
            if self.rect.colliderect(pea.rect):
                pea.damm == 65
                pea.images = objectType[17]


class Catnip(Plant):
    sunPrice = Const.CATNIP_PRICE
    cooling = 3000
    image = 'img/猫尾草/普通/0.png'
    name = '猫尾草'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos[0], pos[1], gameObj)
        self.update = None
        self.x = pos[0]
        self.y = pos[1]
        self.fps = 7
        self.xOffset = -10
        self.yOffset = 5
        self.game = gameObj
        self.row = self.game.rowRoad[self.y]
        self.damm = 20
        self.update = FireCatnip
        self.image_index = 0
        self.shootImg = objectType[21]
        self.images = plantType[11]

    def check(self):
        if self.game.Zombies:
            for zombie in self.game.Zombies:
                if zombie.x <= 700:
                    return zombie
        return None

    def action(self):
        target = self.check()
        if target and self.tick % self.interval in [0, 10]:
            tem = TrackPea(self.x-15, self.y-5, self.game, self.damm)
            tem.images = self.shootImg
            self.game.Peas.append(tem)


class FireCatnip(Catnip):
    sunPrice = Const.FIRECATNIP_PRICE
    cooling = 3000
    alone = False
    image = 'img/猫尾草/火/0.png'
    name = '火球猫尾草'

    def __init__(self, pos, gameObj) -> None:
        super().__init__(pos, gameObj)
        self.update = None
        self.damm = 65
        self.interval = 140
        self.shootImg = objectType[17]
        self.images = plantType[10]

    def action(self):
        target = self.check()
        if target and self.tick % self.interval in [0, 25]:
            tem = TrackPea(self.x-15, self.y-5, self.game, self.damm)
            tem.images = self.shootImg
            self.game.Peas.append(tem)
