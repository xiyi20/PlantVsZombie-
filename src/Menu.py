import sys
import pygame
import pygame.mixer
from pygame.locals import K_a, K_z
from RWconfig import rwconfig
from Source import getImageSource, getSoundEffect, screen, invalidClick_ogg, menutext, buttonClick_ogg, mainmenuBgm_ogg, paper_ogg, tittletext, menuClick_ogg


class Menu:
    def __init__(self, game) -> None:
        self.flag = True
        self.game = game
        self.pause_ogg = getSoundEffect('aud/pause.ogg')
        self.menu = getImageSource('img/widget/菜单栏/options_menuback.png')
        self.buttondown = False
        self.returnimg0 = getImageSource(
            'img/widget/菜单栏/options_backtogamebutton0.png')
        self.returnimg1 = getImageSource(
            'img/widget/菜单栏/options_backtogamebutton1.png')
        self.returnimg = self.returnimg0
        self.returnimgRect = self.returnimg.get_rect(topleft=(220, 432))
        self.volumedown = False
        self.progress = getImageSource('img/widget/菜单栏/options_sliderslot.png')
        self.pointer = getImageSource('img/widget/菜单栏/options_sliderknob2.png')
        self.ispoint = False
        self.pointpos = (rwconfig.menuvolume / 0.008775 + 350, 208)
        self.button = pygame.transform.scale(game.menu, (200, 41))
        self.againRect = pygame.Rect(295, 333, 200, 41)
        self.mainmenuRect = pygame.Rect(295, 375, 200, 41)

    def updata(self, y=452):
        screen.blits([
            (self.menu, (188.5, 51)),
            (self.returnimg, (220, 432)),
            (menutext.render('音乐', True, (107, 109, 145)), (300, 210)),
            (self.progress, (350, 218)),
            (self.pointer, self.pointpos),
            (tittletext.render('返回', True, (0, 216, 0)), (350, y))
        ])
        if self.game.begining:
            screen.blits([
                (self.button, (295, 333)),
                (menutext.render('重新开始', True, (0, 216, 0)), (352, 340)),
                (self.button, (295, 375)),
                (menutext.render('主菜单', True, (0, 216, 0)), (365, 383)),
            ])
        self.pointerRect = self.pointer.get_rect(topleft=self.pointpos)
        pygame.display.flip()

    def draw(self):
        from Source import mainmenu
        self.mainmenuobj = mainmenu
        if self.game.begining:
            self.pointpos = (rwconfig.gamevolume / 0.008775 + 350, 208)
            self.pause_ogg.play()
            self.game.pause = True
        else:
            self.pointpos = (rwconfig.menuvolume / 0.008775 + 350, 208)
        while self.flag:
            for event in pygame.event.get():
                self.updata()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.volumedown = True
                    if self.returnimgRect.collidepoint(event.pos):
                        buttonClick_ogg.play()
                        self.buttondown = True
                        self.returnimg = self.returnimg1
                        self.updata(454)
                    elif self.pointerRect.collidepoint(event.pos):
                        self.ispoint = True
                    elif self.game.begining and self.againRect.collidepoint(event.pos):
                        self.game.flag = False
                        self.game.init()
                        self.game.gamebegin()
                    elif self.game.begining and self.mainmenuRect.collidepoint(event.pos):
                        self.game.flag = False
                        self.game.begining = False
                        pygame.mixer.music.stop()
                        self.mainmenuobj.flag = True
                        self.mainmenuobj.playmusic()
                        self.mainmenuobj.draw()
                    else:
                        self.ispoint = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.volumedown = False
                    self.ispoint = False
                    if self.returnimgRect.collidepoint(event.pos) and self.buttondown:
                        self.flag = False
                        self.buttondown = False
                        curvolume = 'menu'
                        if self.game.begining:
                            curvolume = 'game'
                            self.game.pause = False
                        rwconfig.wconfig('volume', curvolume,
                                         0.008775 * (self.pointpos[0] - 350))
                elif event.type == pygame.MOUSEMOTION:
                    if self.volumedown and self.ispoint:
                        x = min(max(361, event.pos[0]), 474)
                        self.pointpos = (x - 10, 208)
                self.returnimg = self.returnimg0
        if not self.game.begining:
            mainmenuBgm_ogg.set_volume(rwconfig.menuvolume)
        else:
            pygame.mixer.music.set_volume(rwconfig.gamevolume)


