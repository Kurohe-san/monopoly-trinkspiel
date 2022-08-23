from lib import *
import lib
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
    ui.stdscr.clear()
    ui.numberStreets = len(properties)
    for i in range(ui.numberStreets):
        if len(properties[i].name) > ui.widthStreets:
            ui.widthStreets = len(properties[i].name)
    
    #width owner
    ui.widthOwner = 8
    for p in properties:
        if p.owner != None and ui.widthOwner < len(p.owner.name):
            ui.widthOwner = len(p.owner.name)

    #width rent
    ui.widthRent = 5
    if ui.widthRent < max(list(map(lambda s: len(s), lib.DRINKS))):
        ui.widthRent = len(p)

    #width players
    ui.numberPlayers = len(players)
    ui.widthPlayers = 8
    for i in range(ui.numberStreets + 10):
        maxWidth = 0
        for p in players:
            if p.field == i:
                maxWidth += 1 + len(p.name)
        if maxWidth > ui.widthPlayers:
            ui.widthPlayers = maxWidth
    ui.widthPlayers -= 1

    ui.maxWidthCommand = ui.width - ui.widthStreets - ui.widthOwner - ui.widthRent - ui.widthPlayers - 5
    ui.minStartCommand = ui.widthStreets + ui.widthOwner + ui.widthRent + ui.widthPlayers + 5


    #add streets
    ui.curs.addstr(0, 0, "┌")
    ui.curs.addstr(0, ui.widthStreets + 1, "┬")
    ui.curs.addstr(1,0, "│Straßen")
    for i in range(ui.widthStreets - 7):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, 0, "│")
    ui.curs.addstr(1, ui.widthStreets + 1, "│")
    ui.curs.addstr(2, 0, "├")
    ui.curs.addstr(2, ui.widthStreets + 1, "┼")
    ui.curs.addstr(ui.numberStreets + 13, 0, "└")
    ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + 1, "┴")
    for i in range(ui.widthStreets):
        ui.curs.addstr(0, i + 1, "─")
        ui.curs.addstr(2, i + 1, "─")
        ui.curs.addstr(ui.numberStreets + 13, i + 1, "─")
    extra = 0
    for i in range(ui.numberStreets + 10):
        ui.curs.move(3 + i, 0)
        ui.curs.addstr("│")
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
        ui.curs.addstr("│")

    #add owner
    ui.curs.addstr(0, ui.widthStreets + ui.widthOwner + 2, "┬")
    ui.curs.addstr(1, ui.widthStreets + 1, "│Besitzer")
    for i in range(ui.widthOwner - 8):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, ui.widthStreets + ui.widthOwner + 2, "│")
    ui.curs.addstr(2, ui.widthStreets + ui.widthOwner + 2, "┼")
    ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + ui.widthOwner + 2, "┴")
    for i in range(ui.widthOwner):
        ui.curs.addstr(0, ui.widthStreets + i + 2, "─")
        ui.curs.addstr(2, ui.widthStreets + i + 2, "─")
        ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + i + 2, "─")
    extra = 0
    for i in range(ui.numberStreets + 10):
        if not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.move(3 + i, ui.widthStreets + 2)
            if properties[i - extra].owner != None:
                ui.curs.addstr(properties[i - extra].owner.name)
                widthField = len(properties[i - extra].owner.name)
            else:
                widthField = 0
            for i in range(widthField, ui.widthOwner):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")
        else:
            ui.curs.move(3 + i, ui.widthStreets + 2)
            extra += 1
            for i in range(0, ui.widthOwner):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")

    #add rent
    ui.curs.addstr(0, ui.widthStreets + ui.widthOwner + ui.widthRent + 3, "┬")
    ui.curs.addstr(1, ui.widthStreets + ui.widthOwner + 2, "│Miete")
    for i in range(ui.widthRent - 5):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, ui.widthStreets + ui.widthOwner + ui.widthRent + 3, "│")
    ui.curs.addstr(2, ui.widthStreets + ui.widthOwner + ui.widthRent + 3, "┼")
    ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + ui.widthOwner + ui.widthRent + 3, "┴")
    for i in range(ui.widthRent):
        ui.curs.addstr(0, ui.widthStreets + ui.widthOwner + i + 3, "─")
        ui.curs.addstr(2, ui.widthStreets + ui.widthOwner + i + 3, "─")
        ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + ui.widthOwner + i + 3, "─")
    extra = 0
    for i in range(ui.numberStreets + 10):
        if (not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}) and (properties[i - extra].owner != None):
            ui.curs.move(3 + i, ui.widthStreets + ui.widthOwner + 3)
            ui.curs.addstr(lib.DRINKS[properties[i - extra].rent])
            widthField = len(lib.DRINKS[properties[i - extra].rent])
            for i in range(widthField, ui.widthRent):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")
        elif not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.move(3 + i, ui.widthStreets + ui.widthOwner + 3)
            ui.curs.addstr(str(properties[i - extra].base_cost) + "$")
            widthField = len(str(properties[i - extra].base_cost) + "$")
            for i in range(widthField, ui.widthRent):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")   
        else:
            ui.curs.move(3 + i, ui.widthStreets + ui.widthOwner + 3)
            if i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
                extra += 1
            for i in range(0, ui.widthRent):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")

    #add players
    ui.curs.addstr(0, ui.widthStreets + ui.widthOwner + ui.widthRent + ui.widthPlayers + 4, "┐")
    ui.curs.addstr(1, ui.widthStreets + ui.widthOwner + ui.widthRent + 4, "Spieler")
    for i in range(ui.widthOwner - 8):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, ui.widthStreets + ui.widthOwner + ui.widthRent + ui.widthPlayers + 4, "│")
    ui.curs.addstr(2, ui.widthStreets + ui.widthOwner + ui.widthRent + ui.widthPlayers + 4, "┤")
    ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + ui.widthOwner + ui.widthRent + ui.widthPlayers + 4, "┘")
    for i in range(ui.widthPlayers):
        ui.curs.addstr(0, ui.widthStreets + ui.widthOwner + ui.widthRent + i  + 4, "─")
        ui.curs.addstr(2, ui.widthStreets + ui.widthOwner + ui.widthRent + i  + 4, "─")
        ui.curs.addstr(ui.numberStreets + 13, ui.widthStreets + ui.widthOwner + ui.widthRent + i + 4, "─")

    for i in range(0, ui.numberStreets + 10):
        ui.curs.move(3 + i, ui.widthStreets + ui.widthOwner + ui.widthRent + 4)
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
        ui.curs.addstr("│")
    ui.curs.refresh()


