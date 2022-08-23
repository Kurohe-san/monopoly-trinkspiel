import random
import names
from ui import ui_command, ui_init
import json

DRINKS = [
    'S1',
    'S2',
    'S3',
    'S4',
    'S5',
    'H1',
    'H2',
    'H3'
]

UI_TOKEN = {
        'UI_TOKEN_EXIT': "Beenden ❌",
        'UI_TOKEN_ROLL': "Würfeln 🎲",
        'UI_TOKEN_RULES': "Spielanleitung 📜",
        'UI_TOKEN_SAVE': "Speichern 💾",
        'UI_TOKEN_LOAD': "Laden 💽"
}

RULES = """
REGELN:
    1. Spieler kennen ihren aktuellen Kontostand nicht.
    2. Spieler können auf Geld-Feldern zufällig zusätzliches Geld gewinnen (oder verlieren).
    3. Spieler können auf Grundstück-Feldern diese kaufen, auch wenn sie nicht genug Geld haben, und die anderen Spieler lönnen anzweifeln, ob sie tatsächlich genug Geld für den Kauf haben.
    4. Spieler konnen auf Duell-Feldern andere Spieler herausfordern (abwechselnd trinken) und um ein Grundstück spielen.
"""

def yes_no(query,ui,yes_first=False):
    return ui_command([query] + (["Ja","Nein"] if yes_first else ["Nein","Ja"]),ui, False) == 2

def gen_money_card():
    return random.randrange(-2000,10000)

def print_players(players):
    for i,p in enumerate(players):
        print(f"{i}: {p.name} @ Feld Nr. {p.field} => {'  '.join([pr.output() for pr in p.properties])}")

# def select_player(players, output_properties=False):
#    print("Wähle einen Spieler aus:")
#    for i,p in enumerate(players):
#        print(f"{i}: {p.name} @ Feld Nr. {p.field}" + f"=> {'  '.join([pr.output() for pr in p.properties])}" if output_properties else "")
#    i = 0
#    i = int(input('> '))
#    while i > len(players)-1 or i<0:
#        print("Bist du behindert?")
#        i = int(input('> '))
#    return players[i]

def challenge(credit, to_pay, ui, factor=1):
    diff = credit - factor*to_pay
    ui_command([f"Differenz: {diff}",f"{'Oof!' if diff < 0 else 'Yay!'}"],ui)
    return diff > 0

def save_data(players, properties, save_file_name):
    with open(save_file_name+'.json','w') as f:
        json.dump({'players':list(map(lambda p: p.to_dict(), players)), 'properties':list(map(lambda p: p.to_dict(), properties))}, f)


class Property:
    def __init__(self,name, base_cost, rent):
        self.name = name
        self.base_cost = base_cost
        self.rent = rent
        self.owner = None

    def buy(self, player):
        player.remove(self.base_cost)
        player.properties.append(self)
        self.owner = player

    def build(self, player):
        player.remove(self.base_cost)
        if self.rent >=6:
            self.rent = 7
            return
        self.rent += 2

    def output(self):
        return self.name + ": " + DRINKS[self.rent]

    def gen_street():
        x = random.randrange(250,10000)
        c = 0
        if x<1000:
           c = 0
        elif x<2500:    
           c = 1
        elif x<4000:
            c = 2
        elif x<5500:
            c = 3
        elif x<7000:
            c = 4
        elif x<8500:
            c = 5
        elif x<9500:
            c = 6
        else:
            c = 7
        name = names.get_full_name().replace(' ','-')+'-'+random.choice(['Street','Boulevard','Avenue'])
        return Property(name,x,c)

    def to_dict(self):
        return {
            'name': self.name,
            'base_cost': self.base_cost,
            'rent': self.rent
        }


class Player:
    def __init__(self,name):
        self.name = name
        self.credit = sum([gen_money_card() for _ in range(2)])
        self.field = 0
        self.properties = []

    def add(self, amount):        
        self.credit += amount

    def remove(self, amount):
        self.credit -= amount

    def move(self, amount, field_size):
        self.field = (self.field + amount) % field_size

    def to_dict(self):
        return {
            'name': self.name,
            'credit': self.credit,
            'field': self.field
        }

class UI:
    def __init__(self):
        self.curs,self.stdscr = ui_init()
        self.widthStreets = 7
        self.widthOwner = 8
        self.widthRent = 5
        self.widthPlayers = 0
        self.widthCommand = 0
        self.maxWidthCommand = 0
        self.startCommand = 0
        self.minStartCommand = 0
        self.height,self.width = self.stdscr.getmaxyx()
        self.numberStreets = 0
        self.heightOffset = 0
        self.savedCommands = []
