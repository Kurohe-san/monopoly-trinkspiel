import random
import names
from ui import ui_command, ui_init
import json
import consts

# Gewöhnliches UI-Element, dass Auswahl zwischen Ja und Nein ermöglicht. Gibt True zurück für zweite Wahlmöglichkeit.
def yes_no(query,ui,yes_first=False, delete=True, yes_token="Ja", no_token="Nein"):
    return ui_command([query] + ([yes_token,no_token] if yes_first else [no_token,yes_token]),ui, delete=False) == 2

# Generiert eine Geldkarte (auf Geldfeldern oder am Start des Spiels)
def gen_money_card():
    return random.randrange(-2000,10000)

#def print_players(players):
#    for i,p in enumerate(players):
#        print(f"{i}: {p.name} @ Feld Nr. {p.field} => {'  '.join([pr.output() for pr in p.properties])}")

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

# Ermöglich anzweifeln einer Bezahlaktion (alternativ mit Faktor für den zu bezahlenden Wert)
def challenge(credit, to_pay, ui, factor=1):
    diff = credit - factor*to_pay
    ui_command([f"Differenz: {diff}",f"{'Oof!' if diff < 0 else 'Yay!'}"],ui)
    return diff > 0

# Erzeugt Speicherdaten eines laufenden Spieles in einer JSON-Datei mit spezifiziertem Namen
def save_data(players, properties, save_file_name):
    with open(save_file_name+'.json','w') as f:
        json.dump({'players':list(map(lambda p: p.to_dict(), players)), 'properties':list(map(lambda p: p.to_dict(players), properties))}, f, indent=4)

def load_data(save_file_name):
    with open(save_file_name, 'r') as f:
        data = json.load(f)
        players = list(map(lambda p: Player(p['name'], p['credit'], p['field']), data['players']))
        properties = list(map(lambda p: Property(p['name'], p['base_cost'], p['rent'], (None if p['owner'] == None else players[p['owner']]), p['build_level']), data['properties']))
        for p in filter(lambda pr: pr.owner != None,properties): p.owner.properties.append(p)
        return (players, properties)
         



# Klasse eines Gebäudes
class Property:
    def __init__(self,name, base_cost, rent, owner=None, build_level = 0):
        # 
        self.name = name
        self.base_cost = base_cost
        self.rent = rent
        self.owner = owner
        self.build_level = build_level
    
    # Ein Gebäude kaufen
    def buy(self, player):
        player.remove(self.base_cost)
        player.properties.append(self)
        self.owner = player

    # Ein Gebäude bebauen (bis zu zwei Mietestufen)
    def build(self, player):
        player.remove(self.base_cost)
        if self.rent >=6:
            self.rent = 7
            return
        self.rent += 2
        self.build_level += 1

    def output(self):
        return self.name + ": " + consts.DRINKS[self.rent]

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
        name = names.get_last_name()+'-'+random.choice(['Street','Boulevard','Avenue'])
        return Property(name,x,c)

    def to_dict(self, players):
        return {
            'name': self.name,
            'base_cost': self.base_cost,
            'rent': self.rent,
            'owner': None if self.owner == None else players.index(self.owner),
            'build_level': self.build_level
        }


class Player:

    def __init__(self,name, credit=sum([gen_money_card() for _ in range(2)]), field=0):
        self.name = name
        self.credit = credit
        self.field = field
        self.properties = []
    
    def add(self, amount):        
        self.credit += amount

    def remove(self, amount):
        self.credit -= amount

    def move(self, amount, field_size):
        self.field = (self.field + amount) % field_size
    
    def transfer_property(self, recipient, prop, ui):
        x=random.randrange(10)
        if x<3:
            ui_command(["Du MUSST den Preis bezahlen (ohne, dass du es kriegst)...","😢"],ui)
            recipient.remove(prop.base_cost)
            return
        elif x<6:
            ui_command(["Du MUSST für den doppelten Preis kaufen...","😵"],ui)
            recipient.remove(prop.base_cost * 2)
            self.add(prop.base_cost)
        elif x<10:
            ui_command(["Du MUSST für den normalen Preis kaufen...","😌"],ui)
            recipient.remove(prop.base_cost)
            self.add(prop.base_cost)
        else:
            ui_command(["Die Götter lieben dich! Du kriegst es kostenlos.","😎"],ui)

        self.properties.append(prop)
        recipient.properties.append(prop)
        prop.owner = recipient

    def to_dict(self):
        return {
            'name': self.name,
            'credit': self.credit,
            'field': self.field
        }

class UI:
    def __init__(self):
        self.curs,self.stdscr = ui_init()
        self.width_streets = 7
        self.width_owner = 8
        self.width_rent = 5
        self.width_players = 0
        self.width_command = 0
        self.max_width_command = 0
        self.start_command = 0
        self.min_start_command = 0
        self.height,self.width = self.stdscr.getmaxyx()
        self.number_streets = 0
        self.height_offset = 0
        self.height_offset_answerers = 0
        self.saved_commands = []
