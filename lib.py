import random
import random_name_generator as rng

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

def gen_money_card():
    return random.randrange(-2000,10000)

def print_players(players):
    for i,p in enumerate(players):
        print(f"{i}: {p.name} @ Feld Nr. {p.field} => {'  '.join([pr.output() for pr in p.properties])}")

def select_player(players, output_properties=False):
    print("Wähle einen Spieler aus:")
    for i,p in enumerate(players):
        print(f"{i}: {p.name} @ Feld Nr. {p.field}" + f"=> {'  '.join([pr.output() for pr in p.properties])}" if output_properties else "")
    i = 0
    i = int(input('> '))
    while i > len(players)-1 or i<0:
        print("Bist du behindert?")
        i = int(input('> '))
    return players[i]

def challenge(credit, to_pay, factor=1):
    diff = credit - factor*to_pay
    print(f"Differenz: {diff} {'Oof!' if diff < 0 else 'Yay!'}")
    return diff > 0

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
        return Property('-'.join(rng.generate_one(rng.Descent.ENGLISH, sex=rng.Sex.MALE).split(' '))+'-'+random.choice(['Street','Boulevard','Avenue']),
            x,
            c)


class Player:
    def __init__(self,name):
        self.name = name
        self.credit = sum([gen_money_card() for i in range(2)])
        self.field = 0
        self.properties = []

    def add(self, amount):        
        self.credit += amount

    def remove(self, amount):
        self.credit -= amount

    def move(self, amount, field_size):
        self.field = (self.field + amount) % field_size

