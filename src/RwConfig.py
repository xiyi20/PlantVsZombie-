import json


class RwConfig:
    def __init__(self) -> None:
        self.prop = None
        self.menuVolume = None
        self.gameVolume = None
        self.money = None
        self.config = None
        self.name = None
        self.file = None
        self.lconfig()

    def lconfig(self):
        if self.file:
            self.file.close()
        self.file = open('../config.json', 'r', encoding='utf-8')
        self.config = json.load(self.file)
        self.rConfig()

    def rConfig(self):
        self.name = self.config['user']['name']
        self.money = self.config['user']['money']
        self.gameVolume = self.config['volume']['game']
        self.menuVolume = self.config['volume']['menu']

        self.prop = self.config['prop']

    def wConfig(self, zone, name, value, prop=False):
        with open('../config.json', 'w') as f:
            if prop:
                self.config['prop'][zone][name] = value
            else:
                self.config[zone][name] = value
            json.dump(self.config, f, indent=4)
        self.rConfig()


rwConfig = RwConfig()
