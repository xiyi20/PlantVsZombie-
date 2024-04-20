import sys
import json
import math
import random
import pygame
import threading
import pygame.mixer
from pygame.locals import K_a,K_z


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
            self.game.plantsInroad[self.row].append(plant)
            random.choice(plant_ogg).play()
            return True
        return False

    def displanting(self):
        if self.plant:
            self.game.Plants.remove(self.plant)
            self.game.plantsInroad[self.row].remove(self.plant)
            self.plant=None

class Card:
    def __init__(self,img,plant,price,cooltime,game,x=200) -> None:
        self.img=img
        self.plant=plant
        self.selected=None
        self.price=str(price)
        self.coolimage=objectType[11]
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
        if self.selected:screen.blit(self.selected,(self.x,8))
        if self.curtime!='0':
            screen.blit(pygame.transform.scale(self.coolimage,(50,int(self.curtime)*self.interval)),(self.x,7))
            self.curtime=str(int(self.curtime)-1)

class Coin:
    def __init__(self,x,y,game,type=0) -> None:
        self.x=x
        self.y=y
        self.val=50
        self.pick=False
        self.first=True
        self.xspeed=0
        self.yspeed=0
        self.game=game
        self.tick=0
        self.fall_ogg=coinfall_ogg if type==0 else diamondfall_ogg
        self.pick_ogg=coinpick_ogg
        self.image=objectType[12]
        self.rect=self.image.get_rect(topleft=(self.x,self.y))
        self.endRect=pygame.Rect(48,580,20,20)
        if self.fall_ogg:
            self.fall_ogg.play()

    def draw(self):
        if self.pick:
            if self.first:
                self.first=False
                if self.pick_ogg:self.pick_ogg.play()
                self.xspeed=(10-self.x)/60
                self.yspeed=(580-self.y)/60
            self.x+=self.xspeed
            self.y+=self.yspeed       
            if self.rect.colliderect(self.endRect):self.pickup()
        self.tick+=1
        screen.blit(self.image,(self.x,self.y))
        self.rect=self.image.get_rect(topleft=(self.x,self.y))
        if self.tick==1200:self.game.Coins.remove(self)

    def pickup(self):
        self.game.money+=self.val
        rwconfig.wconfig('user','money',self.game.money)
        self.game.Coins.remove(self)

class SilverCoin(Coin):
    def __init__(self, x, y,game) -> None:
        super().__init__(x, y,game)

class GoldCoin(Coin):
    def __init__(self, x, y,game) -> None:
        super().__init__(x, y,game)
        self.val=100
        self.image=objectType[13]    

class Diamond(Coin):
    def __init__(self, x, y,game) -> None:
        super().__init__(x, y,game,1)
        self.val=300
        self.fall_ogg=diamondfall_ogg
        self.pick_ogg=diamondpick_ogg
        self.image=objectType[14]  

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
        self.image=objectType[0]
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

    def draw(self):
        for zombie in game.zombiesInroad[game.rowload[self.y-35]]:
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
        self.cury=50
        self.targety=pos[1]
        self.game=game
        self.falling=falling
        self.image_index = 0
        self.life=900
        self.tick=0
        self.pick=False
        self.images=objectType[1]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.endRect=pygame.Rect(0,0,20,20)
    
    def draw(self):
        if not self.pick:
            if self.falling and self.tick%2==0 and self.cury<self.targety:
                self.cury+=1.5
                self.y=self.cury
            else:self.y=self.cury if self.falling else self.targety
        else:
            self.x+=(-self.x)/30
            self.y+=(-10-self.y)/30
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        if self.rect.colliderect(self.endRect):self.pickup()
        if self.tick%4==0:self.image_index = (self.image_index+1) % len(self.images)
        self.tick+=1
        if self.tick==self.life:game.Suns.remove(self)  
        screen.blit(self.images[self.image_index], (self.x, self.y+20))    

    def pickup(self):
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
        self.image=objectType[2]
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),140)
        random.choice(shoot_ogg).play()

    def draw(self):
        screen.blit(self.image,(self.x,self.y))
        self.x+=self.speed
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        for zombie in game.zombiesInroad[game.rowload[self.y-5]]:
            if zombie.rect.colliderect(self.rect) and zombie.blood>0:
                zombie.blood -= self.damm
                random.choice(zombie.hiteffect).play()
                self.game.Peass.remove(self)
                if zombie.blood <= 0:zombie.dead=1
                break
        if self.x>=self.distorypos and self in self.game.Peass:
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

