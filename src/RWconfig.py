import json


class RWconfig:
    def __init__(self) -> None:
        with open('config.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.rconfig()

    def rconfig(self):
        self.name = self.config['user']['name']
        self.money = self.config['user']['money']
        self.gamevolume = self.config['volume']['game']
        self.menuvolume = self.config['volume']['menu']

        self.prop = self.config['prop']

    def wconfig(self, zone, name, value, prop=False):
        with open('config.json', 'w') as f:
            if prop:
                self.config['prop'][zone][name] = value
            else:
                self.config[zone][name] = value
            json.dump(self.config, f, indent=4)
        self.rconfig()


rwconfig = RWconfig()
