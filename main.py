import pygame
import pygame.mixer
from pygame.locals import K_a,K_z
import random
import json
import time
import math

class Lawn:
    def __init__(self, x, y,game):
        self.plant=None
        self.game=game
        self.x = x
        self.y = y
        self.row=self.game.rowload[self.y]
        self.rect = pygame.Rect(x, y,82,96)

    def getpos(self):
        return (self.x,self.y)
    
    def planting(self, plant):
        if not self.plant:
            self.plant=plant
            self.game.Plants.append(plant)
            self.game.plantsInload[self.row].append(plant)
            random.choice(plant_ogg).play()
            return True
        return False

    def displanting(self):
        if self.plant:
            self.game.Plants.remove(self.plant)
            self.game.plantsInload[self.row].remove(self.plant)
            self.plant=None

class Card:
    def __init__(self,img,plant,price,cooltime,game,x=200) -> None:
        self.img=img
        self.plant=plant
        self.selected=None
        self.price=str(price)
        self.coolimage=getImageSource('images/widget/遮罩.png')
        self.cooltime=str(cooltime)
        self.interval=72/cooltime
        self.curtime='0'
        self.game=game
        self.x=x
        self.rect=pygame.Rect(x,7,50,72)

    def draw(self):
        plantcard=pygame.transform.scale(getImageSource('images/widget/卡槽.png'),(50,72))
        plantimage=pygame.transform.scale(getImageSource(self.img),(30,30))
        screen.blit(plantcard,(self.x,7))
        screen.blit(plantimage,(self.x+10,25))
        color=(255, 0, 0) if int(self.price)>self.game.playSun else (0, 0, 0)
        screen.blit(pricetext.render(self.price, True, color),(self.x+2,62))
        if self.selected:screen.blit(self.selected,(self.x-2,8))
        if self.curtime!='0':
            screen.blit(pygame.transform.scale(self.coolimage,(50,int(self.curtime)*self.interval)),(self.x,7))
            self.curtime=str(int(self.curtime)-1)

class Object:
    def __init__(self) -> None:
        self.tick=0
        self.image_index=0
        self.distorypos=screen.get_width()-30

    def draw(self):
        if self.tick%4==0:
            self.image_index = (self.image_index+1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x, self.y+20))
        self.tick+=1

class Car(Object):
    def __init__(self,x,y,game) -> None:
        super().__init__()
        self.speed=4
        self.x=x
        self.y=y
        self.game=game
        self.active=False
        self.canplay=True
        self.image=getImageSource('images/widget/小推车.png')
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

    def draw(self):
        for zombie in game.zombiesInload[game.rowload[self.y-35]]:
            if self.rect.colliderect(zombie.rect):
                zombie.dead=1
                self.active=True
        if self.active:
            self.x+=self.speed
            if self.canplay:
                car_ogg.play()
                self.canplay=False
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        screen.blit(self.image,(self.x,self.y))
        if self.x>=self.distorypos:
            self.game.Cars.remove(self)

class Sun(Object):
    def __init__(self, val, pos,game,falling=False):
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.cury=100
        self.targety=pos[1]
        self.game=game
        self.falling=falling
        self.image_index = 0
        self.life=900
        self.tick=0
        self.images = [getImageSource(f'images/太阳/{i}.png') for i in range(29)]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
    
    def draw(self):
        if self.falling and self.tick%2==0 and self.cury<self.targety:
            self.cury+=1
            self.rect = pygame.Rect(self.x, self.cury, self.images[0].get_width(), self.images[0].get_height())
        self.y=self.cury if self.falling else self.targety
        screen.blit(self.images[self.image_index], (self.x, self.y+20))
        if self.tick%4==0:self.image_index = (self.image_index+1) % len(self.images)
        self.tick+=1
        if self.tick-self.life==0:
            game.Suns.remove(self)        

    def pickup(self):
        pickup_ogg.play()
        self.game.playSun+=self.val
        self.game.Suns.remove(self)

class Peas(Object):
    def __init__(self,x,y,game,damm=15) -> None:
        super().__init__()
        self.x=x+35
        self.y=y+5
        self.game=game
        self.damm=damm
        self.speed=4
        self.image=getImageSource('images/豌豆射手/豆.png')
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),140)
        random.choice(shoot_ogg).play()

    def draw(self):
        screen.blit(self.image,(self.x,self.y))
        self.x+=self.speed
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        for zombie in game.zombiesInload[game.rowload[self.y-5]]:
            if zombie.rect.colliderect(self.rect):
                zombie.blood -= self.damm
                random.choice(zombie.hiteffect).play()
                self.game.Peass.remove(self)
                if zombie.blood <= 0:zombie.dead=1
                break
        if self.x>=self.distorypos:
            self.game.Peass.remove(self)  

class Plant:
    sunprice=0
    cooling=450
    image=None
    def __init__(self,col,row,game) -> None:
        self.blood=300
        self.col=game.colload[col]
        self.row=game.rowload[row]
        self.rect=None
        self.tick=0
        self.interval=80

    @classmethod
    def getprice(cls):
        return cls.sunprice
    
    @classmethod
    def getimage(cls):
        return getImageSource(cls.image)

    @classmethod
    def getcooltime(cls):
        return cls.cooling

    def shot(self):
        pass

    def draw(self):
        if self.tick%4==0:
            self.image_index = (self.image_index+1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x+13, self.y+5))
        self.tick+=1

    def hurt(self,damm):
        self.blood-=damm
        random.choice(zombieEating_ogg).play()
        if self.blood<0:
            self.game.lawns[self.row-1][self.col-1].displanting()
            plantDead_ogg.play()
            return True

