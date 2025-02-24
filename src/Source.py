import pygame

pygame.init()
pygame.mixer.init()

game = None
menu = None
mainMenu = None


def getImageSource(path):
    return pygame.image.load(f"../{path}")


def getSoundEffect(path):
    return pygame.mixer.Sound(f"../{path}")


clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Plant Vs Zombie α')
pygame.display.set_icon(getImageSource('img/icon.png'))

scoreText = pygame.font.Font('../font/digit.ttf', 15)
priceText = pygame.font.Font('../font/digit.ttf', 13)
menuText = pygame.font.Font('../font/fzsr.ttf', 22)
tittleText = pygame.font.Font('../font/fzsr.ttf', 48)
waveText = pygame.font.Font('../font/fzxs12.ttf', 12)
hoverText = pygame.font.Font('../font/fzxs12.ttf', 17)
plantDead_ogg = getSoundEffect('aud/bigchomp.ogg')
zombieComing_ogg = getSoundEffect('aud/awooga.ogg')
potatoActive_ogg = getSoundEffect('aud/gravestone_rumble.ogg')
potatoBoom_ogg = getSoundEffect('aud/potato_mine.ogg')
cherryBoom_ogg = getSoundEffect('aud/cherrybomb.ogg')
coinFall_ogg = getSoundEffect('aud/moneyfalls.ogg')
coinPick_ogg = getSoundEffect('aud/coin.ogg')
diamondFall_ogg = getSoundEffect('aud/chime.ogg')
diamondPick_ogg = getSoundEffect('aud/diamond.ogg')
paper_ogg = getSoundEffect('aud/paper.ogg')
zombieEating_ogg = [
    getSoundEffect(path) for path in (
        'aud/chomp.ogg',
        'aud/chomp2.ogg',
        'aud/chompsoft.ogg'
    )
]
zombieGroan_ogg = [
    getSoundEffect(path) for path in (
        'aud/groan.ogg',
        'aud/groan2.ogg',
        'aud/groan3.ogg',
        'aud/groan4.ogg',
        'aud/groan5.ogg',
        'aud/groan6.ogg',
        'aud/lowgroan.ogg',
        'aud/lowgroan2.ogg'
    )
]
menuClick_ogg = getSoundEffect('aud/grassstep.ogg')
buttonClick_ogg = getSoundEffect('aud/buttonClick.ogg')
mainMenuBgm_ogg = getSoundEffect(
    'aud/bgm/Laura Shigihara - Crazy Dave.ogg')
loseMusic_ogg = [
    getSoundEffect(path) for path in (
        'aud/losemusic.ogg',
        'aud/scream.ogg'
    )
]
winMusic_ogg = getSoundEffect('aud/winmusic.ogg')
plant_ogg = [
    getSoundEffect(path) for path in (
        'aud/plant.ogg',
        'aud/plant2.ogg'
    )
]
splat_ogg = [
    getSoundEffect(path) for path in (
        'aud/splat.ogg',
        'aud/splat2.ogg',
        'aud/splat3.ogg'
    )
]
ironHit_ogg = [
    getSoundEffect(path) for path in (
        'aud/shieldhit.ogg',
        'aud/shieldhit.ogg'
    )
]
zombie_falling_ogg = [
    getSoundEffect(path) for path in (
        'aud/zombie_falling_1.ogg',
        'aud/zombie_falling_1.ogg'
    )
]
backGroundMusic = [
    'aud/bgm/Brainiac Maniac-Laura Shigihara.mp3',
    'aud/bgm/Graze the Roof-Laura Shigihara.mp3',
    'aud/bgm/Grasswalk.mp3',
    'aud/bgm/Loonboon-Laura Shigihara.mp3',
    'aud/bgm/Moongrains-Laura Shigihara.mp3',
    'aud/bgm/Rigor Mormist-Laura Shigihara.mp3',
    'aud/bgm/Ultimate Battle-Laura Shigihara.mp3',
    'aud/bgm/Watery Graves-Laura Shigihara.mp3'
]

