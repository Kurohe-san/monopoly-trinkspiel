from lib import *
import curses
from glob import glob
import numbers
import time

def ui_init():
    curs = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 11, -1)
    curses.init_pair(2, 0, 7)
    stdscr = curses.initscr()
    return (curs, stdscr)

def ui_display(properties, players, ui):
    ui.numberStreets = len(properties)
    for i in range(ui.numberStreets):
        if len(properties[i].name) > ui.widthStreets:
            ui.widthStreets = len(properties[i].name)
    
    #width owners
    ui.widthOwner = 8
    for p in properties:
        if p.owner != None and ui.widthOwner < len(p.owner.name):
            ui.widthOwner = len(p.owner.name)

    #width players
    ui.numberPlayers = len(players)
    ui.widthPlayers = 8
    for i in range(ui.numberStreets + 10):
        max = 0
        for p in players:
            if p.field == i:
                max += 1 + len(p.name)
        if max > ui.widthPlayers:
            ui.widthPlayers = max
    ui.widthPlayers -= 1

    ui.widthCommand = ui.width - ui.widthStreets - ui.widthOwner - ui.widthPlayers - 4 - 100
    ui.startCommand = ui.width//2 - ui.widthCommand//2


    #add streets
    ui.curs.addstr(0,0, "|Straßen|") 
    ui.curs.move(1, 0)
    ui.curs.addstr("|")
    for i in range(ui.widthStreets):
        ui.curs.addstr("-")
    ui.curs.addstr("|")
    extra = 0
    for i in range(ui.numberStreets + 10):
        ui.curs.move(2 + i, 0)
        ui.curs.addstr("|")
        if not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.addstr(properties[i - extra].name)
            widthField = len(properties[i - extra].name)
        elif i in {0, 13}:
            ui.curs.addstr("Duell")
            widthField = 5
            extra += 1
        else:
            ui.curs.addstr("Geld")
            widthField = 4
            extra += 1
        for i in range(ui.widthStreets - widthField):
            ui.curs.addstr(" ")
        ui.curs.addstr("|")

    #add owner
    ui.curs.addstr(0,ui.widthStreets + 2, "Besitzer|")
    ui.curs.move(1, ui.widthStreets + 2)
    for i in range(ui.widthOwner):
        ui.curs.addstr("-")
    ui.curs.addstr("|")
    extra = 0
    for i in range(ui.numberStreets + 10):
        if not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.move(2 + i, ui.widthStreets + 2)
            if properties[i - extra].owner != None:
                ui.curs.addstr(properties[i - extra].owner.name)
                widthField = len(properties[i - extra].owner.name)
            else:
                widthField = 0
            for i in range(widthField, ui.widthOwner):
                ui.curs.addstr(" ")
            ui.curs.addstr("|")
        else:
            ui.curs.move(2 + i, ui.widthStreets + 2)
            extra += 1
            for i in range(0, ui.widthOwner):
                ui.curs.addstr(" ")
            ui.curs.addstr("|")

    #add players
    ui.curs.addstr(0,ui.widthStreets + ui.widthOwner + 3, "Spieler")
    for i in range(ui.widthPlayers - 7):
        ui.curs.addstr(" ")
    ui.curs.addstr("|           ")
    ui.curs.move(1, ui.widthStreets + ui.widthOwner + 3)
    for i in range(ui.widthPlayers):
        ui.curs.addstr("-")
    ui.curs.addstr("|            ")
    for i in range(0, ui.numberStreets + 10):
        ui.curs.move(2 + i, ui.widthStreets + ui.widthOwner + 3)
        widthField = 1
        for p in players:
            if p.field == i:
                if widthField > 1:
                    ui.curs.addstr(" ")
                    widthField += 1
                ui.curs.addstr(p.name)
                widthField += len(p.name)
        for i in range(widthField - 1, ui.widthPlayers):
            ui.curs.addstr(" ")
        ui.curs.addstr("|")
        ui.curs.addstr("               ")

    ui.curs.refresh()

def ui_command(array, ui):
    if len(array) < 2:
        return -1
    
    selectedAnswerer = 1
    
    ui.curs.move(0, ui.startCommand)
    ui.curs.addstr(array[0])
    while True:
        __print_answerers__(array, selectedAnswerer, ui)
        input = ui.stdscr.getch()
        if input == 65:
            if selectedAnswerer > 1:
                selectedAnswerer -= 1
        elif input == 66:
            if selectedAnswerer < len(array) - 1:
                selectedAnswerer += 1
        elif input == 10:
            for i in range(len(array) + 1):
                for j in range(ui.widthCommand):
                    ui.curs.addstr(i, ui.startCommand + j, " ")
            ui.curs.refresh()
            return selectedAnswerer


def __print_answerers__(array, selectedAnswerer,ui):
    for i in range(1, len(array)):
        ui.curs.move(1 + i, ui.startCommand)
        if i == selectedAnswerer:
            ui.curs.addstr(array[i], curses.color_pair(2))
            curses.use_default_colors()
        else:
            ui.curs.addstr(array[i])
    ui.curs.refresh()