class Sunflower(Plant):
    sunprice=25
    image='images/向日葵/0.png'
    def __init__(self,pos,game):
        super().__init__(pos[0],pos[1],game)
        self.x = pos[0]
        self.y = pos[1]
        self.game=game
        self.image_index = 0
        self.images = [getImageSource(f'images/向日葵/{i}.png') for i in range(18)]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.suntime=random.randint(180,720)

    def draw(self):
        if self.tick%4==0:
            self.image_index = (self.image_index+1) % len(self.images)
        screen.blit(self.images[self.image_index], (self.x+13, self.y+5))
        self.tick+=1
        self.suntime-=1
        if self.suntime==0:
            self.game.Suns.append(Sun(50,(self.x+44,self.y+25),self.game))
            self.suntime=random.randint(1200,1800)

class PeasShoter(Plant):
    sunprice=75
    image='images/豌豆射手/0.png'
    def __init__(self,pos,game) -> None:
        super().__init__(pos[0],pos[1],game)
        self.x = pos[0]
        self.y = pos[1]
        self.game=game
        self.row=game.rowload[self.y]
        self.damm=20
        self.image_index = 0
        self.images = [getImageSource(f'images/豌豆射手/{i}.png') for i in range(13)]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        
    def shot(self):
        if game.zombiesInload[self.row]:
            for zombie in game.zombiesInload[self.row]:
                if self.x-30<=zombie.x<=700:
                    if self.tick%self.interval==0:
                        self.game.Peass.append(Peas(self.x,self.y,self.game,self.damm))
                        break
                
class Repeater(Plant):
    sunprice=0
    image='images/双重射手/0.png'
    def __init__(self,pos,game) -> None:
        super().__init__(pos[0],pos[1],game)
        self.x = pos[0]
        self.y = pos[1]
        self.game=game
        self.row=self.game.rowload[self.y]
        self.damm=20
        self.image_index = 0
        self.images = [getImageSource(f'images/双重射手/{i}.png') for i in range(15)]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        
    def shot(self):
        if game.zombiesInload[self.row]:
            for zombie in game.zombiesInload[self.row]:
                if self.x-30<=zombie.x<=700:
                    if self.tick%self.interval in [0,10]:
                        self.game.Peass.append(Peas(self.x,self.y,self.game,self.damm))
                        break

class SpicyChili(Plant):
    sunprice=125
    cooling=300
    image='images/火爆辣椒/0.png'
    def __init__(self,pos,game) -> None:
        super().__init__(pos[0], pos[1],game)
        self.x=pos[0]
        self.y=pos[1]
        self.game=game
        self.row=self.game.rowload[self.y]
        self.col=self.game.colload[self.x]
        self.damm=1800
        self.booming=False
        self.spicy_ogg=getSoundEffect('sounds/jalapeno.ogg')
        self.image_index=0
        self.images=[getImageSource(f'images/火爆辣椒/{i}.png') for i in range(7)]
        self.rect=pygame.Rect(self.x,self.y,self.images[0].get_width(),self.images[0].get_height())
        self.boom_index=0
        self.boomimages=[getImageSource(f'images/火/{i}.png') for i in range(8)]
        self.boomRect=pygame.Rect(50,self.y,730,self.images[0].get_height())
    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(self.image_index)], (self.x+10,self.y-5))
            self.image_index+=0.25
            if self.image_index==len(self.images):
                self.booming=True
                self.spicy_ogg.play()
                for zombie in self.game.Zombies:
                    if self.boomRect.colliderect(zombie.rect):
                        zombie.blood-=self.damm
                        if zombie.blood<=0:
                            zombie.dead=2
        else:
            screen.blit(self.boomimages[math.floor(self.boom_index)], (25, self.y-40))
            self.boom_index+=0.25
            if self.boom_index==len(self.boomimages):
                self.game.lawns[self.row-1][self.col-1].displanting()         
            
class NutsWall(Plant):
    sunprice=50
    cooling=1800
    image='images/坚果/0.png'
    def __init__(self,pos,game) -> None:
        super().__init__(pos[0], pos[1],game)
        self.x=pos[0]
        self.y=pos[1]
        self.game=game
        self.row=game.rowload[self.y]
        self.col=game.colload[self.x]
        self.image_index=0
        self.blood=4000
        self.images=[getImageSource(f'images/坚果/{i}.png') for i in range(16)]
        self.rect=pygame.Rect(self.x,self.y,self.images[0].get_width(),self.images[0].get_height())