class SunFlower(Plant):
    sunprice=25
    image='images/向日葵/0.png'
    def __init__(self,pos,game):
        super().__init__(pos[0],pos[1],game)
        self.x = pos[0]
        self.y = pos[1]
        self.game=game
        self.image_index = 0
        self.images =plantType[0]
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
        self.images = plantType[1]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        
    def shot(self):
        if game.zombiesInroad[self.row]:
            for zombie in game.zombiesInroad[self.row]:
                if self.x-30<=zombie.x<=700:
                    if self.tick%self.interval==0:
                        self.game.Peass.append(Peas(self.x,self.y,self.game,self.damm))
                        break
                
class Repeater(Plant):
    sunprice=200
    image='images/双重射手/0.png'
    def __init__(self,pos,game) -> None:
        super().__init__(pos[0],pos[1],game)
        self.x = pos[0]
        self.y = pos[1]
        self.game=game
        self.row=self.game.rowload[self.y]
        self.damm=20
        self.image_index = 0
        self.images = plantType[2]
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        
    def shot(self):
        if game.zombiesInroad[self.row]:
            for zombie in game.zombiesInroad[self.row]:
                if self.x-30<=zombie.x<=700:
                    if self.tick%self.interval in [0,10]:
                        self.game.Peass.append(Peas(self.x,self.y,self.game,self.damm))
                        break

