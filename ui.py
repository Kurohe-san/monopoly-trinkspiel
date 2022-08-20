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

def ui_display(properties, players, curs, stdscr):
    widthStreets = 7
    widthOwner = 8
    widthPlayers = 0
    widthCommand = None
    startCommand = None
    height,width = stdscr.getmaxyx()
    numberStreets = len(properties)
    for i in range(numberStreets):
        if len(properties[i].name) > widthStreets:
            widthStreets = len(properties[i].name)
    numberPlayers = len(players)
    for i in range(numberPlayers):
        widthPlayers += len(players[i].name) + 1
    widthPlayers -= 1

    widthCommand = width - widthStreets - widthOwner - widthPlayers - 4 - 100
    startCommand = width//2 - widthCommand//2


    #add streets
    curs.addstr(0,0, "|Straßen|") 
    curs.move(1, 0)
    curs.addstr("|")
    for i in range(widthStreets):
        curs.addstr("-")
    curs.addstr("|")
    for i in range(numberStreets):
        curs.move(2 + i, 0)
        curs.addstr("|")
        curs.addstr(properties[i].name)
        for i in range(widthStreets - len(properties[i].name)):
            curs.addstr(" ")
        curs.addstr("|")

    #add owner
    curs.addstr(0,widthStreets + 2, "Besitzer|")
    curs.move(1, widthStreets + 2)
    for i in range(widthOwner):
        curs.addstr("-")
    curs.addstr("|")
    for i in range(numberStreets):
        curs.move(2 + i, widthStreets + 2)
        for i in range(widthOwner):
            curs.addstr(" ")
        curs.addstr("|")

    #add players
    curs.addstr(0,widthStreets + widthOwner + 3, "Spieler")
    for i in range(widthPlayers - 7):
        curs.addstr(" ")
    curs.addstr("|")
    curs.move(1, widthStreets + widthOwner + 3)
    for i in range(widthPlayers):
        curs.addstr("-")
    curs.addstr("|")
    for i in range(0, numberStreets):
        curs.move(2 + i, widthStreets + widthOwner + 3)
        for p in players:
            if p.field == i:
                curs.addstr(p.name)
        for i in range(widthPlayers):
            curs.addstr(" ")
        curs.addstr("|")

    curs.refresh()

def ui_command(array, curs, stdscr):
    if len(array) < 2:
        return -1
    
    selectedAnswerer = 1
    startCommand = 100
    curs.move(0, startCommand)
    curs.addstr(array[0])
    while True:
        __print_answerers__(array, selectedAnswerer, curs, startCommand)
        input = stdscr.getch()
        if input == 65:
            if selectedAnswerer > 1:
                selectedAnswerer -= 1
        elif input == 66:
            if selectedAnswerer < len(array) - 1:
                selectedAnswerer += 1
        elif input == 10:
            for i in range(len(array) + 1):
                for j in range(widthCommand):
                    curs.addstr(i, startCommand + j, " ")
            curs.refresh()
            return selectedAnswerer


def __print_answerers__(array, selectedAnswerer,curs,startCommand):
    for i in range(1, len(array)):
        curs.move(1 + i, startCommand)
        if i == selectedAnswerer:
            curs.addstr(array[i], curses.color_pair(2))
            curses.use_default_colors()
        else:
            curs.addstr(array[i])
    curs.refresh()
