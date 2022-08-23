import imp
import re
import consts
import curses
from glob import glob
from lib import *

def ui_init():
    curs = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 11, -1)
    curses.init_pair(2, 0, 7)
    curses.init_pair(3, curses.COLOR_WHITE, -1)     #color 0: default
    curses.init_pair(4, curses.COLOR_RED, -1)       #color 1: red
    curses.init_pair(5, curses.COLOR_BLUE, -1)      #color 2: blue
    curses.init_pair(6, curses.COLOR_GREEN, -1)     #color 3: green
    stdscr = curses.initscr()
    return (curs, stdscr)

def ui_display(properties, players, ui):
    ui.stdscr.clear()
    ui.number_streets = len(properties)
    for i in range(ui.number_streets):
        if len(properties[i].name) > ui.width_streets:
            ui.width_streets = len(properties[i].name)
    
    #width owner
    ui.width_owner = 8
    for p in properties:
        if p.owner != None and ui.width_owner < len(p.owner.name):
            ui.width_owner = len(p.owner.name)

    #width rent
    ui.width_rent = 5
    if ui.width_rent < max(list(map(lambda s: len(s), consts.DRINKS))):
        ui.width_rent = len(p)

    #width players
    ui.number_players = len(players)
    ui.width_players = 8
    for i in range(ui.number_streets + 10):
        max_width = 0
        for p in players:
            if p.field == i:
                max_width += 1 + len(p.name)
        if max_width > ui.width_players:
            ui.width_players = max_width
    ui.width_players -= 1

    ui.max_width_command = ui.width - ui.width_streets - ui.width_owner - ui.width_rent - ui.width_players - 5
    ui.min_start_command = ui.width_streets + ui.width_owner + ui.width_rent + ui.width_players + 5


    #add streets
    ui.curs.addstr(0, 0, "┌")
    ui.curs.addstr(0, ui.width_streets + 1, "┬")
    ui.curs.addstr(1,0, "│Straßen")
    for i in range(ui.width_streets - 7):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, 0, "│")
    ui.curs.addstr(1, ui.width_streets + 1, "│")
    ui.curs.addstr(2, 0, "├")
    ui.curs.addstr(2, ui.width_streets + 1, "┼")
    ui.curs.addstr(ui.number_streets + 13, 0, "└")
    ui.curs.addstr(ui.number_streets + 13, ui.width_streets + 1, "┴")
    for i in range(ui.width_streets):
        ui.curs.addstr(0, i + 1, "─")
        ui.curs.addstr(2, i + 1, "─")
        ui.curs.addstr(ui.number_streets + 13, i + 1, "─")
    extra = 0
    for i in range(ui.number_streets + 10):
        ui.curs.move(3 + i, 0)
        ui.curs.addstr("│")
        if not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.addstr(properties[i - extra].name)
            width_field = len(properties[i - extra].name)
        elif i in {0, 13}:
            ui.curs.addstr("Duell")
            width_field = 5
            extra += 1
        else:
            ui.curs.addstr("Geld")
            width_field = 4
            extra += 1
        for i in range(ui.width_streets - width_field):
            ui.curs.addstr(" ")
        ui.curs.addstr("│")

    #add owner
    ui.curs.addstr(0, ui.width_streets + ui.width_owner + 2, "┬")
    ui.curs.addstr(1, ui.width_streets + 1, "│Besitzer")
    for i in range(ui.width_owner - 8):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, ui.width_streets + ui.width_owner + 2, "│")
    ui.curs.addstr(2, ui.width_streets + ui.width_owner + 2, "┼")
    ui.curs.addstr(ui.number_streets + 13, ui.width_streets + ui.width_owner + 2, "┴")
    for i in range(ui.width_owner):
        ui.curs.addstr(0, ui.width_streets + i + 2, "─")
        ui.curs.addstr(2, ui.width_streets + i + 2, "─")
        ui.curs.addstr(ui.number_streets + 13, ui.width_streets + i + 2, "─")
    extra = 0
    for i in range(ui.number_streets + 10):
        if not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.move(3 + i, ui.width_streets + 2)
            if properties[i - extra].owner != None:
                ui.curs.addstr(properties[i - extra].owner.name)
                width_field = len(properties[i - extra].owner.name)
            else:
                width_field = 0
            for i in range(width_field, ui.width_owner):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")
        else:
            ui.curs.move(3 + i, ui.width_streets + 2)
            extra += 1
            for i in range(0, ui.width_owner):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")

    #add rent
    ui.curs.addstr(0, ui.width_streets + ui.width_owner + ui.width_rent + 3, "┬")
    ui.curs.addstr(1, ui.width_streets + ui.width_owner + 2, "│Miete")
    for i in range(ui.width_rent - 5):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, ui.width_streets + ui.width_owner + ui.width_rent + 3, "│")
    ui.curs.addstr(2, ui.width_streets + ui.width_owner + ui.width_rent + 3, "┼")
    ui.curs.addstr(ui.number_streets + 13, ui.width_streets + ui.width_owner + ui.width_rent + 3, "┴")
    for i in range(ui.width_rent):
        ui.curs.addstr(0, ui.width_streets + ui.width_owner + i + 3, "─")
        ui.curs.addstr(2, ui.width_streets + ui.width_owner + i + 3, "─")
        ui.curs.addstr(ui.number_streets + 13, ui.width_streets + ui.width_owner + i + 3, "─")
    extra = 0
    for i in range(ui.number_streets + 10):
        if (not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}) and (properties[i - extra].owner != None):
            ui.curs.move(3 + i, ui.width_streets + ui.width_owner + 3)
            ui.curs.addstr(consts.DRINKS[properties[i - extra].rent])
            width_field = len(consts.DRINKS[properties[i - extra].rent])
            for i in range(width_field, ui.width_rent):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")
        elif not i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
            ui.curs.move(3 + i, ui.width_streets + ui.width_owner + 3)
            ui.curs.addstr(str(properties[i - extra].base_cost) + "$")
            width_field = len(str(properties[i - extra].base_cost) + "$")
            for i in range(width_field, ui.width_rent):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")   
        else:
            ui.curs.move(3 + i, ui.width_streets + ui.width_owner + 3)
            if i in {0, 3 ,6, 9, 12, 13, 15, 18, 21, 24}:
                extra += 1
            for i in range(0, ui.width_rent):
                ui.curs.addstr(" ")
            ui.curs.addstr("│")

    #add players
    ui.curs.addstr(0, ui.width_streets + ui.width_owner + ui.width_rent + ui.width_players + 4, "┐")
    ui.curs.addstr(1, ui.width_streets + ui.width_owner + ui.width_rent + 4, "Spieler")
    for i in range(ui.width_owner - 8):
        ui.curs.addstr(" ")
    ui.curs.addstr(1, ui.width_streets + ui.width_owner + ui.width_rent + ui.width_players + 4, "│")
    ui.curs.addstr(2, ui.width_streets + ui.width_owner + ui.width_rent + ui.width_players + 4, "┤")
    ui.curs.addstr(ui.number_streets + 13, ui.width_streets + ui.width_owner + ui.width_rent + ui.width_players + 4, "┘")
    for i in range(ui.width_players):
        ui.curs.addstr(0, ui.width_streets + ui.width_owner + ui.width_rent + i  + 4, "─")
        ui.curs.addstr(2, ui.width_streets + ui.width_owner + ui.width_rent + i  + 4, "─")
        ui.curs.addstr(ui.number_streets + 13, ui.width_streets + ui.width_owner + ui.width_rent + i + 4, "─")

    for i in range(0, ui.number_streets + 10):
        ui.curs.move(3 + i, ui.width_streets + ui.width_owner + ui.width_rent + 4)
        width_field = 1
        for p in players:
            if p.field == i:
                if width_field > 1:
                    ui.curs.addstr(" ")
                    width_field += 1
                ui.curs.addstr(p.name)
                width_field += len(p.name)
        for i in range(width_field - 1, ui.width_players):
            ui.curs.addstr(" ")
        ui.curs.addstr("│")
    ui.curs.refresh()