class SpicyChili(Plant):
    sunprice=125
    cooling=3000
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
        self.images=plantType[3]
        self.rect=pygame.Rect(self.x,self.y,self.images[0].get_width(),self.images[0].get_height())
        self.boom_index=0
        self.boomimages=plantType[4]
        self.boomRect=pygame.Rect(50,self.y,730,self.images[0].get_height())
    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(self.image_index)], (self.x+10,self.y-5))
            self.image_index+=0.25
            if self.image_index==len(self.images):
                self.booming=True
                self.spicy_ogg.play()
                for zombie in self.game.zombiesInroad[self.row]:
                    if zombie.blood>0:
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
        self.images= plantType[5]
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
        self.boom1=objectType[3]
        self.boom2=objectType[4]
        self.images0=objectType[5]
        self.images1=plantType[6]
        self.images=self.images0
        self.rect=pygame.Rect(pos[0],pos[1],self.images1[0].get_width(),self.images1[0].get_height())
    
    def draw(self):
        tem=[]
        if not self.booming:
            if self.tick%13==0:
                self.image_index = (self.image_index+1) % len(self.images)
            if self.tick==900:
                self.active=True
                potatoActive_ogg.play()
                self.x,self.y=self.x-18,self.y-20
                self.images=self.images1
            screen.blit(self.images[self.image_index],(self.x,self.y))
            self.tick+=1
            for zombie in self.game.zombiesInroad[self.row]:
                if self.rect.colliderect(zombie.rect) and self.active:
                    self.booming=True
                    potatoBoom_ogg.play()
                    for zombie in self.game.zombiesInroad[self.row]:
                        if -25<zombie.x-self.x+30<25:tem.append(zombie)
                    for i in tem:
                        if i.blood>0:
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
    cooling=3000
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
        self.image_index=0
        self.images=plantType[7]
        self.rect=pygame.Rect(self.x,self.y,self.images[0].get_width(),self.images[0].get_height())
        self.boomtime=0
        self.boomimage=objectType[6]
        self.boomRect=pygame.Rect(self.x-70,self.y-30,200,130)
    def draw(self):
        if not self.booming:
            screen.blit(self.images[math.floor(self.image_index)], (self.x-10,self.y-5))
            self.image_index+=0.25
            if self.image_index==len(self.images):
                self.booming=True
                cherryBoom_ogg.play()
                for zombie in self.game.Zombies:
                    if self.boomRect.colliderect(zombie.rect) and zombie.blood>0:
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
    def __init__(self,y,zombie,game,type:int) -> None:
        self.x=780
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
        self.state='walk'
        self.fps=4
        self.hiteffect=splat_ogg
        self.laststate=None
        self.game.zombiesInroad[self.row].append(zombie)
        self.images=None
        self.type=zombieType[type]
        self.die=[objectType[7],objectType[8]]
        self.head=objectType[9]

    def draw(self):
        if self.dead==0:
            self.state='eat' if self.eating else 'walk'
            for plant in game.plantsInroad[self.row]:
                if self.rect.colliderect(plant.rect):
                    self.eating=plant
                    self.state='eat'
                    self.resetstate()
                    break
            if self.state=='walk':
                self.images=self.type[0]
                self.x-=self.speed
                self.rect=pygame.Rect(self.x+100, self.y, 20, self.images[0].get_height())
            else:
                self.images=self.type[1]
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
        
    def dieanimation(self):
        if self.deadindex<len(self.die[self.dead-1]):
            curindex=math.floor(self.deadindex)
            bodyframe=self.die[self.dead-1][curindex]
            if self.dead==1:
                headframe=self.head[math.floor(self.deadindex+0.05)]
                screen.blit(headframe, (self.x+60, self.y+5))
                screen.blit(bodyframe, (self.x+10, self.y+20))
            elif self.dead==2:screen.blit(bodyframe, (self.x+70, self.y+55))
            self.deadindex+=0.15
        else:
            self.distory()
            random.choice(zombie_falling_ogg).play()

    def distory(self):
        choose=random.randrange(100)
        if 0<choose<=10:
            if 5<choose<=10:money=SilverCoin(self.x+60,self.y+120,self.game)
            elif 3<choose<=5:money=GoldCoin(self.x+60,self.y+120,self.game)
            elif 0<choose<=3:money=Diamond(self.x+60,self.y+120,self.game)
            self.game.Coins.append(money)
        if self.sunval!=0:self.game.Suns.append(Sun(self.sunval,(self.x+45,self.y+80),self.game))
        self.game.Zombies.remove(self)
        self.game.zombiesInroad[game.loadzombies[self.y]].remove(self)
        self.game.curScore+=1
        self.game.wonpos=[self.x+30,self.y+90]
        
class NomalZ(Zombie):
    def __init__(self,y,game) -> None:
        super().__init__(y,self,game,0)
        self.y=y
        self.game=game
        self.image_index = 0
        self.fps=4.5
        self.rect = pygame.Rect(self.x+100,self.y,20,48)

class RoadZ(Zombie):
    def __init__(self, y,game) -> None:
        super().__init__(y, self,game,1)    
        self.y=y
        self.game=game
        self.blood=640
        self.fps=5.5
        self.image_index = 0
        self.rect = pygame.Rect(self.x+100,self.y,20,48) 

class IronBZ(Zombie):
    def __init__(self, y,game) -> None:
        super().__init__(y, self,game, 2)
        self.y=y
        self.game=game
        self.blood=1300
        self.fps=5.5
        self.image_index = 0
        self.hiteffect=ironHit_ogg
        self.rect = pygame.Rect(self.x+100,self.y,20,48) 