class PotatoMine(Plant):
    sunprice=25
    cooling=1800
    image='images/土豆地雷/0.png'
    def __init__(self,pos, game) -> None:
        super().__init__(pos[0], pos[1], game)
        self.x=pos[0]+30
        self.y=pos[1]+45
        self.game=game
        self.damm=1800
        self.row=game.rowload[pos[1]]
        self.col=game.colload[pos[0]]
        self.image_index=0
        self.active=False
        self.booming=False
        self.boomtime=0
        self.active_ogg=getSoundEffect('sounds/gravestone_rumble.ogg')
        self.boom_ogg=getSoundEffect('sounds/potato_mine.ogg')
        self.boom1=getImageSource('images/土豆地雷/爆炸.gif')
        self.boom2=getImageSource('images/土豆地雷/土豆泥.gif')
        self.images0=[getImageSource('images/土豆地雷/在地下.gif')]
        self.images1=[getImageSource(f'images/土豆地雷/{i}.png') for i in range(8)]
        self.images=self.images0
        self.rect=pygame.Rect(pos[0],pos[1],self.images1[0].get_width(),self.images1[0].get_height())
    
    def draw(self):
        tem=[]
        if not self.booming:
            if self.tick%13==0:
                self.image_index = (self.image_index+1) % len(self.images)
            if self.tick==900:
                self.active=True
                self.active_ogg.play()
                self.x,self.y=self.x-18,self.y-20
                self.images=self.images1
            screen.blit(self.images[self.image_index],(self.x,self.y))
            self.tick+=1
            for zombie in self.game.zombiesInload[self.row]:
                if self.rect.colliderect(zombie.rect) and self.active:
                    self.booming=True
                    self.boom_ogg.play()
                    for zombie in self.game.zombiesInload[self.row]:
                        if -25<zombie.x-self.x+30<25:tem.append(zombie)
                    if tem:
                        for i in tem:
                            i.blood-=self.damm
                            if i.blood<=0:
                                i.deadanimation=False
                                i.dead=1
                    break
        else:
            if self.boomtime<=60:
                screen.blits([
                    (self.boom2,(self.x-30,self.y-25)),
                    (self.boom1,(self.x-45,self.y-55))
                ])
                self.boomtime+=1    
            else:
                self.game.lawns[self.row-1][self.col-1].displanting()        

class CherryBomb(Plant):
    sunprice=150
    cooling=300
    image='images/樱桃炸弹/0.png'
    def __init__(self,pos,game) -> None:
        super().__init__(pos[0], pos[1],game)
        self.x=pos[0]
        self.y=pos[1]
        self.game=game
        self.row=self.game.rowload[self.y]
        self.col=self.game.colload[self.x]
        self.damm=1800
        self.booming=False
        self.boom_ogg=getSoundEffect('sounds/cherrybomb.ogg')
        self.image_index=0
        self.images=[getImageSource(f'images/樱桃炸弹/{i}.png') for i in range(7)]
        self.rect=pygame.Rect(self.x,self.y,self.images[0].get_width(),self.images[0].get_height())
        self.boomtime=0
        self.boomimage=getImageSource('images/樱桃炸弹/boom.png')
        self.boomRect=pygame.Rect(self.x-70,self.y-30,200,130)
    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(self.image_index)], (self.x-10,self.y-5))
            self.image_index+=0.25
            if self.image_index==len(self.images):
                self.booming=True
                self.boom_ogg.play()
                for zombie in self.game.Zombies:
                    if self.boomRect.colliderect(zombie.rect):
                        zombie.blood-=self.damm
                        if zombie.blood<=0:
                            zombie.dead=2
        else:
            if self.boomtime<=30:
                screen.blit(self.boomimage,(self.x-70,self.y-30))
                self.boomtime+=1
            else:
                self.game.lawns[self.row-1][self.col-1].displanting()
                   
class Zombie:
    def __init__(self,y,zombie,game,type=0) -> None:
        self.x=790
        self.speed=0.25
        self.blood=260
        self.sunval=0
        self.game=game
        self.damm=100
        self.tick=0
        self.dead=0
        self.deadanimation=True
        self.deadindex=0
        self.row=game.loadzombies[y]
        self.eating=None
        self.eat_count=0
        self.type=type
        self.state='walk'
        self.fps=4
        self.hiteffect=splat_ogg
        self.laststate=None
        self.game.zombiesInload[self.row].append(zombie)
        self.images=None
        self.zombies=[
            [
                [getImageSource(f'images/普通僵尸/走/{i}.png') for i in range(18)],
                [getImageSource(f'images/普通僵尸/吃/{i}.png') for i in range(18)]
            ],
            [
                [getImageSource(f'images/路障僵尸/走/{i}.png') for i in range(21)],
                [getImageSource(f'images/路障僵尸/吃/{i}.png') for i in range(11)]
            ],
            [
                [getImageSource(f'images/铁桶僵尸/走/{i}.png') for i in range(15)],
                [getImageSource(f'images/铁桶僵尸/吃/{i}.png') for i in range(11)]
            ],
        ]
        self.die=[
            [getImageSource(f'images/僵尸死/普通/{i}.png') for i in range(10)],
            [getImageSource(f'images/僵尸死/灰烬/{i}.png') for i in range(10)]
        ]

    def draw(self):
        if self.dead==0:
            self.state='eat' if self.eating else 'walk'
            for plant in game.plantsInload[self.row]:
                if self.rect.colliderect(plant.rect):
                    self.eating=plant
                    self.state='eat'
                    self.resetstate()
                    break
            if self.state=='walk':
                self.images=self.zombies[self.type][0]
                self.x-=self.speed
                self.islose()
                self.rect=pygame.Rect(self.x+100, self.y, 20, self.images[0].get_height())
            else:
                self.images=self.zombies[self.type][1]
                if self.game.lawns[self.eating.row-1][self.eating.col-1].plant:
                    if self.eat_count%60==0:
                        if self.eating.hurt(self.damm):
                            self.state='walk'
                            self.resetstate()
                            self.eating=None
                    self.eat_count+=1
                else:
                    self.eat_count=60
                    self.state='walk'
                    self.resetstate()
                    self.eating=None   
            if self.tick%self.fps==0:
                self.image_index = (self.image_index + 1) % len(self.images)
            self.tick+=1
            screen.blit(self.images[self.image_index], (self.x+10, self.y+20))
        else:
            if self.deadanimation:self.dieanimation()
            else:self.distory()

    def resetstate(self):
        if self.laststate!=self.state:
            self.image_index=0
            self.laststate=self.state

    def islose(self):
        if self.x<=-90:
            pygame.mixer.music.pause()
            self.game.paused=True
            for i in zombieEating_ogg:i.play()
            losemusic_ogg[0].play()
            losemusic_ogg[1].play()
            lose=getImageSource('images/widget/失败.png')
            screen.blit(lose,((screen.get_width()-lose.get_width())/2,(screen.get_height()-lose.get_height())/2))   
        
    def dieanimation(self):
        if self.deadindex<len(self.die[self.dead-1]):
            frame=self.die[self.dead-1][math.floor(self.deadindex)]
            if self.dead==1:screen.blit(frame, (self.x+10, self.y+20))
            elif self.dead==2:screen.blit(frame, (self.x+70, self.y+55))
            self.deadindex+=0.15
        else:
            self.distory()
            random.choice(zombie_falling_ogg).play()

    def distory(self):
        if self.sunval!=0:self.game.Suns.append(Sun(self.sunval,(self.x+45,self.y+80),self.game))
        self.game.Zombies.remove(self)
        self.game.zombiesInload[game.loadzombies[self.y]].remove(self)
        self.game.curScore+=1
        
