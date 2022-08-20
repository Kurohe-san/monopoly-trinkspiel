#!/usr/bin/python

import random
import time
from colorama import Fore,Style
from lib import *
from ui import *

"""
AKTIONEN:
    Duell: 


"""

def action(f, player, players, properties):
    match f[0]:
        case 'M':
            ui_command(["Du bist auf einem Geld-Feld!", "OK"],curs,stdscr)
            time.sleep(1)
            x = gen_money_card()
            ui_command([f"Die Geldkarte enthält... {x}$", "OK"],curs,stdscr)
            player.add(x)
        case 'D':
            ui_command(["IT'S TIME TO DUEL!!!1!!1!", "HELL YEAH!"],curs,stdscr)
            dp = select_player(players, True)
            if dp.properties == []:
                ui_command([f"{dp.name} hat keine Grundstücke.\nAbbruch...", "OK"],curs,stdscr)
            w = yes_no("Hat {player.name} gewonnen?",curs,stdscr)

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
                    if input(f"Will jemand {player.name} herausfordern? y/N > ") == 'y':
                        if challenge(player.credit, properties[index].base_cost):
                            properties[index].buy(player)
                    else:
                        properties[index].buy(player)
                return
            if properties[index].owner == player:
                if input("Bereits der Besitzer. Bebauen (erhöhen um 2 Getränkestufen)? y/N > ") == 'y':
                    if input(f"Will jemand {player.name} herausfordern? y/N > ") == 'y':
                        if challenge(player.credit, properties[index].base_cost):
                            properties[index].build(player)
                    else:
                        properties[index].build(player)
                return
            if properties[index].owner != player:
                # Bestrafen (trinken) oder:
                if input("Abkaufen (statt saufen)? y/N > ") == 'y':
                    if input(f"Will {properties[index].owner.name} {player.name} herausfordern? y/N > ") == 'y':
                        if challenge(player.credit, properties[index].base_cost, 2):
                            transfer_property(properties[index].owner, player, properties[index])
                    else:
                        transfer_property(properties[index].owner, player, properties[index])
                return


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
        properties.append(Property.gen_street())
    fields = ['' for i in range(25)]
    fields[0] = 'D'
    fields[13] = 'D'
    fields[3] = fields[6] = fields[9] = fields[12] = fields[15] = fields[18] = fields[21] = fields[24] = 'M'
    j = 0
    for i in range(25):
        if fields[i] == '':
            fields[i] = 'P'+str(j)
            j+=1

    curs,stdscr = ui_init()

    #while len(i:=input("Gebe einen Spielernamen ein: ")) > 0:
    #    players.append(Player(i))
    players.append(Player('Henri'))
    players.append(Player('Levin'))
    ui_display(properties,players, curs, stdscr)
    return (players,properties,fields,curs,stdscr)

if __name__ == '__main__':
    players,properties,fields,curs,stdscr = init()
    cur_player = 0
    c = ''
    while c != "exit":
        # print("Info über das Spiel: ")
        # print_players(players)
        # print(Fore.GREEN + players[cur_player].name + Style.RESET_ALL + " ist an der Reihe!")
        # if players[cur_player].credit < 0:
        #     print(Fore.RED+"ACHTUNG: Dein Kontostand ist negativ."+Style.RESET_ALL)
      

        # Grafische Darstellung des Spielfeldes
        # print('')
        # player_str = '-' * 25 
        # for p in players:
        #     e = p.name[0]
        #     if player_str[p.field] != '-':
        #         e = '*'
        #     player_str = player_str[:p.field] + p.name[0] + player_str[p.field+1:]
        # print(Fore.GREEN +player_str)
        # print(Fore.BLUE +''.join([f[0] for f in fields])+Style.RESET_ALL)
        # print('')

        
        # c = input("GAME >> ")
        c = ui_command([players[cur_player].name + " ist an der Reihe", "Würfeln", "Spielanleitung"],curs,stdscr)
        if c == 2:
            pass
        #     print("exit - Exit the game")
        #     print("\n\n")
        elif c == 1:
            w1 = random.randrange(1,6)
            w2 = random.randrange(1,6)
            ui_command(["Du hast gewürfelt: " + str(w1) + " + " + str(w2), "OK"],curs,stdscr)
            p = players[cur_player]
            p.move(w1+w2, 25)
            action(fields[p.field],p, players, properties)
            cur_player = (cur_player + 1) % len(players)