class Game:
    def __init__(self) -> None:
        self.endRect=pygame.Rect(310,241,40,40)
        self.background = pygame.transform.scale(getImageSource('images/scene/白天.jpg'), (1400, 600))
        self.moneybag=getImageSource('images/widget/关卡/moneybag.png')
        self.plantmenu =getImageSource('images/widget/菜单栏/植物商店.png')
        self.shovelslot=getImageSource('images/widget/菜单栏/铲子槽.png')
        self.shovel=getImageSource('images/widget/菜单栏/铲子.png')
        self.shovelpos=(447,-3)
        self.plantpos=(-100,-100)
        self.menu=getImageSource('images/widget/菜单栏/按钮.png')
        self.menuRect=self.menu.get_rect(topleft=(680, 0))
        self.money=rwconfig.money
        self.coinbank=objectType[15]
        self.readysetplant_ogg=getSoundEffect('sounds/readysetplant.ogg')
        self.colload={20:1,102:2,184:3,266:4,348:5,430:6,512:7,594:8,676:9}
        self.rowload={95:1,191:2,287:3,383:4,479:5}
        self.loadzombies={20:1,116:2,212:3,308:4,404:5}
        self.plantcards={
            'images/向日葵/0.png':SunFlower,
            'images/豌豆射手/0.png':PeasShoter,
            'images/双重射手/0.png':Repeater,
            'images/火爆辣椒/0.png':SpicyChili,
            'images/坚果/0.png':NutsWall,
            'images/土豆地雷/0.png':PotatoMine,
            'images/樱桃炸弹/0.png':CherryBomb
        }
        self.init() 

    def init(self):
        self.first=True
        self.tick=0
        self.playSun=25
        self.curScore=0
        self.flag=True
        self.begining=False
        self.animation=False
        self.alpha=0
        self.won=False
        self.wonflag=False
        self.wonpos=[550,350]
        self.zombierule=dict()
        self.ZombiesType=[NomalZ]
        self.zombiestime={60:1,1200:2,3000:3,4800:5,7200:7,9600:8,12000:15,15000:25}
        self.waves=list(self.zombiestime.keys())
        self.endScore=sum([i for i in self.zombiestime.values()])
        self.shovelactive=False
        self.curplant=None
        self.lastcard=None
        self.zombiesInroad={1:[],2:[],3:[],4:[],5:[]}
        self.plantsInroad={1:[],2:[],3:[],4:[],5:[]}
        self.Cards=[]
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
        self.Coins=[]
        self.paused = False 

    def win(self):
        if self.animation:
            mask = pygame.Surface((800, 600))
            mask.set_alpha(self.alpha)
            mask.fill((255,255,255))
            screen.blit(mask, (0, 0))
            self.alpha+=2
            if self.alpha>255:
                self.flag=False
                mainmenu.flag=True
                mainmenu.playmusic()
                mainmenu.draw()
        else:
            if self.wonflag:
                self.wonpos[0]+=(310-self.wonpos[0])/100
                self.wonpos[1]+=(241-self.wonpos[1])/100
            screen.blit(self.moneybag,self.wonpos)
            self.moneybagRect=self.moneybag.get_rect(topleft=self.wonpos)
            if self.moneybagRect.colliderect(self.endRect):
                ypos=[0,1,2,1,0]
                for i in range(5):
                    coin=GoldCoin(self.wonpos[0]-55+45*i,self.wonpos[1]-18*ypos[i],self)
                    coin.pick=True
                    self.Coins.append(coin)
                self.begining=False
                self.animation=True

    def update(self):
        screen.blit(self.background, (-220, 0))
        screen.blit(self.plantmenu, (10, 0))
        screen.blit(self.shovelslot, (456, 0))
        screen.blit(self.menu, (680, 0))
        screen.blit(scoretext.render(str(self.playSun), True, (0, 0, 0)), (26, 62))
        screen.blit(menutext.render('菜单', True, (0, 255, 0)), (715, 8))
        shovelpos=self.shovelpos if self.shovelactive else (447,-3)
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
            zombies=self.zombiesInroad[i]
            if zombies:
                for zombie in zombies:
                    zombie.draw()
        for peas in self.Peass:
            peas.draw()
        screen.blit(self.coinbank,(35,570))
        screen.blit(scoretext.render(str(self.money), True, (255, 215, 0)), (80, 578))
        for coin in self.Coins:
            coin.draw()
        screen.blit(self.shovel,shovelpos)
        if self.curplant and self.curplant!='displant':screen.blit(self.curplant.getimage(),self.plantpos)  

    def logical(self):
        #出僵尸，阳光
        if self.tick==3000:self.ZombiesType.append(RoadZ)
        elif self.tick==7200:self.ZombiesType.append(IronBZ)
        if self.tick in self.zombiestime:
            print('当前为第:',self.waves.index(self.tick)+1,' 波')
            interval=180 if self.tick<15000 else 90
            if self.tick==self.waves[-1]:
                self.waves.append(self.waves[-1]+3000)
                self.zombiestime[self.waves[-1]]=25
            for i in range(self.zombiestime[self.tick]):
                self.zombierule[self.tick+interval*i]=1
        if self.tick in self.zombierule:   
            if self.first:
                zombieComing_ogg.play()
                self.first=False
            zombie=random.choice(self.ZombiesType)
            self.Zombies.append(zombie(20+96*random.randint(0,4),self))
        if self.tick%1200==0:
            self.Suns.append(Sun(50,(random.randrange(60,750),random.randrange(50,450)),self,True))
        #僵尸叫
        if self.Zombies and random.randrange(1000)==0:
            random.choice(zombieGroan_ogg).play()
        #胜利
        if self.curScore==self.endScore and not self.loop:
            self.won=True
        #失败
        for zombie in self.Zombies:
            if zombie.x<=-100:
                pygame.mixer.music.pause()
                self.paused=True
                for i in zombieEating_ogg:i.play()
                losemusic_ogg[0].play()
                losemusic_ogg[1].play()
                lose=getImageSource('images/widget/失败.png')
                screen.blit(pygame.transform.scale(getImageSource('images/widget/遮罩.png'),(800,600)),(0,0))
                screen.blit(lose,((screen.get_width()-lose.get_width())/2,(screen.get_height()-lose.get_height())/2))

    def playmusic(self):
        pygame.mixer.music.load(random.choice(backgroundmusic))
        pygame.mixer.music.set_volume(rwconfig.gamevolume)
        pygame.mixer.music.play(-1)
    
    def gamebegin(self,loop=False):
        self.loop=loop
        mainmenuBgm_ogg.stop()
        self.begining=True
        self.readysetplant_ogg.play()
        for img in objectType[10]:
            self.update()
            screen.blit(img,((800-img.get_width())/2,(600-img.get_height())/2))
            pygame.display.flip()
            pygame.time.wait(500)
        self.playmusic()
        while self.flag:
            if not self.paused:
                self.update()
                self.logical()
                if self.won:self.win()
                self.tick+=1
            for event in pygame.event.get():
                if not self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for sun in self.Suns:
                                if sun.rect.collidepoint(event.pos):
                                    sun.pick=True
                                    pickup_ogg.play()
                                    break
                            for coin in self.Coins:
                                if coin.rect.collidepoint(event.pos):
                                    coin.pick=True
                                    break
                            if self.won and self.moneybagRect.collidepoint(event.pos):
                                self.wonflag=True
                                pygame.mixer.music.stop()
                                winmusic_ogg.play()
                            if self.shovel.get_rect(topleft=(464, 9)).collidepoint(event.pos):
                                if self.lastcard:self.lastcard.selected=None
                                self.curplant='displant'
                                shovel_ogg.play()
                                self.shovelactive=True
                            elif self.menuRect.collidepoint(event.pos):
                                menu.flag=True
                                menu.returnimg=menu.returnimg0
                                menu.draw()
                            for card in self.Cards:
                                if card.rect.collidepoint(event.pos):
                                    if self.playSun>=int(card.price) and card.curtime=='0':
                                        if card.selected:
                                            self.lastcard=card.selected=self.curplant=None
                                        else:
                                            if self.lastcard:self.lastcard.selected=None
                                            plantSlot_ogg.play()
                                            card.selected=card.coolimage
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
                                        self.shovelactive=False
                                        self.curplant=None
                                        break
                                    elif lawn.rect.collidepoint(event.pos) and self.curplant=='displant':
                                        if self.shovelactive:
                                            self.shovelactive=False
                                            self.curplant=None
                                        break
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
                        if self.shovelactive:self.shovelpos=(event.pos[0]-30,event.pos[1]-40)
                        else:self.shovelpos=(463,9)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
        self.money=self.config['user']['money']
        self.gamevolume=self.config['volume']['game']
        self.menuvolume=self.config['volume']['menu']

    def wconfig(self,zone,name,value):
        with open('config.json','w') as f:
            self.config[zone][name]=value
            json.dump(self.config,f,indent=4)
        self.rconfig()

