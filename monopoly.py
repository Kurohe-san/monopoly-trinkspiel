#!/usr/bin/python

import random_name_generator as rng
import random
import time
from colorama import Fore,Style

"""
AKTIONEN:
    Duell: 


"""

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

def gen_money_card():
    return random.randrange(-2000,10000)

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

def print_players(players):
    for i,p in enumerate(players):
        print(f"{i}: {p.name} @ Feld Nr. {p.field} => {'  '.join([pr.output() for pr in p.properties])}")

def action(f, player, players, properties):
    match f[0]:
        case 'M':
            print("Du bist auf einem Geld-Feld!")
            time.sleep(1)
            x = gen_money_card()
            print(f"Die Geldkarte enthält... {x}$")
            player.add(x)
        case 'D':
            print("IT'S TIME TO DUEL!!!1!!1!")
            dp = select_player(players, True)
            w = input("Hat der Herrausforderer gewonnen? y/N > ") == 'y'
            played_property = random.choice(dp.properties)
            print(f"Es ging um {played_property.output()}!")
            if w:
                dp.properties.remove(played_property)
                player.properties.append(played_property)
                played_property.owner = player
        case 'P':
            print("Du bist auf einem Geländefeld!")
            index = int(f[1:])
            owned = properties[index].owner != None
            print(Fore.YELLOW + properties[index].output() + Style.RESET_ALL + "; Besitzer: " +Fore.GREEN+ (properties[index].owner.name if owned else '- ') + Style.RESET_ALL+ f"; Preis: {Fore.MAGENTA}{properties[index].base_cost}{Style.RESET_ALL}$")
            if not owned:
                if input("Kaufen? y/N > ") == 'y':
                    if input(f"Will jemand {player.name} herrausfordern? y/N > ") == 'y':
                        if challenge(player.credit, properties[index].base_cost):
                            properties[index].buy(player)
                    else:
                        properties[index].buy(player)
                return
            if properties[index].owner == player:
                if input("Bereits der Besitzer. Bebauen (erhöhen um 2 Getränkestufen)? y/N > ") == 'y':
                    if input(f"Will jemand {player.name} herrausfordern? y/N > ") == 'y':
                        if challenge(player.credit, properties[index].base_cost):
                            properties[index].build(player)
                    else:
                        properties[index].build(player)
                return
            if properties[index].owner != player:
                # Bestrafen (trinken) oder:
                if input("Abkaufen (statt saufen)? y/N > ") == 'y':
                    if input(f"Will {properties[index].owner.name} {player.name} herrausfordern? y/N > "):
                        if challenge(player.credit, properties[index].base_cost, 2):
                            transfer_property(properties[index].owner, player, properties[index])
                    else:
                        transfer_property(properties[index].owner, player, properties[index])
                return


def challenge(credit, to_pay, factor=1):
    diff = credit - factor*to_pay
    print(f"Differenz: {diff} {'Oof!' if diff < 0 else 'Yay!'}")
    return diff > 0

def transfer_property(old, new, prop):
    x=random.randrange(10)
    if x<3:
        print("Du MUSST den Preis bezahlen (ohne, dass du es kriegst)...")
        new.remove(prop.base_cost)
        return
    elif x<6:
        print("Du MUSST für den doppelten Preis kaufen...")
        new.remove(prop.base_cost * 2)
        old.add(prop.base_cost)
    elif x<10:
        print("Du MUSST für den normalen Preis kaufen...")
        new.remove(prop.base_cost)
        old.add(prop.base_cost)
    else:
        print("Die Götter lieben dich! Du kriegst es kostenlos.")

    old.properties.append(prop)
    new.properties.append(prop)
    prop.owner(new)

def init():
    properties = []
    players = []
    for i in range(15):
        properties.append(gen_street())
    fields = ['' for i in range(25)]
    fields[0] = 'D'
    fields[13] = 'D'
    fields[3] = fields[6] = fields[9] = fields[12] = fields[15] = fields[18] = fields[21] = fields[24] = 'M'
    j = 0
    for i in range(25):
        if fields[i] == '':
            fields[i] = 'P'+str(j)
            j+=1

    print("Hallo.")
    while len(i:=input("Gebe einen Spielernamen ein: ")) > 0:
        players.append(Player(i))
    return (players,properties,fields)

if __name__ == '__main__':
    players,properties,fields = init()
    cur_player = 0
    c = ''
    while c != "exit":
        print("Info über das Spiel: ")
        print_players(players)
        print(Fore.GREEN + players[cur_player].name + Style.RESET_ALL + " ist an der Reihe!")
        if players[cur_player].credit < 0:
            print(Fore.RED+"ACHTUNG: Dein Kontostand ist negativ."+Style.RESET_ALL)
      

        # Grafische Darstellung des Spielfeldes
        print('')
        player_str = '-' * 25 
        for p in players:
            e = p.name[0]
            if player_str[p.field] != '-':
                e = '*'
            player_str = player_str[:p.field] + p.name[0] + player_str[p.field+1:]
        print(Fore.GREEN +player_str)
        print(Fore.BLUE +''.join([f[0] for f in fields])+Style.RESET_ALL)
        print('')

        c = input("GAME >> ")
        if c == "help":
            print("exit - Exit the game")
            print("\n\n")
        elif c.startswith('r'):
            time.sleep(1)
            w1 = random.randrange(1,6)
            w2 = random.randrange(1,6)
            print(f"Du hast gewürfelt: {w1} + {w2} = {w1+w2}")
            time.sleep(1)
            p = players[cur_player]
            p.move(w1+w2, 25)
            action(fields[p.field],p, players, properties)
            cur_player = (cur_player + 1) % len(players)

