from src import Source
from src.Game import Game
from src.Menu import Menu, MainMenu

if __name__ == '__main__':
    Source.game = Game()
    Source.menu = Menu(Source.game)
    Source.mainMenu = MainMenu(Source.game)
    Source.mainMenu.init()