class Menu:
    def __init__(self,game) -> None:
        self.flag=True
        self.game=game
        self.pause_ogg=getSoundEffect('sounds/pause.ogg')
        self.menu=getImageSource('images/widget/菜单栏/options_menuback.png')
        self.buttondown=False
        self.returnimg0=getImageSource('images/widget/菜单栏/options_backtogamebutton0.png')
        self.returnimg1=getImageSource('images/widget/菜单栏/options_backtogamebutton1.png')
        self.returnimg=self.returnimg0
        self.returnimgRect=self.returnimg.get_rect(topleft=(220,432))
        self.volumedown=False
        self.progress=getImageSource('images/widget/菜单栏/options_sliderslot.png')
        self.pointer=getImageSource('images/widget/菜单栏/options_sliderknob2.png')
        self.ispoint=False
        self.pointpos=(rwconfig.menuvolume/0.008775+350,208)
        self.button=pygame.transform.scale(game.menu,(200,41))
        self.againRect=pygame.Rect(295,333,200,41)
        self.mainmenuRect=pygame.Rect(295,375,200,41)


    def updata(self,y=452):
        screen.blits([
            (self.menu,(188.5,51)),
            (self.returnimg,(220,432)),
            (menutext.render('音乐',True,(107,109,145)),(300,210)),
            (self.progress,(350,218)),
            (self.pointer,self.pointpos),
            (tittletext.render('返回',True,(0,216,0)),(350,y))
        ])
        if self.game.begining:
            screen.blits([
                (self.button,(295,333)),
                (menutext.render('重新开始',True,(0,216,0)),(352,340)),
                (self.button,(295,375)),
                (menutext.render('主菜单',True,(0,216,0)),(365,383)),
            ])
        self.pointerRect=self.pointer.get_rect(topleft=self.pointpos)
        pygame.display.flip()

    def draw(self):
        if self.game.begining:
            self.pointpos=(rwconfig.gamevolume/0.008775+350,208)
            self.pause_ogg.play()
            self.game.pause=True
        while self.flag:
            for event in pygame.event.get():
                self.updata()
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    self.volumedown=True
                    if self.returnimgRect.collidepoint(event.pos):
                        buttonClick_ogg.play()
                        self.buttondown=True
                        self.returnimg=self.returnimg1
                        self.updata(454)
                    elif self.pointerRect.collidepoint(event.pos):
                        self.ispoint=True
                    elif self.game.begining and self.againRect.collidepoint(event.pos):
                        self.game.flag=False
                        self.game.init()
                        self.game.gamebegin()
                    elif self.game.begining and self.mainmenuRect.collidepoint(event.pos):
                        self.game.flag=False
                        self.game.begining=False
                        pygame.mixer.music.stop()
                        mainmenu.flag=True
                        mainmenu.playmusic()
                        mainmenu.draw()
                    else:
                        self.ispoint=False
                elif event.type==pygame.MOUSEBUTTONUP:
                    self.volumedown=False
                    self.ispoint=False
                    if self.returnimgRect.collidepoint(event.pos) and self.buttondown:
                        self.flag=False
                        self.buttondown=False
                        curvolume='menu'
                        if self.game.begining:
                            curvolume='game'
                            self.game.pause=False
                        rwconfig.wconfig('volume',curvolume,0.008775*(self.pointpos[0]-350))
                elif event.type==pygame.MOUSEMOTION:
                    if self.volumedown and self.ispoint:
                        x=min(max(361,event.pos[0]),474)
                        self.pointpos=(x-10,208)
                self.returnimg=self.returnimg0
        if not self.game.begining:
            mainmenuBgm_ogg.set_volume(rwconfig.menuvolume)
        else:
            pygame.mixer.music.set_volume(rwconfig.gamevolume)

