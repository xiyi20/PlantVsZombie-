import json


class RWconfig:
    def __init__(self) -> None:
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        self.rconfig()

    def rconfig(self):
        self.name = self.config['user']['name']
        self.money = self.config['user']['money']
        self.gamevolume = self.config['volume']['game']
        self.menuvolume = self.config['volume']['menu']

    def wconfig(self, zone, name, value):
        with open('config.json', 'w') as f:
            self.config[zone][name] = value
            json.dump(self.config, f, indent=4)
        self.rconfig()


rwconfig = RWconfig()