def ui_command(array, ui, delete=True):
    if len(array) < 1:
        return -1

    #clear
    if ui.savedCommands != []:
        for i in range(len(ui.savedCommands)*4 + 2):
            for j in range(ui.widthCommand):
                ui.curs.addstr(i, ui.startCommand + j, " ")

    #print box
    ui.widthCommand = 0
    for a in array:
        lenA = len(a.encode('utf-16-le')) // 2
        if lenA > ui.widthCommand and lenA + 2 <= ui.maxWidthCommand:
            ui.widthCommand = lenA + 2
    for a in ui.savedCommands:
        lenA = len(a.encode('utf-16-le')) // 2
        if lenA > ui.widthCommand and lenA + 2 <= ui.maxWidthCommand:
            ui.widthCommand = lenA + 2
    ui.startCommand = ui.minStartCommand + (ui.maxWidthCommand - ui.widthCommand) // 2

    if len(array) > 1:
        ui.curs.addstr(0 + ui.heightOffset, ui.startCommand, "┌")
        ui.curs.addstr(0 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "┐")
        ui.curs.addstr(len(array) + 2 + ui.heightOffset, ui.startCommand, "└")
        ui.curs.addstr(len(array) + 2 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "┘")
        for i in range(ui.widthCommand - 2):
            ui.curs.addstr(0 + ui.heightOffset, ui.startCommand + i + 1, "─")
            ui.curs.addstr(2 + ui.heightOffset, ui.startCommand + i + 1, "─")
            ui.curs.addstr(len(array) + 2 + ui.heightOffset, ui.startCommand + i + 1, "─")
        for i in range(len(array) + 1):
            if i == 1:
                ui.curs.addstr(i + 1 + ui.heightOffset, ui.startCommand, "├")
                ui.curs.addstr(i + 1 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "┤")
            else:
                ui.curs.addstr(i + 1 + ui.heightOffset, ui.startCommand, "│")
                ui.curs.addstr(i + 1 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "│")
    else:
        ui.curs.addstr(0 + ui.heightOffset, ui.startCommand, "┌")
        ui.curs.addstr(0 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "┐")
        ui.curs.addstr(2 + ui.heightOffset, ui.startCommand, "└")
        ui.curs.addstr(2 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "┘")
        for i in range(ui.widthCommand - 2):
            ui.curs.addstr(0 + ui.heightOffset, ui.startCommand + i + 1, "─")
            ui.curs.addstr(2 + ui.heightOffset, ui.startCommand + i + 1, "─")
            ui.curs.addstr(1 + ui.heightOffset, ui.startCommand, "│")
            ui.curs.addstr(1 + ui.heightOffset, ui.startCommand + ui.widthCommand - 1, "│")

    #print saved Commands
    __print_saved_Commands__(ui)

    selectedAnswerer = 1
    
    ui.curs.move(1 + ui.heightOffset, ui.startCommand + (ui.widthCommand - len(array[0])) // 2)
    ui.curs.addstr(array[0])
    if len(array) == 1:
        ui.heightOffset += 4
        ui.savedCommands.append(array[0])
        return 0
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
            if delete:
                for i in range(len(array) + 3 + ui.heightOffset):
                    for j in range(ui.widthCommand):
                        ui.curs.addstr(i, ui.startCommand + j, " ")
                ui.curs.refresh()
                ui.heightOffset = 0
                ui.savedCommands = []
            else:
                ui.heightOffset += 4
                ui.savedCommands.append(array[0])
            return selectedAnswerer


def __print_answerers__(array, selectedAnswerer,ui):
    for i in range(1, len(array)):
        ui.curs.move(2 + i + ui.heightOffset, ui.startCommand + (ui.widthCommand - len(array[i])) // 2)
        if i == selectedAnswerer:
            ui.curs.addstr(array[i], curses.color_pair(2))
            curses.use_default_colors()
        else:
            ui.curs.addstr(array[i])
    ui.curs.refresh()

def __print_saved_Commands__(ui):
    if len(ui.savedCommands) != 0:
        for i in range(len(ui.savedCommands)):
            ui.curs.addstr(0 + i * 4, ui.startCommand, "┌")
            ui.curs.addstr(0 + i * 4, ui.startCommand + ui.widthCommand - 1, "┐")
            ui.curs.addstr(1 + i * 4, ui.startCommand, "│")
            ui.curs.addstr(1 + i * 4, ui.startCommand + ui.widthCommand - 1, "│")
            ui.curs.addstr(2 + i * 4, ui.startCommand, "└")
            ui.curs.addstr(2 + i * 4, ui.startCommand + ui.widthCommand - 1, "┘")
            for j in range(ui.widthCommand - 2):
                ui.curs.addstr(0 + i * 4, ui.startCommand + j + 1, "─")
                ui.curs.addstr(2 + i * 4, ui.startCommand + j + 1, "─")
            ui.curs.addstr(1 + i * 4, ui.startCommand + (ui.widthCommand - len(ui.savedCommands[i])) // 2, ui.savedCommands[i])
            

def ui_input(question, ui):

    #print box
    ui.widthCommand = 0
    if len(question) + 2 <= ui.maxWidthCommand:
            ui.widthCommand = len(question) + 2
    ui.startCommand = ui.minStartCommand + (ui.maxWidthCommand - ui.widthCommand) // 2

    ui.curs.addstr(0, ui.startCommand, "┌")
    ui.curs.addstr(0, ui.startCommand + ui.widthCommand - 1, "┐")
    ui.curs.addstr(1, ui.startCommand , "│")
    ui.curs.addstr(1, ui.startCommand + ui.widthCommand - 1, "│")
    ui.curs.addstr(2, ui.startCommand , "├")
    ui.curs.addstr(2, ui.startCommand + ui.widthCommand - 1, "┤")
    ui.curs.addstr(3, ui.startCommand , "│")
    ui.curs.addstr(3, ui.startCommand + ui.widthCommand - 1, "│")
    ui.curs.addstr(4, ui.startCommand, "└")
    ui.curs.addstr(4, ui.startCommand + ui.widthCommand - 1, "┘")
    for i in range(ui.widthCommand - 2):
        ui.curs.addstr(0, ui.startCommand + i + 1, "─")
        ui.curs.addstr(2, ui.startCommand + i + 1, "─")
        ui.curs.addstr(4, ui.startCommand + i + 1, "─")

    ui.curs.addstr(1, ui.startCommand + 1, question)
    ui.curs.move(3, ui.startCommand + 1)
    curses.echo()
    curses.curs_set(1)
    ui.curs.refresh()

    input = ui.stdscr.getstr().decode()

    curses.noecho()
    curses.curs_set(0)
    for i in range(5):
        for j in range(ui.widthCommand):
            ui.curs.addstr(i, ui.startCommand + j, " ")
    ui.curs.refresh()
    return input