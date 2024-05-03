import Source
from Game import Game
from Menu import Menu, MainMenu


if __name__ == '__main__':
    Source.game = Game()
    Source.menu = Menu(Source.game)
    Source.mainMenu = MainMenu(Source.game)
    Source.mainMenu.init()