class MainMenu:
    def __init__(self,game) -> None:
        self.flag=True
        self.game=game
        mainmenuBgm_ogg.set_volume(rwconfig.menuvolume)
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
        #冒险
        self.adventure0=getImageSource('images/主界面/SelectorScreen_StartAdventure_Button.png')
        self.adventure1=getImageSource('images/主界面/SelectorScreen_StartAdventure_Highlight.png')
        self.adventure=self.adventure0
        self.adventureRect=pygame.Rect(404,55,self.adventure.get_width(),self.adventure.get_height()-25)
        #小游戏
        self.small0=getImageSource('images/主界面/SelectorScreen_Survival_button.png')
        self.small1=getImageSource('images/主界面/SelectorScreen_Survival_Highlight.png')
        self.small=self.small0
        self.smallRect=pygame.Rect(405,185,self.small.get_width(),self.small.get_height()-50)
        #解密
        self.challeng0=getImageSource('images/主界面/SelectorScreen_Challenges_button.png')
        self.challeng1=getImageSource('images/主界面/SelectorScreen_Challenges_Highlight.png')
        self.challeng=self.challeng0
        self.challengRect=pygame.Rect(412,275,self.challeng.get_width(),self.challeng.get_height()-45)
        #生存
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
        self.name=rwconfig.name
        self.typing=self.name
        self.confirm=pygame.Rect(190,331,204,44)
        self.cancel=pygame.Rect(410,331,204,44)

    def playmusic(self):
        mainmenuBgm_ogg.play(-1)

    def init(self):
        self.playmusic()
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
                    sys.exit()
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

    def updata(self):
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

    def click(self,mode):
        val=self.name if mode==0 else self.typing
        if not val:
            invalidClick_ogg.play()
        else:
            menuClick_ogg.play()
            return True

    def setname(self):
        while self.naming:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    leng=len(self.typing)
                    if event.key==8 and leng>0:
                        self.typing=self.typing[:-1]
                    elif event.key in range(K_a,K_z+1) and leng<=10:
                        self.typing+=chr(event.key)
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if self.confirm.collidepoint(event.pos):
                        if self.click(1):
                            rwconfig.wconfig('user','name',self.typing)
                            self.name=self.typing
                            self.naming=False
                    elif self.cancel.collidepoint(event.pos):
                        if self.click(0):
                            self.typing=self.name
                            self.naming=False
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
        paper_ogg.play()
        while self.helpering:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
            self.updata()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEMOTION:
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
                        self.game.init()
                        self.game.gamebegin()
                    if self.survivalRect.collidepoint(event.pos):
                        self.flag=False
                        self.game.flag=True
                        self.game.gamebegin(True)
                    elif self.saveRect.collidepoint(event.pos):
                        self.naming=True
                        self.setname()
                    elif self.exitRect.collidepoint(event.pos):
                        menuClick_ogg.play()
                        pygame.quit()
                        sys.exit()
                    elif self.helpRect.collidepoint(event.pos):
                        menuClick_ogg.play()
                        self.flag=False
                        self.helpering=True
                        self.helper()
                    elif self.optionRect.collidepoint(event.pos):
                        menuClick_ogg.play()
                        menu.flag=True
                        menu.returnimg=menu.returnimg0
                        menu.draw()
                if self.name=='':
                    self.setname()
            pygame.display.flip()