def ui_command(array, ui, delete=True):
    if len(array) < 1:
        return -1

    #clear
    if ui.saved_commands != []:
        for i in range(len(ui.saved_commands)*4 + 2):
            for j in range(ui.width_command):
                ui.curs.addstr(i, ui.start_command + j, " ")

    #print box
    ui.width_command = 0
    for a in array:
        len_a = __ui_len_colored_text__(a)
        if len_a > ui.width_command and len_a + 2 <= ui.max_width_command:
            ui.width_command = len_a + 2
    for a in ui.saved_commands:
        len_a = len(a.encode('utf-16-le')) // 2
        if len_a > ui.width_command and len_a + 2 <= ui.max_width_command:
            ui.width_command = len_a + 2
    ui.start_command = ui.min_start_command + (ui.max_width_command - ui.width_command) // 2

    if len(array) > 1:
        ui.curs.addstr(0 + ui.height_offset, ui.start_command, "┌")
        ui.curs.addstr(0 + ui.height_offset, ui.start_command + ui.width_command - 1, "┐")
        ui.curs.addstr(len(array) + 2 + ui.height_offset, ui.start_command, "└")
        ui.curs.addstr(len(array) + 2 + ui.height_offset, ui.start_command + ui.width_command - 1, "┘")
        for i in range(ui.width_command - 2):
            ui.curs.addstr(0 + ui.height_offset, ui.start_command + i + 1, "─")
            ui.curs.addstr(2 + ui.height_offset, ui.start_command + i + 1, "─")
            ui.curs.addstr(len(array) + 2 + ui.height_offset, ui.start_command + i + 1, "─")
        for i in range(len(array) + 1):
            if i == 1:
                ui.curs.addstr(i + 1 + ui.height_offset, ui.start_command, "├")
                ui.curs.addstr(i + 1 + ui.height_offset, ui.start_command + ui.width_command - 1, "┤")
            else:
                ui.curs.addstr(i + 1 + ui.height_offset, ui.start_command, "│")
                ui.curs.addstr(i + 1 + ui.height_offset, ui.start_command + ui.width_command - 1, "│")
    else:
        ui.curs.addstr(0 + ui.height_offset, ui.start_command, "┌")
        ui.curs.addstr(0 + ui.height_offset, ui.start_command + ui.width_command - 1, "┐")
        ui.curs.addstr(2 + ui.height_offset, ui.start_command, "└")
        ui.curs.addstr(2 + ui.height_offset, ui.start_command + ui.width_command - 1, "┘")
        for i in range(ui.width_command - 2):
            ui.curs.addstr(0 + ui.height_offset, ui.start_command + i + 1, "─")
            ui.curs.addstr(2 + ui.height_offset, ui.start_command + i + 1, "─")
            ui.curs.addstr(1 + ui.height_offset, ui.start_command, "│")
            ui.curs.addstr(1 + ui.height_offset, ui.start_command + ui.width_command - 1, "│")

    #print saved Commands
    __print_saved_commands__(ui)

    selected_answerer = 1
    
    #ui.curs.move(1 + ui.height_offset, ui.start_command + (ui.width_command - len(array[0])) // 2)
    #ui.curs.addstr(array[0])
    __ui_print_Color__(1 + ui.height_offset, ui.start_command + (ui.width_command - __ui_len_colored_text__(array[0])) // 2,array[0], ui)
    if len(array) == 1:
        ui.height_offset += 4
        ui.saved_commands.append(array[0])
        return 0
    while True:
        __print_answerers__(array, selected_answerer, ui)
        input = ui.stdscr.getch()
        if input == 65:
            if selected_answerer > 1:
                selected_answerer -= 1
        elif input == 66:
            if selected_answerer < len(array) - 1:
                selected_answerer += 1
        elif input == 10:
            if delete:
                for i in range(len(array) + 3 + ui.height_offset):
                    for j in range(ui.width_command):
                        ui.curs.addstr(i, ui.start_command + j, " ")
                ui.curs.refresh()
                ui.height_offset = 0
                ui.saved_commands = []
            else:
                ui.height_offset += 4
                ui.saved_commands.append(array[0])
                ui.height_offset_answerers = len(array) + 1
            return selected_answerer


def __print_answerers__(array, selected_answerer,ui):
    for i in range(1, len(array)):
        ui.curs.move(2 + i + ui.height_offset, ui.start_command + (ui.width_command - len(array[i])) // 2)
        if i == selected_answerer:
            ui.curs.addstr(array[i], curses.color_pair(2))
            curses.use_default_colors()
        else:
            ui.curs.addstr(array[i])
    ui.curs.refresh()

def __print_saved_commands__(ui):
    if len(ui.saved_commands) != 0:
        for i in range(len(ui.saved_commands)):
            ui.curs.addstr(0 + i * 4, ui.start_command, "┌")
            ui.curs.addstr(0 + i * 4, ui.start_command + ui.width_command - 1, "┐")
            ui.curs.addstr(1 + i * 4, ui.start_command, "│")
            ui.curs.addstr(1 + i * 4, ui.start_command + ui.width_command - 1, "│")
            ui.curs.addstr(2 + i * 4, ui.start_command, "└")
            ui.curs.addstr(2 + i * 4, ui.start_command + ui.width_command - 1, "┘")
            for j in range(ui.width_command - 2):
                ui.curs.addstr(0 + i * 4, ui.start_command + j + 1, "─")
                ui.curs.addstr(2 + i * 4, ui.start_command + j + 1, "─")
            ui.curs.addstr(1 + i * 4, ui.start_command + (ui.width_command - len(ui.saved_commands[i])) // 2, ui.saved_commands[i])

def ui_delete_saved_commands(ui):
    for i in range(ui.height_offset + ui.height_offset_answerers):
        for j in range(ui.width_command):
            ui.curs.addstr(i, ui.start_command + j, " ")
    ui.curs.refresh()
    ui.height_offset = 0
    ui.saved_commands = []     

def ui_input(question, ui):

    #print box
    ui.width_command = 0
    if len(question) + 2 <= ui.max_width_command:
            ui.width_command = len(question) + 2
    ui.start_command = ui.min_start_command + (ui.max_width_command - ui.width_command) // 2

    ui.curs.addstr(0, ui.start_command, "┌")
    ui.curs.addstr(0, ui.start_command + ui.width_command - 1, "┐")
    ui.curs.addstr(1, ui.start_command , "│")
    ui.curs.addstr(1, ui.start_command + ui.width_command - 1, "│")
    ui.curs.addstr(2, ui.start_command , "├")
    ui.curs.addstr(2, ui.start_command + ui.width_command - 1, "┤")
    ui.curs.addstr(3, ui.start_command , "│")
    ui.curs.addstr(3, ui.start_command + ui.width_command - 1, "│")
    ui.curs.addstr(4, ui.start_command, "└")
    ui.curs.addstr(4, ui.start_command + ui.width_command - 1, "┘")
    for i in range(ui.width_command - 2):
        ui.curs.addstr(0, ui.start_command + i + 1, "─")
        ui.curs.addstr(2, ui.start_command + i + 1, "─")
        ui.curs.addstr(4, ui.start_command + i + 1, "─")

    ui.curs.addstr(1, ui.start_command + 1, question)
    ui.curs.move(3, ui.start_command + 1)
    curses.echo()
    curses.curs_set(1)
    ui.curs.refresh()

    input = ui.stdscr.getstr().decode()

    curses.noecho()
    curses.curs_set(0)
    for i in range(5):
        for j in range(ui.width_command):
            ui.curs.addstr(i, ui.start_command + j, " ")
    ui.curs.refresh()
    return input

def __ui_print_Color__(y, x, text, ui):
    splitedText = re.split('(\§)', text)
    ui.curs.move(y, x)
    i = 0
    while i < len(splitedText):
        if splitedText[i] == "§":
            if splitedText[i + 1] == "1":
                ui.curs.addstr(splitedText[i + 3], curses.color_pair(4))
            if splitedText[i + 1] == "2":
                ui.curs.addstr(splitedText[i + 3], curses.color_pair(5))
            if splitedText[i + 1] == "3":
                ui.curs.addstr(splitedText[i + 3], curses.color_pair(6))
            i += 4
        else:
            ui.curs.addstr(splitedText[i], curses.color_pair(3))
            i += 1

def __ui_len_colored_text__(text):
    splitedText = re.split('(\§)', text)
    i = 0
    result = 0
    while i < len(splitedText):
        if splitedText[i] == "§":
            result += len(splitedText[i + 3].encode('utf-16-le')) // 2
            i += 4
        else:
            result += len(splitedText[i].encode('utf-16-le')) // 2
            i += 1
    return result