import sys
import pygame
import random
from RWconfig import rwconfig
from Coin import GoldCoin
from Object import Car, Sun
from Zombie import NomalZ, RoadZ, IronBZ, RugbyZ
from Plant import SunFlower, PeaShooter, Repeater, SpicyChili, NutsWall, PotatoMine, CherryBomb, Torchwood, GatlingPea
from Source import objectType, getImageSource, getSoundEffect, screen, clock, zombieEating_ogg, invalidClick_ogg, plant_ogg, plantSlot_ogg, wavetext, scoretext, menutext, zombieComing_ogg, zombieGroan_ogg, losemusic_ogg, winmusic_ogg, backgroundmusic, mainmenuBgm_ogg, pickup_ogg, shovel_ogg


class Game:
    def __init__(self) -> None:
        self.endRect = pygame.Rect(310, 241, 40, 40)
        self.background = pygame.transform.scale(
            getImageSource('img/scene/白天.jpg'), (1400, 600))
        self.moneybag = getImageSource('img/widget/关卡/moneybag.png')
        self.plantmenu = getImageSource('img/widget/菜单栏/植物商店.png')
        self.shovelslot = getImageSource('img/widget/菜单栏/铲子槽.png')
        self.shovel = getImageSource('img/widget/菜单栏/铲子.png')
        self.shovelpos = (447, -3)
        self.plantpos = (-100, -100)
        self.menu = getImageSource('img/widget/菜单栏/按钮.png')
        self.progress1 = getImageSource(
            'img/widget/进度/FlagMeterLevelProgress.png')
        self.progress2 = pygame.transform.scale(getImageSource(
            'img/widget/进度/FlagMeterEmpty.png'), (175, 30))
        self.progressflag1 = getImageSource(
            'img/widget/进度/FlagMeterParts1.png')
        self.progressflag2 = getImageSource(
            'img/widget/进度/FlagMeterParts2.png')
        self.chooseseed = pygame.transform.scale(getImageSource('img/widget/关卡/SeedChooser_Background.png'),
                                                 (475, 513))
        self.ready = getImageSource('img/widget/关卡/SeedChooser_Button.png')
        self.menuRect = self.menu.get_rect(topleft=(680, 0))
        self.money = rwconfig.money
        self.coinbank = objectType[15]
        self.readysetplant_ogg = getSoundEffect('aud/readysetplant.ogg')
        self.colload = {20: 1, 102: 2, 184: 3, 266: 4,
                        348: 5, 430: 6, 512: 7, 594: 8, 676: 9}
        self.rowload = {95: 1, 191: 2, 287: 3, 383: 4, 479: 5}
        self.loadzombies = {20: 1, 116: 2, 212: 3, 308: 4, 404: 5}
        self.plantcards = {
            'img/向日葵/0.png': SunFlower,
            'img/豌豆射手/0.png': PeaShooter,
            'img/双重射手/0.png': Repeater,
            'img/火爆辣椒/0.png': SpicyChili,
            'img/坚果/0.png': NutsWall,
            'img/土豆地雷/0.png': PotatoMine,
            'img/樱桃炸弹/0.png': CherryBomb,
            'img/火炬树桩/0.png': Torchwood,
            'img/机枪射手/0.png': GatlingPea
        }
        self.gameplantcards = dict()
        self.init()

    def init(self):
        self.first = True
        self.tick = 0
        self.playSun = 25
        self.flag = True
        self.selectp = True
        self.begining = False
        self.animation = False
        self.alpha = 0
        self.won = False
        self.wonflag = False
        self.wonpos = [550, 350]
        self.zombierule = dict()
        self.ZombiesType = [NomalZ]
        self.zombiestime = {120: 1, 1800: 2, 3600: 3,
                            5400: 5, 7800: 7, 10200: 8, 13200: 15, 17400: 25}
        self.wave = 0
        self.waves = list(self.zombiestime.keys())
        self.curScore = 0
        self.endScore = sum([i for i in self.zombiestime.values()])
        self.shovelactive = False
        self.curplant = None
        self.lastcard = None
        self.zombiesInroad = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.plantsInroad = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.Cards = []
        self.Peass = []
        from Lawn import Lawn
        self.lawns = [[Lawn(20 + (82 * x), 95 + (96 * y), self)
                       for x in range(9)] for y in range(5)]
        self.Plants = []
        self.Suns = []
        self.Zombies = []
        self.Cars = [Car(-30, y + 35, self) for y in self.rowload.keys()]
        self.Coins = []
        self.paused = False

    def selectplant(self):
        from Card import Card
        curcards = 0
        pygame.mixer.music.load(
            'aud/bgm/Choose Your Seeds-Laura Shigihara.mp3')
        pygame.mixer.music.play(-1)
        col, row = 0, 0
        for key, value in self.plantcards.items():
            if col == 9:
                row += 1
            self.Cards.append(
                Card(key, value, value.getprice(), value.getcooltime(), self, 13 + 50 * (col % 9), 122 + 72 * row))
            col += 1
        while self.selectp:
            self.update()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for card in self.Cards:
                        if card.rect.collidepoint(event.pos):
                            if card.active:
                                cur = 0
                                card.x = card.lastx
                                card.y = card.lasty
                                card.active = False
                                curcards -= 1
                                for card in self.Cards:
                                    if card.y == 7:
                                        card.x = 90 + 50 * cur
                                        cur += 1
                            elif not card.active and curcards < 7:
                                card.lastx = card.x
                                card.lasty = card.y
                                card.x = 90 + 50 * curcards
                                card.y = 7
                                card.active = True
                                curcards += 1
                            else:
                                invalidClick_ogg.play()
                    if pygame.Rect(320, 558, 156, 42).collidepoint(event.pos):
                        tem = []
                        for card in self.Cards:
                            if card.y == 7:
                                tem.append(card)
                        self.Cards = tem
                        self.selectp = False

    def win(self):
        from Main import mainmenu
        if self.animation:
            mask = pygame.Surface((800, 600))
            mask.set_alpha(self.alpha)
            mask.fill((255, 255, 255))
            screen.blit(mask, (0, 0))
            self.alpha += 2
            if self.alpha > 255:
                self.flag = False
                mainmenu.flag = True
                mainmenu.playmusic()
                mainmenu.draw()
        else:
            if self.wonflag:
                self.wonpos[0] += (310 - self.wonpos[0]) / 100
                self.wonpos[1] += (241 - self.wonpos[1]) / 100
            screen.blit(self.moneybag, self.wonpos)
            self.moneybagRect = self.moneybag.get_rect(topleft=self.wonpos)
            if self.moneybagRect.colliderect(self.endRect):
                ypos = [0, 1, 2, 1, 0]
                for i in range(5):
                    coin = GoldCoin(
                        self.wonpos[0] - 55 + 45 * i, self.wonpos[1] - 18 * ypos[i], self)
                    coin.pick = True
                    self.Coins.append(coin)
                self.begining = False
                self.animation = True

    def update(self):
        screen.blits([
            (self.background, (-220, 0)),
            (self.plantmenu, (10, 0)),
            (self.shovelslot, (456, 0)),
            (self.menu, (680, 0)),
            (scoretext.render(str(self.playSun), True, (0, 0, 0)), (26, 62)),
            (menutext.render('菜单', True, (0, 255, 0)), (715, 8)),
            (self.progress2, (600, 570)),
            (self.progress1, (645, 568)),
            (self.progressflag2, (605, 577)),
            (self.progressflag1, (748, 575)),
            (wavetext.render('第 ' + str(self.wave) +
                             ' 波', True, (0, 216, 0)), (670, 579))
        ])
        shovelpos = self.shovelpos if self.shovelactive else (447, -3)
        for car in self.Cars:
            car.draw()
        screen.blit(self.coinbank, (35, 570))
        screen.blit(scoretext.render(str(self.money),
                                     True, (255, 215, 0)), (80, 578))
        if self.selectp:
            screen.blits([
                (self.chooseseed, (0, 87)),
                (self.ready, (300, 550)),
                (menutext.render('一起摇滚吧!', True, (255, 215, 0)), (320, 558))
            ])
        for card in self.Cards:
            card.draw()
        for plant in self.Plants:
            plant.draw()
            plant.shot()
        for sun in self.Suns:
            sun.draw()
        for i in range(1, 6):
            zombies = self.zombiesInroad[i]
            if zombies:
                for zombie in zombies:
                    zombie.draw()
        for peas in self.Peass:
            peas.draw()
        for coin in self.Coins:
            coin.draw()
        screen.blit(self.shovel, shovelpos)
        if self.curplant and self.curplant != 'displant':
            screen.blit(self.curplant.getimage(), self.plantpos)

    def logical(self):
        # 出僵尸，阳光
        if self.tick == 3000:
            self.ZombiesType.append(RoadZ)
        elif self.tick == 7200:
            self.ZombiesType.append(IronBZ)
        elif self.tick == 15000:
            self.ZombiesType.append(RugbyZ)
        if self.tick in self.zombiestime:
            self.wave += 1
            interval = 180 if self.tick < 15000 else 90
            if self.tick == self.waves[-1] and self.loop:
                self.waves.append(self.waves[-1] + 4800)
                self.zombiestime[self.waves[-1]] = 25
            for i in range(self.zombiestime[self.tick]):
                self.zombierule[self.tick + interval * i] = 1
        if self.tick in self.zombierule:
            if self.first:
                zombieComing_ogg.play()
                self.first = False
            zombie = random.choice(self.ZombiesType)
            self.Zombies.append(zombie(20 + 96 * random.randint(0, 4), self))
        if self.tick % 1200 == 0:
            self.Suns.append(
                Sun(50, (random.randrange(60, 750), random.randrange(50, 450)), self, True))
        # 僵尸叫
        if self.Zombies and random.randrange(1000) == 0:
            random.choice(zombieGroan_ogg).play()
        # 胜利
        if self.curScore == self.endScore and not self.loop:
            self.won = True
        # 失败
        for zombie in self.Zombies:
            if zombie.x <= -100:
                pygame.mixer.music.pause()
                self.paused = True
                for i in zombieEating_ogg:
                    i.play()
                losemusic_ogg[0].play()
                losemusic_ogg[1].play()
                lose = getImageSource('img/widget/失败.png')
                screen.blit(pygame.transform.scale(getImageSource(
                    'img/widget/遮罩.png'), (800, 600)), (0, 0))
                screen.blit(lose, (
                    (screen.get_width() - lose.get_width()) / 2, (screen.get_height() - lose.get_height()) / 2))

    def playmusic(self):
        pygame.mixer.music.load(random.choice(backgroundmusic))
        pygame.mixer.music.set_volume(rwconfig.gamevolume)
        pygame.mixer.music.play(-1)

    def gamebegin(self, loop=False):
        from Source import menu
        self.loop = loop
        mainmenuBgm_ogg.stop()
        self.begining = True
        if self.selectp:
            self.selectplant()
        self.readysetplant_ogg.play()
        for img in objectType[10]:
            self.update()
            screen.blit(img, ((800 - img.get_width()) /
                              2, (600 - img.get_height()) / 2))
            pygame.display.flip()
            pygame.time.wait(500)
        self.playmusic()
        while self.flag:
            if not self.paused:
                self.update()
                self.logical()
                if self.won:
                    self.win()
                self.tick += 1
            for event in pygame.event.get():
                if not self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for sun in self.Suns:
                                if sun.rect.collidepoint(event.pos):
                                    sun.pick = True
                                    pickup_ogg.play()
                                    break
                            for coin in self.Coins:
                                if coin.rect.collidepoint(event.pos):
                                    coin.pick = True
                                    break
                            if self.won and self.moneybagRect.collidepoint(event.pos):
                                self.wonflag = True
                                pygame.mixer.music.stop()
                                winmusic_ogg.play()
                            if self.shovel.get_rect(topleft=(464, 9)).collidepoint(event.pos):
                                if self.lastcard:
                                    self.lastcard.selected = None
                                self.curplant = 'displant'
                                shovel_ogg.play()
                                self.shovelactive = True
                            elif self.menuRect.collidepoint(event.pos):
                                menu.flag = True
                                menu.returnimg = menu.returnimg0
                                menu.draw()
                            for card in self.Cards:
                                if card.rect.collidepoint(event.pos):
                                    if self.playSun >= int(card.price) and card.curtime == '0':
                                        if card.selected:
                                            self.lastcard = card.selected = self.curplant = None
                                        else:
                                            if self.lastcard:
                                                self.lastcard.selected = None
                                            plantSlot_ogg.play()
                                            card.selected = card.coolimage
                                            self.lastcard = card
                                            self.curplant = card.plant
                                    else:
                                        invalidClick_ogg.play()
                            for row in self.lawns:
                                for lawn in row:
                                    x, y = lawn.getpos()
                                    p = self.lawns[self.rowload[y] -
                                                   1][self.colload[x] - 1]
                                    if lawn.rect.collidepoint(event.pos) and self.curplant == 'displant' and p.plant:
                                        if p.plant.sunprice != 0:
                                            self.Suns.append(
                                                Sun(p.plant.sunprice // 2, (x, y), self))
                                        p.displanting()
                                        random.choice(plant_ogg).play()
                                        self.shovelactive = False
                                        self.curplant = None
                                        break
                                    elif lawn.rect.collidepoint(event.pos) and self.curplant == 'displant':
                                        if self.shovelactive:
                                            self.shovelactive = False
                                            self.curplant = None
                                        break
                                    elif lawn.rect.collidepoint(
                                            event.pos) and self.curplant and self.curplant != 'displant' and self.lastcard.curtime == '0' and self.playSun >= self.curplant.getprice():
                                        if lawn.planting(self.curplant, (x, y)):
                                            self.playSun -= self.curplant.getprice()
                                            self.curplant = None
                                            self.lastcard.curtime = self.lastcard.cooltime
                                            self.lastcard.selected = None
                                        break
                        elif event.button == 3:
                            for zombie in self.Zombies:
                                if zombie.rect.collidepoint(event.pos):
                                    zombie.dead = 1
                            if self.curplant == 'displant' and self.shovelactive:
                                self.shovelactive = False
                                self.curplant = None
                    elif event.type == pygame.MOUSEMOTION:
                        if self.curplant and self.curplant != 'displant':
                            self.plantpos = (
                                event.pos[0] - 30, event.pos[1] - 40)
                        else:
                            self.plantpos = (-100, -100)
                        if self.shovelactive:
                            self.shovelpos = (
                                event.pos[0] - 30, event.pos[1] - 40)
                        else:
                            self.shovelpos = (463, 9)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu.flag = True
                        menu.returnimg = menu.returnimg0
                        menu.draw()
            pygame.display.flip()
            clock.tick(60)