def getImageSource(path):
    return pygame.image.load(path)

def getSoundEffect(path):
    return pygame.mixer.Sound(path)

def getImages():
    global zombieType
    zombieType=[
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
        ]
    ]
    global objectType
    objectType=[
        getImageSource('images/widget/小推车.png'),
        [getImageSource(f'images/太阳/{i}.png') for i in range(29)],
        getImageSource('images/豌豆射手/豆.png'),
        getImageSource('images/土豆地雷/爆炸.gif'),
        getImageSource('images/土豆地雷/土豆泥.gif'),
        [getImageSource('images/土豆地雷/在地下.gif')],
        getImageSource('images/樱桃炸弹/boom.png'),
        [getImageSource(f'images/僵尸死/普通/{i}.png') for i in range(10)],
        [getImageSource(f'images/僵尸死/灰烬/{i}.png') for i in range(10)],
        [getImageSource(f'images/僵尸死/普通/头/{i}.png') for i in range(12)],
        [
            getImageSource('images/widget/关卡/StartReady.png'),
            getImageSource('images/widget/关卡/StartSet.png'),
            getImageSource('images/widget/关卡/StartPlant.png')
        ],
        getImageSource('images/widget/遮罩.png'),
        getImageSource('images/widget/关卡/coin_silver.png'),
        getImageSource('images/widget/关卡/coin_gold.png'),
        getImageSource('images/widget/关卡/diamond.png'),
        getImageSource('images/widget/关卡/coinbank.png')
    ]
    global plantType
    plantType=[
        [getImageSource(f'images/向日葵/{i}.png') for i in range(18)],
        [getImageSource(f'images/豌豆射手/{i}.png') for i in range(13)],
        [getImageSource(f'images/双重射手/{i}.png') for i in range(15)],
        [getImageSource(f'images/火爆辣椒/{i}.png') for i in range(7)],
        [getImageSource(f'images/火/{i}.png') for i in range(8)],
        [getImageSource(f'images/坚果/{i}.png') for i in range(16)],
        [getImageSource(f'images/土豆地雷/{i}.png') for i in range(8)],
        [getImageSource(f'images/樱桃炸弹/{i}.png') for i in range(7)]
    ]

