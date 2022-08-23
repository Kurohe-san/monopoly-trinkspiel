#!/usr/bin/python

import random
#from colorama import Fore,Style
from lib import *
from ui import *
from consts import UI_TOKEN, RULES

"""
AKTIONEN:
    Duell: 


"""


# Aktionen die auf Feldern ausgeführt werden:
# 'M': Geld-Feld -- eine Geldkarte ziehen
# 'D': Duell-Felds -- ein Duell ausführen und Gewinner angeben
# 'P<n>': Ein Grundstück mit index n in der properties liste
def action(f, player, players, properties):
    match f[0]:
        case 'M':
            ui_command(["Du bist auf einem Geld-Feld!"],ui)
            #time.sleep(1)
            x = gen_money_card()
            ui_command([f"Die Geldkarte enthält... {x}$", "OK"],ui)
            player.add(x)
        case 'D':
            ui_command(["IT'S TIME TO DUEL!!!1!!1!", "HELL YEAH!"],ui, False)
            players_available = list(filter(lambda n: n != player and n.properties != [],players))
            if players_available ==  []: 
                ui_command(["Es stehen keine Spieler zur Auswahl", "OK"], ui)
                return
            dp = players_available[ui_command(["Wähle einen Gegner aus:"]+list(map(lambda p: p.name, players_available)), ui)-1]

            if dp.properties == []:
                ui_command([f"{dp.name} hat keine Grundstücke. Abbruch...", "OK"],ui)
                return
            played_property = random.choice(dp.properties)
            w = yes_no(f"Hat {player.name} gewonnen?",ui)

            ui_command([f"Es ging um {played_property.output()}!","OK"], ui)
            if w:
                dp.properties.remove(played_property)
                player.properties.append(played_property)
                played_property.owner = player
                ui_display(ui)
        case 'P':
            ui_command(["Du bist auf einem Grundstück!"],ui, False)
            index = int(f[1:])
            owned = properties[index].owner != None
            ui_command([properties[index].output() + "; Besitzer: " + (properties[index].owner.name if owned else '- ') + f"; Preis: {properties[index].base_cost}$"],ui, False)

            if not owned:
                if yes_no("Kaufen?",ui, False, False):
                    if yes_no(f"Will jemand {player.name} herausfordern?",ui):
                        if challenge(player.credit, properties[index].base_cost, ui):
                            properties[index].buy(player)
                    else:
                        properties[index].buy(player)
                    ui_display(properties,players,ui)
                return
            if properties[index].owner == player:
                if yes_no("Bereits der Besitzer. Bebauen (erhöhen um 2 Getränkestufen)?",ui):
                    if yes_no(f"Will jemand {player.name} herausfordern?",ui):
                        if challenge(player.credit, properties[index].base_cost, ui):
                            properties[index].build(player)
                    else:
                        properties[index].build(player)
                return
            if properties[index].owner != player:
                # Bestrafen (trinken) oder:
                if yes_no("Abkaufen (statt saufen)?",ui):
                    if yes_no(f"Will {properties[index].owner.name} {player.name} herausfordern?",ui):
                        if challenge(player.credit, properties[index].base_cost, ui, 2):
                            properties[index].owner.transfer_property(player, properties[index], ui)
                    else:
                        properties[index].owner.transfer_property(player, properties[index], ui)
                    ui_display(properties,players,ui)
                return


def init():
    players = []
    properties = list(map(lambda _: Property.gen_street(), range(15)))
    fields = ['' for _ in range(25)]
    
    j = 0
    for i in range(consts.FIELD_SIZE):
        if i%13 == 0:
            fields[i] = 'D'
        elif i%3 == 0:
            fields[i] = 'M'
        else:
            fields[i] = 'P'+str(j)
            j += 1

    ui = UI()

    #while len(i:=input("Gebe einen Spielernamen ein: ")) > 0:
    #    players.append(Player(i))
    ui_display(properties,players, ui)
    players.append(Player(ui_input("Gebe einen Spieler ein", ui)))
    ui_display(properties,players, ui)
    while True:
        players.append(Player(ui_input("Gebe einen Spieler ein", ui)))
        ui_display(properties,players, ui)
        if ui_command(["Noch ein Spieler?", "Ja", "Nein"], ui) == 2:
            break
    ui_display(properties,players, ui)
    return (players,properties,fields,ui)

if __name__ == '__main__':
    players,properties,fields,ui = init()
    cur_player = 0
    running = True
    while running:
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
        ui_delete_saved_commands(ui)
        commands = [players[cur_player].name] + [
                    UI_TOKEN['UI_TOKEN_ROLL'], 
                    UI_TOKEN['UI_TOKEN_RULES'], 
                    UI_TOKEN['UI_TOKEN_SAVE'], 
                    UI_TOKEN['UI_TOKEN_LOAD'], 
                    UI_TOKEN['UI_TOKEN_EXIT']
                ]

        c = ui_command(commands,ui)

        if commands[c] == UI_TOKEN['UI_TOKEN_RULES']:
            ui_command([RULES, "OK"], ui)
        elif commands[c] == UI_TOKEN['UI_TOKEN_ROLL']:
            w1 = random.randrange(1,6)
            w2 = random.randrange(1,6)
            ui_command(["Du hast gewürfelt: " + str(w1) + " + " + str(w2)],ui, False)
            p = players[cur_player]
            p.move(w1+w2, 25)
            ui_display(properties,players,ui)
            action(fields[p.field],p, players, properties)
            cur_player = (cur_player + 1) % len(players)
        elif commands[c] == UI_TOKEN['UI_TOKEN_EXIT']:
            if yes_no("Bist du dir sicher?", ui):
                curses.curs_set(1)
                curses.echo()
                ui.stdscr.clear()
                ui.curs.refresh()
                running = False
        elif commands[c] == UI_TOKEN['UI_TOKEN_SAVE']:
            save_data(players, properties, ui_input("Dateiname:", ui))
        elif commands[c] == UI_TOKEN['UI_TOKEN_LOAD']:
            if yes_no("Bist du sicher? (Laufende Spieldaten gehen verloren)", ui):
                ui_delete_saved_commands(ui)
                players, properties = load_data(ui_input("Dateiname:", ui))
                ui_display(properties, players, ui)
