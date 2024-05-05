import sys
import pygame
from RWconfig import rwconfig
from Source import screen, objectType, menuText, scoreText, invalidClick_ogg, getImageSource, goodsType


class Goods:
    def __init__(self, x, y, id, name, image, price, state) -> None:
        self.x = x
        self.y = y
        self.id = id
        self.name = name
        self.state = state
        self.image = pygame.transform.scale(getImageSource(image), (50, 70))
        self.price = price
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        y = self.y+self.image.get_height()
        pygame.draw.rect(screen, (252, 235, 98), pygame.Rect(
            self.x, y, self.image.get_width()+10, 20))
        screen.blits([
            (self.image, (self.x, self.y)),
            (scoreText.render(f'${self.price}',
             True, (0, 0, 0)), (self.x, y+1))
        ])
        if not self.state:
            screen.blit(goodsType[0], (self.x-10, self.y))


class Shop:
    def __init__(self) -> None:
        self.flag = True
        self.dialogFlag = True
        self.image = objectType[19]
        self.money = rwconfig.money
        self.Goods = []
        col,rol=0,0
        for key in rwconfig.prop:
            prop = rwconfig.prop[key]
            self.Goods.append(
                Goods(380+80*col, 315, key, prop['name'], prop['image'], prop['price'], prop['state']))
            col += 1
        self.dialogButton = objectType[18]
        self.dialogImg = objectType[20]
        self.mainMenuRect = pygame.Rect(377, 512, 121, 70)
        self.confirmRect = self.dialogButton.get_rect(topleft=(275, 380))
        self.cancelRect = self.dialogButton.get_rect(topleft=(415, 380))

    def dialog(self, goods):
        self.dialogFlag = True
        propId = goods.id
        name = goods.name
        price = goods.price
        while self.dialogFlag:
            screen.blits([
                (self.dialogImg, ((800-self.dialogImg.get_width()) /
                 2, (600-self.dialogImg.get_height())/2)),
                (menuText.render(f'确定花费{price}$',
                 True, (107, 109, 145)), (300, 240)),
                (menuText.render(f'购买{name}吗', True,
                 (107, 109, 145)), (300, 270)),
                (self.dialogButton, (275, 380)),
                (self.dialogButton, (415, 380)),
                (menuText.render('确定', True,
                 (0, 216, 0)), (310, 391)),
                (menuText.render('取消', True,
                 (0, 216, 0)), (450, 391))
            ])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirmRect.collidepoint(event.pos):
                        if self.money >= price:
                            goods.state = 0
                            rwconfig.wconfig('user', 'money', self.money-price)
                            rwconfig.wconfig(propId, 'state', 0, True)
                            self.money = rwconfig.money
                            self.dialogFlag = False
                        else:
                            invalidClick_ogg.play()
                    elif self.cancelRect.collidepoint(event.pos):
                        self.dialogFlag = False

    def draw(self):
        self.flag = True
        while self.flag:
            screen.blits([
                (self.image, (0, 0)),
                (menuText.render('主菜单', True, (105, 152, 217)), (400, 537)),
                (objectType[15], (650, 560)),
                (scoreText.render(str(self.money), True,
                 (255, 215, 0)), (695, 568))
            ])
            for goods in self.Goods:
                goods.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mainMenuRect.collidepoint(event.pos):
                        self.flag = False
                    for goods in self.Goods:
                        if goods.rect.collidepoint(event.pos):
                            if goods.state:
                                self.dialog(goods)
                            else:
                                invalidClick_ogg.play()
                            break