class NomalZ(Zombie):
    def __init__(self,y,game) -> None:
        super().__init__(y,self,game,0)
        self.y=y
        self.game=game
        self.image_index = 0
        self.fps=4.5
        self.images=self.zombies[0][0]
        self.rect = pygame.Rect(self.x+100,self.y,20,48)

class RoadZ(Zombie):
    def __init__(self, y,game) -> None:
        super().__init__(y, self,game,1)    
        self.y=y
        self.game=game
        self.blood=640
        self.sunval=25
        self.fps=5.5
        self.image_index = 0
        self.images=self.zombies[1][0]
        self.rect = pygame.Rect(self.x+100,self.y,20,48) 

class IronBZ(Zombie):
    def __init__(self, y,game) -> None:
        super().__init__(y, self,game, 2)
        self.y=y
        self.game=game
        self.blood=1300
        self.sunval=100
        self.fps=5.5
        self.image_index = 0
        self.hiteffect=ironHit_ogg
        self.images=self.zombies[2][0]
        self.rect = pygame.Rect(self.x+100,self.y,20,48) 

class Game:
    def __init__(self) -> None:
        self.first=True
        self.tick=0
        self.playSun=25
        self.curScore=0
        self.endScore=0
        self.flag=True
        self.begining=False
        self.zombierule=dict()
        self.ZombiesType=[NomalZ]
        self.zombiestime={660:1,1200:2,3000:3,4800:5,7200:7,9600:8,12000:15}
        for key,value in self.zombiestime.items():
            for i in range(value):
                self.endScore+=1
                self.zombierule[key+180*i]=1
        self.background = pygame.transform.scale(getImageSource('images/scene/白天.jpg'), (1400, 600))
        self.plantmenu =getImageSource('images/widget/菜单栏/植物商店.png')
        self.shovelslot=pygame.transform.scale(getImageSource('images/widget/菜单栏/铲子槽.png'),(90,50))
        self.shovel=getImageSource('images/widget/菜单栏/铲子.png')
        self.shovelpos=(461,9)
        self.plantpos=(-100,-100)
        self.menu=getImageSource('images/widget/菜单栏/按钮.png')
        self.menuRect=self.menu.get_rect(topleft=(680, 0))
        self.shovelactive=False
        self.readysetplant_ogg=getSoundEffect('sounds/readysetplant.ogg')

        self.curplant=None
        self.lastcard=None
        self.colload={20:1,102:2,184:3,266:4,348:5,430:6,512:7,594:8,676:9}
        self.rowload={95:1,191:2,287:3,383:4,479:5}
        self.loadzombies={20:1,116:2,212:3,308:4,404:5}
        self.zombiesInload={1:[],2:[],3:[],4:[],5:[]}
        self.plantsInload={1:[],2:[],3:[],4:[],5:[]}
        self.Cards=[]
        self.plantcards={
            'images/向日葵/0.png':Sunflower,
            'images/豌豆射手/0.png':PeasShoter,
            'images/双重射手/0.png':Repeater,
            'images/火爆辣椒/0.png':SpicyChili,
            'images/坚果/0.png':NutsWall,
            'images/土豆地雷/0.png':PotatoMine,
            'images/樱桃炸弹/0.png':CherryBomb
        }
        i=0
        for key,value in self.plantcards.items():
            self.Cards.append(Card(key,value,value.getprice(),value.getcooltime(),self,90+50*i))
            i+=1
        self.Peass=[]
        self.lawns = [[Lawn(20 + (82 * x), 95 + (96 * y),self) for x in range(9)] for y in range(5)]
        self.Plants = []
        self.Suns = []
        self.Zombies=[]
        self.Cars=[Car(-30,y+35,self) for y in self.rowload.keys()]
        self.paused = False
            
    def update(self):
        screen.blit(self.background, (-220, 0))
        screen.blit(self.plantmenu, (10, 0))
        screen.blit(self.shovelslot, (456, 0))
        screen.blit(self.menu, (680, 0))
        screen.blit(scoretext.render(str(self.playSun), True, (0, 0, 0)), (26, 62))
        screen.blit(menutext.render('菜单', True, (0, 255, 0)), (715, 8))
        shovelpos=self.shovelpos if self.shovelactive else (463,9)
        screen.blit(self.shovel,shovelpos)
        
        for car in self.Cars:
            car.draw()
        for card in self.Cards:
            card.draw()
        for plant in self.Plants:
            plant.draw()
            plant.shot()
        for sun in self.Suns:
            sun.draw()
        for i in range(1,6):
            zombies=self.zombiesInload[i]
            if zombies:
                for zombie in zombies:
                    zombie.draw()
        for peas in self.Peass:
            peas.draw()
        if self.curplant and self.curplant!='displant':screen.blit(self.curplant.getimage(),self.plantpos)  

    def logical(self):
        #出僵尸，阳光
        if self.tick==3000:self.ZombiesType.append(RoadZ)
        elif self.tick==7200:self.ZombiesType.append(IronBZ)
        if self.tick in self.zombierule:
            print(self.tick)
            if self.first:
                zombieComing_ogg.play()
                self.first=False
            zombie=random.choice(self.ZombiesType)
            self.Zombies.append(zombie(20+96*random.randint(0,4),self))
        elif self.tick%1200==0:
            self.Suns.append(Sun(50,(random.randrange(60,750),random.randrange(150,450)),self,True))
        #僵尸叫
        if self.Zombies and random.randrange(1000)==0:
            random.choice(zombieGroan_ogg).play()
        #胜利
        if self.curScore==self.endScore:
            winmusic_ogg.play()
            self.paused=True

    def playmusic(self):
        pygame.mixer.music.load(random.choice(backgroundmusic))
        pygame.mixer.music.play(-1)

    def gamebegin(self):
        mainmenuBgm_ogg.stop()
        self.begining=True
        self.readysetplant_ogg.play()
        for i in [getImageSource('images/widget/关卡/StartReady.png'),getImageSource('images/widget/关卡/StartSet.png'),getImageSource('images/widget/关卡/StartPlant.png')]:
            self.update()
            screen.blit(i,((800-i.get_width())/2,(600-i.get_height())/2))
            pygame.display.flip()
            pygame.time.wait(500)
        self.playmusic()
        while self.flag:
            if not self.paused:
                self.logical()
                self.update()
                self.tick+=1
            for event in pygame.event.get():
                if not self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for sun in self.Suns:
                                if sun.rect.collidepoint(event.pos):
                                    sun.pickup()
                                    break
                            else:
                                self.shovelactive=False
                                if self.shovel.get_rect(topleft=(464, 9)).collidepoint(event.pos):
                                    if self.shovelactive:
                                        self.shovelactive=False
                                        self.curplant=None
                                    else:
                                        if self.lastcard:self.lastcard.selected=None
                                        self.curplant='displant'
                                        shovel_ogg.play()
                                        self.shovelactive=True
                                elif self.menuRect.collidepoint(event.pos):
                                    menu.flag=True
                                    menu.button=menu.button0
                                    menu.draw()
                                for card in self.Cards:
                                    if card.rect.collidepoint(event.pos):
                                        if self.playSun>=int(card.price) and card.curtime=='0':
                                            if card.selected:
                                                self.lastcard=card.selected=self.curplant=None
                                            else:
                                                if self.lastcard:self.lastcard.selected=None
                                                plantSlot_ogg.play()
                                                card.selected=getImageSource('images/widget/已被选.png')
                                                self.lastcard=card
                                                self.curplant=card.plant
                                        else:invalidClick_ogg.play()
                                for row in self.lawns:
                                    for lawn in row:
                                        pos=lawn.getpos()
                                        p=self.lawns[self.rowload[pos[1]]-1][self.colload[pos[0]]-1]
                                        if lawn.rect.collidepoint(event.pos) and self.curplant=='displant' and p.plant:
                                            if p.plant.sunprice!=0:self.Suns.append(Sun(p.plant.sunprice//2,pos,self))
                                            p.displanting()
                                            random.choice(plant_ogg).play()
                                            self.curplant=None
                                        elif lawn.rect.collidepoint(event.pos) and self.curplant and self.curplant!='displant' and self.lastcard.curtime=='0' and self.playSun >= self.curplant.getprice():
                                            if lawn.planting(self.curplant(pos,self)):
                                                self.playSun -= self.curplant.getprice()
                                                self.curplant=None
                                                self.lastcard.curtime=self.lastcard.cooltime
                                                self.lastcard.selected=None
                                            break
                                            
                    elif event.type==pygame.MOUSEMOTION:
                        if self.curplant and self.curplant!='displant':self.plantpos=(event.pos[0]-30,event.pos[1]-40)
                        else:self.plantpos=(-100,-100)
                        if self.shovelactive:self.shovelpos=event.pos
                        else:self.shovelpos=(463,9)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        menu.flag=True
                        menu.button=menu.button0
                        menu.draw()  
            pygame.display.flip()
            clock.tick(60)

class RWconfig:
    def __init__(self) -> None:
        with open('config.json','r') as f:
            self.config=json.load(f)
        self.rconfig()

    def rconfig(self):
        self.name=self.config['user']['name']

    def wconfig(self,zone,name,value):
        with open('config.json','w') as f:
            self.config[zone][name]=value
            json.dump(self.config,f,indent=4)

class Menu:
    def __init__(self,game) -> None:
        self.flag=True
        self.game=game
        self.pause_ogg=getSoundEffect('sounds/pause.ogg')
        self.menu=getImageSource('images/widget/菜单栏/options_menuback.png')
        self.button0=getImageSource('images/widget/菜单栏/options_backtogamebutton0.png')
        self.button1=getImageSource('images/widget/菜单栏/options_backtogamebutton1.png')
        self.button=self.button0
        self.buttonRect=self.button.get_rect(topleft=(220,432))

    def updata(self):
        screen.blits([
            (self.menu,(188.5,51)),
            (self.button,(220,432)),
            (tittletext.render('返回',True,(0,255,0)),(350,452))
        ])
        pygame.display.flip()

    def draw(self):
        if self.game.begining:
            self.pause_ogg.play()
            self.game.pause=True
        while self.flag:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if self.buttonRect.collidepoint(event.pos):
                        buttonClick_ogg.play()
                        self.button=self.button1
                        self.updata()
                        self.flag=False
                        if self.game.flag:self.game.pause=False
                else:
                    self.updata()

class MainMenu:
    def __init__(self,game) -> None:
        self.flag=True
        self.game=game
        mainmenuBgm_ogg.set_volume(0.2)
        mainmenuBgm_ogg.play()
        self.menuClick_ogg=getSoundEffect('sounds/bleep.ogg')

        #开屏界面
        self.load=250
        self.loading=True
        self.tittlescreen=getImageSource('images/主界面/titlescreen.jpg')
        self.popcap=getImageSource('images/主界面/PopCap_Logo.png')
        self.popcap=pygame.transform.scale(self.popcap,(150,150))
        self.pvzlogo=getImageSource('images/主界面/PvZ_Logo.png')
        self.loadbar=getImageSource('images/主界面/LoadBar_dirt.png')
        self.loadgrass=getImageSource('images/主界面/LoadBar_grass.png')
        self.angle=0
        self.rollcapimage=getImageSource('images/主界面/SodRollCap.png')

        #主界面
        self.center=getImageSource('images/主界面/center.png')
        self.BG=pygame.transform.scale(getImageSource('images/主界面/SelectorScreen_BG.png'),(800,600))
        self.left=getImageSource('images/主界面/left.png')
        self.right=getImageSource('images/主界面/right.png')
        self.hello=getImageSource('images/主界面/SelectorScreen_WoodSign1.png')
        self.save0=getImageSource('images/主界面/SelectorScreen_WoodSign2.png')
        self.save1=getImageSource('images/主界面/SelectorScreen_WoodSign2_press.png')
        self.save=self.save1
        self.saveRect=self.save1.get_rect(topleft=(20,135))
        self.grass=getImageSource('images/主界面/SelectorScreen_Leaves.png')
        self.leaf1=getImageSource('images/主界面/SelectorScreen_Leaf4.png')
        self.leaf2=getImageSource('images/主界面/SelectorScreen_Leaf5.png')
        self.leaf3=getImageSource('images/主界面/SelectorScreen_Leaf3.png')
        self.leaf4=getImageSource('images/主界面/SelectorScreen_Leaf1.png')
        self.flower1=getImageSource('images/主界面/SelectorScreen_Flower1.png')
        self.flower2=getImageSource('images/主界面/SelectorScreen_Flower2.png')
        self.flower3=getImageSource('images/主界面/SelectorScreen_Flower3.png')
        self.help0=getImageSource('images/主界面/SelectorScreen_Help1.png')
        self.help1=getImageSource('images/主界面/SelectorScreen_Help2.png')
        self.help=self.help0
        self.helpRect=self.help0.get_rect(topleft=(648,525))
        self.option0=getImageSource('images/主界面/SelectorScreen_Options1.png')
        self.option1=getImageSource('images/主界面/SelectorScreen_Options2.png')
        self.option=self.option0
        self.optionRect=self.option0.get_rect(topleft=(563,487))
        self.exit0=getImageSource('images/主界面/SelectorScreen_Quit1.png')
        self.exit1=getImageSource('images/主界面/SelectorScreen_Quit2.png')
        self.exit=self.exit0
        self.exitRect=self.exit0.get_rect(topleft=(720,515))
        self.rename=getImageSource('images/主界面/rename.png')

        #游戏选择
        self.adventure0=getImageSource('images/主界面/SelectorScreen_StartAdventure_Button.png')
        self.adventure1=getImageSource('images/主界面/SelectorScreen_StartAdventure_Highlight.png')
        self.adventure=self.adventure0
        self.adventureRect=pygame.Rect(404,55,self.adventure.get_width(),self.adventure.get_height()-25)

        self.small0=getImageSource('images/主界面/SelectorScreen_Survival_button.png')
        self.small1=getImageSource('images/主界面/SelectorScreen_Survival_Highlight.png')
        self.small=self.small0
        self.smallRect=pygame.Rect(405,185,self.small.get_width(),self.small.get_height()-50)

        self.challeng0=getImageSource('images/主界面/SelectorScreen_Challenges_button.png')
        self.challeng1=getImageSource('images/主界面/SelectorScreen_Challenges_Highlight.png')
        self.challeng=self.challeng0
        self.challengRect=pygame.Rect(412,275,self.challeng.get_width(),self.challeng.get_height()-45)

        self.survival0=getImageSource('images/主界面/SelectorScreen_Vasebreaker_button.png')
        self.survival1=getImageSource('images/主界面/SelectorScreen_Vasebreaker_Highlight.png')
        self.survival=self.survival0
        self.survivalRect=pygame.Rect(450,340,self.survival.get_width(),self.survival.get_height()-45)

        #帮助
        self.helpering=True
        self.words=getImageSource('images/主界面/says.png')
        self.wordsbg=pygame.transform.scale(getImageSource('images/主界面/saysbg.jpg'),(800,600))
        self.backmenu0=getImageSource('images/主界面/return.png')
        self.backmenu1=getImageSource('images/主界面/return1.png')
        self.backmenu=self.backmenu0
        self.backmenuRect=self.backmenu.get_rect(topleft=(322,520))

        #读取配置
        self.naming=True
        self.typing=''
        self.name=rwconfig.name
        self.confirm=pygame.Rect(190,331,204,44)
        self.cancel=pygame.Rect(410,331,204,44)

    def init(self):
        def updata():
            screen.blits([
                (self.tittlescreen,(0,0)),
                (self.pvzlogo,(60,30)),
                (self.popcap,(-10,-10)),
                (self.loadbar,((800-self.loadbar.get_width())//2,500)),
                (self.loadgrass,((800-self.loadbar.get_width())//2,480))     
            ])
        while self.loading and self.load<=533:
            updata()
            screen.blit(menutext.render('请等待加载',True,(255, 215, 0)),(345,510))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type==pygame.KEYUP or event.type==pygame.MOUSEBUTTONUP:
                    self.loading=False
            rollcap = pygame.transform.rotate(self.rollcapimage, self.angle)
            new_rect = rollcap.get_rect(center=(self.load, 470))
            screen.blit(rollcap, new_rect.topleft)
            self.angle -= 0.3
            self.load += 0.2
            pygame.display.flip()
        updata()
        screen.blit(menutext.render('任意操作以开始游戏',True,(255, 215, 0)),(295,510))
        self.draw()
    
    def click(self):
        if not self.typing:
            invalidClick_ogg.play()
        else:return True

    def setname(self):
        while self.naming:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type==pygame.KEYDOWN:
                    leng=len(self.typing)
                    if event.key==8 and leng>0:
                        self.typing=self.typing[:-1]
                    elif event.key in range(K_a,K_z+1) and leng<=10:
                        self.typing+=chr(event.key)
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if self.confirm.collidepoint(event.pos):
                        if self.click():
                            rwconfig.wconfig('user','name',self.typing)
                            self.name=self.typing
                            self.typing=''
                            self.naming=False
                    elif self.cancel.collidepoint(event.pos):
                        if self.click():self.naming=False
                screen.blits([
                    (self.rename,(154,104)),
                    (pygame.transform.scale(self.game.menu,(204,44)),(190,331)),
                    (pygame.transform.scale(self.game.menu,(204,44)),(410,331)),
                    (menutext.render('确定',True,(0, 255, 0)),(270,340)),
                    (menutext.render('取消',True,(0, 255, 0)),(490,340)),
                    (menutext.render(self.typing,True,(255, 215, 0)),(205,256))
                ])
                pygame.display.flip()

    def updatabutton(self,rect,currentstate,defaultimage,hoverimage,pos):
        if rect.collidepoint(pos):
            if currentstate == defaultimage:
                self.menuClick_ogg.play()
            return hoverimage
        return defaultimage

    def helper(self):
        while self.helpering:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if self.backmenuRect.collidepoint(event.pos):
                        self.helpering=False
                        self.flag=True
                        self.draw()
                else:
                    if event.type==pygame.MOUSEMOTION:
                        self.backmenu=self.updatabutton(self.backmenuRect,self.backmenu,self.backmenu0,self.backmenu1,event.pos)
                    screen.blits([
                        (self.wordsbg,(0,0)),
                        (self.words,(85,80)),
                        (self.backmenu,(322,520)),
                        (menutext.render('返回主页',True,(255, 215, 0)),(355,528))
                    ])
                    pygame.display.flip()

    def draw(self):
        while self.flag:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                else:
                    screen.blits([
                        (self.BG,(0,0)),
                        (self.center,(90,270)),
                        (self.left,(0,-70)),
                        (self.right,(70,40)),
                        (self.hello,(20,0)),
                        (self.save,(20,135)),
                        (self.grass,(0,538)),
                        (self.leaf1,(220,562)),
                        (self.leaf3,(255,550)),
                        (self.leaf2,(248,572)),
                        (self.leaf4,(287,565)),
                        (menutext.render(self.name,True,(255, 215, 0)),(150,90))
                    ])  
                    screen.blits([
                        (self.adventure,(405,55)),
                        (self.small,(405,168)),
                        (self.challeng,(412,255)),
                        (self.survival,(410,325)),
                        (self.flower1,(682,415)),
                        (self.flower2,(637,435)),
                        (self.flower3,(735,457)),
                        (self.option,(563,487)),
                        (self.help,(648,525)),
                        (self.exit,(720,515))
                    ])
                
                if event.type == pygame.MOUSEMOTION:
                    self.adventure = self.updatabutton(self.adventureRect, self.adventure, self.adventure0, self.adventure1,event.pos)
                    self.small = self.updatabutton(self.smallRect, self.small, self.small0, self.small1,event.pos)
                    self.challeng = self.updatabutton(self.challengRect, self.challeng, self.challeng0, self.challeng1,event.pos)
                    self.survival = self.updatabutton(self.survivalRect, self.survival, self.survival0, self.survival1,event.pos)
                    self.option = self.updatabutton(self.optionRect, self.option, self.option0, self.option1,event.pos)
                    self.help = self.updatabutton(self.helpRect, self.help, self.help0, self.help1,event.pos)
                    self.exit = self.updatabutton(self.exitRect, self.exit, self.exit0, self.exit1,event.pos)
                    self.save = self.updatabutton(self.saveRect, self.save, self.save0, self.save1,event.pos)

                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if self.adventureRect.collidepoint(event.pos):
                        self.flag=False
                        self.game.gamebegin()
                    elif self.saveRect.collidepoint(event.pos):
                        self.naming=True
                        self.setname()
                    elif self.exitRect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    elif self.helpRect.collidepoint(event.pos):
                        self.flag=False
                        self.helpering=True
                        self.helper()
                    elif self.optionRect.collidepoint(event.pos):
                        menu.flag=True
                        menu.button=menu.button0
                        menu.draw()
                if self.name=='':
                    self.setname()
            pygame.display.flip()

def getImageSource(path):
    return pygame.image.load(path)

def getSoundEffect(path):
    return pygame.mixer.Sound(path)

if __name__=='__main__':
    pygame.init()
    pygame.mixer.init()
    scoretext = pygame.font.Font('font/digit.ttf', 15)
    pricetext = pygame.font.Font('font/digit.ttf', 13)
    menutext=pygame.font.Font('font/fzsr.ttf',22)
    tittletext=pygame.font.Font('font/fzsr.ttf',48)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('PvZ test')
    icon = getImageSource('images/icon.png')
    pygame.display.set_icon(icon)
    plantDead_ogg=getSoundEffect('sounds/bigchomp.ogg')
    zombieComing_ogg=getSoundEffect('sounds/awooga.ogg')
    zombieEating_ogg=[
        getSoundEffect(path) for path in (
            'sounds/chomp.ogg',
            'sounds/chomp2.ogg',
            'sounds/chompsoft.ogg'
        )
    ]
    zombieGroan_ogg=[
        getSoundEffect(path) for path in (
            'sounds/groan.ogg',
            'sounds/groan2.ogg',
            'sounds/groan3.ogg',
            'sounds/groan4.ogg',
            'sounds/groan5.ogg',
            'sounds/groan6.ogg',
            'sounds/lowgroan.ogg',
            'sounds/lowgroan2.ogg'
        )
    ]
    buttonClick_ogg=getSoundEffect('sounds/buttonClick.ogg')
    mainmenuBgm_ogg=getSoundEffect('sounds/bgm/Laura Shigihara - Crazy Dave.ogg')
    losemusic_ogg=[
        getSoundEffect(path) for path in (
            'sounds/losemusic.ogg',
            'sounds/scream.ogg'
        )
    ]
    winmusic_ogg=getSoundEffect('sounds/winmusic.ogg')
    plant_ogg=[
        getSoundEffect(path) for path in (
            'sounds/plant.ogg',
            'sounds/plant2.ogg'
        )
    ]
    splat_ogg=[
        getSoundEffect(path) for path in (
            'sounds/splat.ogg',
            'sounds/splat2.ogg',
            'sounds/splat3.ogg'
        )
    ]
    ironHit_ogg=[
        getSoundEffect(path) for path in (
            'sounds/shieldhit.ogg',
            'sounds/shieldhit.ogg'
        )
    ]
    zombie_falling_ogg=[
        getSoundEffect(path) for path in (
            'sounds/zombie_falling_1.ogg',
            'sounds/zombie_falling_1.ogg'
        )
    ]
    backgroundmusic=[
        'sounds/bgm/Brainiac Maniac-Laura Shigihara.mp3',
        'sounds/bgm/Graze the Roof-Laura Shigihara.mp3',
        'sounds/bgm/Grasswalk.mp3',
        'sounds/bgm/Loonboon-Laura Shigihara.mp3',
        'sounds/bgm/Moongrains-Laura Shigihara.mp3',
        'sounds/bgm/Rigor Mormist-Laura Shigihara.mp3',
        'sounds/bgm/Ultimate Battle-Laura Shigihara.mp3',
        'sounds/bgm/Watery Graves-Laura Shigihara.mp3'
    ]

    pickup_ogg=getSoundEffect('sounds/points.ogg')
    shoot_ogg=[
        getSoundEffect(path) for path in (
            'sounds/kernelpult.ogg',
            'sounds/kernelpult2.ogg'
        )
    ]
    car_ogg=getSoundEffect('sounds/lawnmower.ogg')
    invalidClick_ogg=getSoundEffect('sounds/buzzer.ogg')
    shovel_ogg=getSoundEffect('sounds/shovel.ogg')
    plantSlot_ogg=getSoundEffect('sounds/seedlift.ogg')
    rwconfig=RWconfig()
    game=Game()
    menu=Menu(game)
    mainmenu=MainMenu(game)
    mainmenu.init()