class MainMenu:
    def __init__(self, game) -> None:
        self.flag = True
        self.game = game
        mainmenuBgm_ogg.set_volume(rwconfig.menuvolume)
        self.menuClick_ogg = getSoundEffect('aud/bleep.ogg')

        # 开屏界面
        self.load = 250
        self.loading = True
        self.tittlescreen = getImageSource('img/主界面/titlescreen.jpg')
        self.popcap = getImageSource('img/主界面/PopCap_Logo.png')
        self.popcap = pygame.transform.scale(self.popcap, (150, 150))
        self.pvzlogo = getImageSource('img/主界面/PvZ_Logo.png')
        self.loadbar = getImageSource('img/主界面/LoadBar_dirt.png')
        self.loadgrass = getImageSource('img/主界面/LoadBar_grass.png')
        self.angle = 0
        self.rollcapimage = getImageSource('img/主界面/SodRollCap.png')

        # 主界面
        self.center = getImageSource('img/主界面/center.png')
        self.BG = pygame.transform.scale(getImageSource(
            'img/主界面/SelectorScreen_BG.png'), (800, 600))
        self.left = getImageSource('img/主界面/left.png')
        self.right = getImageSource('img/主界面/right.png')
        self.hello = getImageSource('img/主界面/SelectorScreen_WoodSign1.png')
        self.save0 = getImageSource('img/主界面/SelectorScreen_WoodSign2.png')
        self.save1 = getImageSource(
            'img/主界面/SelectorScreen_WoodSign2_press.png')
        self.save = self.save1
        self.saveRect = self.save1.get_rect(topleft=(20, 135))
        self.grass = getImageSource('img/主界面/SelectorScreen_Leaves.png')
        self.leaf1 = getImageSource('img/主界面/SelectorScreen_Leaf4.png')
        self.leaf2 = getImageSource('img/主界面/SelectorScreen_Leaf5.png')
        self.leaf3 = getImageSource('img/主界面/SelectorScreen_Leaf3.png')
        self.leaf4 = getImageSource('img/主界面/SelectorScreen_Leaf1.png')
        self.flower1 = getImageSource('img/主界面/SelectorScreen_Flower1.png')
        self.flower2 = getImageSource('img/主界面/SelectorScreen_Flower2.png')
        self.flower3 = getImageSource('img/主界面/SelectorScreen_Flower3.png')
        self.help0 = getImageSource('img/主界面/SelectorScreen_Help1.png')
        self.help1 = getImageSource('img/主界面/SelectorScreen_Help2.png')
        self.help = self.help0
        self.helpRect = self.help0.get_rect(topleft=(648, 525))
        self.option0 = getImageSource('img/主界面/SelectorScreen_Options1.png')
        self.option1 = getImageSource('img/主界面/SelectorScreen_Options2.png')
        self.option = self.option0
        self.optionRect = self.option0.get_rect(topleft=(563, 487))
        self.exit0 = getImageSource('img/主界面/SelectorScreen_Quit1.png')
        self.exit1 = getImageSource('img/主界面/SelectorScreen_Quit2.png')
        self.exit = self.exit0
        self.exitRect = self.exit0.get_rect(topleft=(720, 515))
        self.rename = getImageSource('img/主界面/rename.png')

        # 游戏选择
        # 冒险
        self.adventure0 = getImageSource(
            'img/主界面/SelectorScreen_StartAdventure_Button.png')
        self.adventure1 = getImageSource(
            'img/主界面/SelectorScreen_StartAdventure_Highlight.png')
        self.adventure = self.adventure0
        self.adventureRect = pygame.Rect(
            404, 55, self.adventure.get_width(), self.adventure.get_height() - 25)
        # 小游戏
        self.small0 = getImageSource(
            'img/主界面/SelectorScreen_Survival_button.png')
        self.small1 = getImageSource(
            'img/主界面/SelectorScreen_Survival_Highlight.png')
        self.small = self.small0
        self.smallRect = pygame.Rect(
            405, 185, self.small.get_width(), self.small.get_height() - 50)
        # 解密
        self.challeng0 = getImageSource(
            'img/主界面/SelectorScreen_Challenges_button.png')
        self.challeng1 = getImageSource(
            'img/主界面/SelectorScreen_Challenges_Highlight.png')
        self.challeng = self.challeng0
        self.challengRect = pygame.Rect(
            412, 275, self.challeng.get_width(), self.challeng.get_height() - 45)
        # 生存
        self.survival0 = getImageSource(
            'img/主界面/SelectorScreen_Vasebreaker_button.png')
        self.survival1 = getImageSource(
            'img/主界面/SelectorScreen_Vasebreaker_Highlight.png')
        self.survival = self.survival0
        self.survivalRect = pygame.Rect(
            450, 340, self.survival.get_width(), self.survival.get_height() - 45)

        # 商店
        self.shop0 = getImageSource('img/主界面/SelectorScreen_Store.png')
        self.shop1 = getImageSource(
            'img/主界面/SelectorScreen_StoreHighlight.png')
        self.shop = self.shop0
        self.shopRect = self.shop.get_rect(topleft=(400, 480))

        # 帮助
        self.helpering = True
        self.words = getImageSource('img/主界面/says.png')
        self.wordsbg = pygame.transform.scale(
            getImageSource('img/主界面/saysbg.jpg'), (800, 600))
        self.backmenu0 = getImageSource('img/主界面/return.png')
        self.backmenu1 = getImageSource('img/主界面/return1.png')
        self.backmenu = self.backmenu0
        self.backmenuRect = self.backmenu.get_rect(topleft=(322, 520))

        # 读取配置
        self.naming = True
        self.name = rwconfig.name
        self.typing = self.name
        self.confirm = pygame.Rect(190, 331, 204, 44)
        self.cancel = pygame.Rect(410, 331, 204, 44)

        from Source import menu
        self.menuobj = menu

    def playmusic(self):
        mainmenuBgm_ogg.play(-1)

    def init(self):        
        self.playmusic()
        def updata():
            screen.blits([
                (self.tittlescreen, (0, 0)),
                (self.pvzlogo, (60, 30)),
                (self.popcap, (-10, -10)),
                (self.loadbar, ((800 - self.loadbar.get_width()) // 2, 500)),
                (self.loadgrass, ((800 - self.loadbar.get_width()) // 2, 480))
            ])

        while self.loading and self.load <= 533:
            updata()
            screen.blit(menutext.render(
                '请等待加载', True, (255, 215, 0)), (345, 510))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    self.loading = False
                    break
            rollcap = pygame.transform.rotate(self.rollcapimage, self.angle)
            new_rect = rollcap.get_rect(center=(self.load, 470))
            screen.blit(rollcap, new_rect.topleft)
            self.angle -= 0.3
            self.load += 0.2
            pygame.display.flip()
        updata()
        screen.blit(menutext.render(
            '任意操作以开始游戏', True, (255, 215, 0)), (295, 510))
        self.draw()

    def updata(self):
        screen.blits([
            (self.BG, (0, 0)),
            (self.center, (90, 270)),
            (self.left, (0, -70)),
            (self.right, (70, 40)),
            (self.hello, (20, 0)),
            (self.save, (20, 135)),
            (self.grass, (0, 538)),
            (self.leaf1, (220, 562)),
            (self.leaf3, (255, 550)),
            (self.leaf2, (248, 572)),
            (self.leaf4, (287, 565)),
            (menutext.render(self.name, True, (255, 215, 0)), (150, 90))
        ])
        screen.blits([
            (self.adventure, (405, 55)),
            (self.small, (405, 168)),
            (self.challeng, (412, 255)),
            (self.survival, (410, 325)),
            (self.shop, (400, 480)),
            (self.flower1, (682, 415)),
            (self.flower2, (637, 435)),
            (self.flower3, (735, 457)),
            (self.option, (563, 487)),
            (self.help, (648, 525)),
            (self.exit, (720, 515))
        ])

    def click(self, mode):
        val = self.name if mode == 0 else self.typing
        if not val:
            invalidClick_ogg.play()
        else:
            menuClick_ogg.play()
            return True

    def setname(self):
        while self.naming:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    leng = len(self.typing)
                    if event.key == 8 and leng > 0:
                        self.typing = self.typing[:-1]
                    elif event.key in range(K_a, K_z + 1) and leng <= 10:
                        self.typing += chr(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirm.collidepoint(event.pos):
                        if self.click(1):
                            rwconfig.wconfig('user', 'name', self.typing)
                            self.name = self.typing
                            self.naming = False
                    elif self.cancel.collidepoint(event.pos):
                        if self.click(0):
                            self.typing = self.name
                            self.naming = False
                screen.blits([
                    (self.rename, (154, 104)),
                    (pygame.transform.scale(self.game.menu, (204, 44)), (190, 331)),
                    (pygame.transform.scale(self.game.menu, (204, 44)), (410, 331)),
                    (menutext.render('确定', True, (0, 255, 0)), (270, 340)),
                    (menutext.render('取消', True, (0, 255, 0)), (490, 340)),
                    (menutext.render(self.typing, True, (255, 215, 0)), (205, 256))
                ])
                pygame.display.flip()

    def updatabutton(self, rect, currentstate, defaultimage, hoverimage, pos):
        if rect.collidepoint(pos):
            if currentstate == defaultimage:
                self.menuClick_ogg.play()
            return hoverimage
        return defaultimage

    def helper(self):
        paper_ogg.play()
        while self.helpering:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backmenuRect.collidepoint(event.pos):
                        self.helpering = False
                        self.flag = True
                        self.draw()
                else:
                    if event.type == pygame.MOUSEMOTION:
                        self.backmenu = self.updatabutton(self.backmenuRect, self.backmenu, self.backmenu0,
                                                          self.backmenu1, event.pos)
                    screen.blits([
                        (self.wordsbg, (0, 0)),
                        (self.words, (85, 80)),
                        (self.backmenu, (322, 520)),
                        (menutext.render('返回主页', True, (255, 215, 0)), (355, 528))
                    ])
                    pygame.display.flip()

    def draw(self):
        while self.flag:
            for event in pygame.event.get():
                self.updata()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    self.adventure = self.updatabutton(self.adventureRect, self.adventure, self.adventure0,
                                                       self.adventure1, event.pos)
                    self.small = self.updatabutton(
                        self.smallRect, self.small, self.small0, self.small1, event.pos)
                    self.challeng = self.updatabutton(self.challengRect, self.challeng, self.challeng0, self.challeng1,
                                                      event.pos)
                    self.survival = self.updatabutton(self.survivalRect, self.survival, self.survival0, self.survival1,
                                                      event.pos)
                    self.option = self.updatabutton(
                        self.optionRect, self.option, self.option0, self.option1, event.pos)
                    self.help = self.updatabutton(
                        self.helpRect, self.help, self.help0, self.help1, event.pos)
                    self.exit = self.updatabutton(
                        self.exitRect, self.exit, self.exit0, self.exit1, event.pos)
                    self.save = self.updatabutton(
                        self.saveRect, self.save, self.save0, self.save1, event.pos)
                    self.shop = self.updatabutton(
                        self.shopRect, self.shop, self.shop0, self.shop1, event.pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.adventureRect.collidepoint(event.pos):
                        self.flag = False
                        self.game.init()
                        self.game.gamebegin()
                    if self.survivalRect.collidepoint(event.pos):
                        self.flag = False
                        self.game.flag = True
                        if self.game.won:
                            self.game.init()
                        self.game.gamebegin(True)
                    elif self.saveRect.collidepoint(event.pos):
                        self.naming = True
                        self.setname()
                    elif self.exitRect.collidepoint(event.pos):
                        menuClick_ogg.play()
                        pygame.quit()
                        sys.exit()
                    elif self.helpRect.collidepoint(event.pos):
                        menuClick_ogg.play()
                        self.flag = False
                        self.helpering = True
                        self.helper()
                    elif self.optionRect.collidepoint(event.pos):
                        menuClick_ogg.play()
                        self.menuobj.flag = True
                        self.menuobj.returnimg = self.menuobj.returnimg0
                        self.menuobj.draw()
                if self.name == '':
                    self.setname()
            pygame.display.flip()