if __name__=='__main__':
    pygame.init()
    pygame.mixer.init()
    zombieType,objectType,plantType=[],[],[]
    imgThread=threading.Thread(target=getImages)
    imgThread.start()
    scoretext = pygame.font.Font('fonts/digit.ttf', 15)
    pricetext = pygame.font.Font('fonts/digit.ttf', 13)
    menutext=pygame.font.Font('fonts/fzsr.ttf',22)
    tittletext=pygame.font.Font('fonts/fzsr.ttf',48)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Plant Vs Zombie α')
    pygame.display.set_icon(getImageSource('images/icon.png'))
    plantDead_ogg=getSoundEffect('sounds/bigchomp.ogg')
    zombieComing_ogg=getSoundEffect('sounds/awooga.ogg')
    potatoActive_ogg=getSoundEffect('sounds/gravestone_rumble.ogg')
    potatoBoom_ogg=getSoundEffect('sounds/potato_mine.ogg')
    cherryBoom_ogg=getSoundEffect('sounds/cherrybomb.ogg')
    coinfall_ogg=getSoundEffect('sounds/moneyfalls.ogg')
    coinpick_ogg=getSoundEffect('sounds/coin.ogg')
    diamondfall_ogg=getSoundEffect('sounds/chime.ogg')
    diamondpick_ogg=getSoundEffect('sounds/diamond.ogg')
    paper_ogg=getSoundEffect('sounds/paper.ogg')
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
    menuClick_ogg=getSoundEffect('sounds/grassstep.ogg')
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