pickup_ogg = getSoundEffect('aud/points.ogg')
shoot_ogg = [
    getSoundEffect(path) for path in (
        'aud/kernelpult.ogg',
        'aud/kernelpult2.ogg'
    )
]
car_ogg = getSoundEffect('aud/lawnmower.ogg')
invalidClick_ogg = getSoundEffect('aud/buzzer.ogg')
shovel_ogg = getSoundEffect('aud/shovel.ogg')
plantSlot_ogg = getSoundEffect('aud/seedlift.ogg')

zombieType = [
    [
        [getImageSource(f'img/普通僵尸/走/{i}.png') for i in range(18)],
        [getImageSource(f'img/普通僵尸/吃/{i}.png') for i in range(18)]
    ],
    [
        [getImageSource(f'img/路障僵尸/走/{i}.png') for i in range(21)],
        [getImageSource(f'img/路障僵尸/吃/{i}.png') for i in range(11)]
    ],
    [
        [getImageSource(f'img/铁桶僵尸/走/{i}.png') for i in range(15)],
        [getImageSource(f'img/铁桶僵尸/吃/{i}.png') for i in range(11)]
    ],
    [
        [getImageSource(f'img/大爷/走/{i}.png') for i in range(11)],
        [getImageSource(f'img/大爷/吃/{i}.png') for i in range(10)]
    ]
]
objectType = [
    getImageSource('img/widget/小推车.png'),
    [getImageSource(f'img/太阳/{i}.png') for i in range(29)],
    [getImageSource('img/豆/普通/0.png')],
    getImageSource('img/土豆地雷/爆炸.gif'),
    getImageSource('img/土豆地雷/土豆泥.gif'),
    [getImageSource('img/土豆地雷/在地下.gif')],
    getImageSource('img/樱桃炸弹/boom.png'),
    [getImageSource(f'img/僵尸死/普通/{i}.png') for i in range(10)],
    [getImageSource(f'img/僵尸死/灰烬/{i}.png') for i in range(10)],
    [getImageSource(f'img/僵尸死/普通/头/{i}.png') for i in range(12)],
    [
        getImageSource('img/widget/关卡/StartReady.png'),
        getImageSource('img/widget/关卡/StartSet.png'),
        getImageSource('img/widget/关卡/StartPlant.png')
    ],
    getImageSource('img/widget/遮罩.png'),
    getImageSource('img/widget/关卡/coin_silver.png'),
    getImageSource('img/widget/关卡/coin_gold.png'),
    getImageSource('img/widget/关卡/diamond.png'),
    getImageSource('img/widget/关卡/coinbank.png'),
    [getImageSource(f'img/大爷/死/{i}.png') for i in range(7)],
    [getImageSource(f'img/豆/火豆/{i}.png') for i in range(2)],
    getImageSource('img/widget/菜单栏/按钮.png'),
    getImageSource('img/主界面/store.png'),
    getImageSource('img/主界面/dialog.png'),
    [getImageSource('img/猫尾草/thorn.png')]
]
plantType = [
    [getImageSource(f'img/向日葵/{i}.png') for i in range(18)],
    [getImageSource(f'img/豌豆射手/{i}.png') for i in range(13)],
    [getImageSource(f'img/双重射手/{i}.png') for i in range(15)],
    [getImageSource(f'img/火爆辣椒/{i}.png') for i in range(7)],
    [getImageSource(f'img/火/{i}.png') for i in range(8)],
    [getImageSource(f'img/坚果/{i}.png') for i in range(16)],
    [getImageSource(f'img/土豆地雷/{i}.png') for i in range(8)],
    [getImageSource(f'img/樱桃炸弹/{i}.png') for i in range(7)],
    [getImageSource(f'img/火炬树桩/{i}.png') for i in range(9)],
    [getImageSource(f'img/机枪射手/{i}.png') for i in range(13)],
    [getImageSource(f'img/猫尾草/火/{i}.png') for i in range(14)],
    [getImageSource(f'img/猫尾草/普通/{i}.png') for i in range(14)]
]
goodsType=[
    getImageSource('img/widget/商店/Store_SoldOutLabel.png')
]