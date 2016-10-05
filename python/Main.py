import math
import os
import libtcodpy as libtcod
import Tile
import Map
import MapGenerator
from random import random, randrange

smap = ['##############################################',
        '#######################      #################',
        '#####################    #     ###############',
        '######################  ###        ###########',
        '##################      #####             ####',
        '################       ########    ###### ####',
        '###############      #################### ####',
        '################    ######                  ##',
        '########   #######  ######   #     #     #  ##',
        '########   ######      ###      B    ii     ##',
        '########                        B    ii    i##',
        '####       ######      ###   #     #     #  ##',
        '#### ###   ########## ####                  ##',
        '#### ###   ##########   ###########=##########',
        '#### ##################   #####          #####',
        '#### ###             #### #####          #####',
        '####           #     ####         t      #####',
        '########       #     #### #####          #####',
        '########       #####      ####################',
        '##############################################',
        ]

smap1 = ['##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '###############iiiiiiiiiii#iiiii##############',
         '###############iii#iiiiiiiiiiiii##############',
         '###############iiiiiiiiiiii#iiii##############',
         '###############i#iiiiiiiiiiiiiii##############',
         '################iiiiiiiiii#iiiii##############',
         '###############iiiiiiiiiiiiiiii###############',
         '###############iiiiiiiii#iiiiiii      ########',
         '###############ii#iiiiiiiiiiiiii      ########',
         '###############iiiiiiiiiiiiiiii###############',
         '###############iiiiiiiiii#iiiiii##############',
         '###############iiiiiiii#iii#iiii##############',
         '###############iiiiiiiiiiiiiiiii##############',
         '###############################  #############',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################',
         '##############################################'
         ]


SCREEN_WIDTH = 100
SCREEN_HEIGHT = 80
SCREEN_X = 0
SCREEN_Y = 0
cwd_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.abspath(os.path.join(cwd_path, b'..', b'data'))
font = os.path.join(data_path, b'fonts', b'consolas10x10_gs_tc.png')
libtcod.console_set_custom_font(
    font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, b'libtcod testing', False)
main_console = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
first = True
fov_px = 20
fov_py = 10


def handle_keys(key, playerx, playery):

    update = False
    # movement keys
    if key.vk == libtcod.KEY_UP:
        update = "move"
        playery -= 1

    elif key.vk == (libtcod.KEY_DOWN):
        update = "move"
        playery += 1

    elif key.vk == (libtcod.KEY_LEFT):
        update = "move"
        playerx -= 1

    elif key.vk == (libtcod.KEY_RIGHT):
        update = "move"
        playerx += 1
    elif key.c == ord('m'):
        update = "map"
    print "Update is: ", update

    return (update, (playerx, playery))


def gen_new():
    global main_console, fov_px, fov_py, current_map
    libtcod.console_clear(None)
    libtcod.console_clear(main_console)
    libtcod.console_flush()
    gen = MapGenerator.MapGenerator()
    newMap = gen.generateCave(100, 80, main_console)
    libtcod.console_clear(None)
    libtcod.console_clear(main_console)
    libtcod.console_flush()
    while True:
        rx = randrange(20, 60)
        ry = randrange(30, 50)
        if (newMap[ry][rx] == ' '):
            break
    (fov_px, fov_py) = (rx, ry)
    while True:
        rx = randrange(20, 60)
        ry = randrange(30, 50)
        if (newMap[ry][rx] == ' '):
            break
    newMap[ry][rx] = 's'
    current_map.convert_crude(newMap)
    current_map.update_fov(fov_px, fov_py)
    current_map.draw_map()
    libtcod.console_put_char(main_console, fov_px, fov_py, '@',
                             libtcod.BKGND_NONE)
    libtcod.console_blit(main_console,
                         0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                         0, SCREEN_X, SCREEN_Y)
    libtcod.console_flush()

current_map = Map.Map(main_console)
current_map.convert_crude(smap)
current_map.update_fov(fov_px, fov_py)
current_map.draw_map()
libtcod.console_put_char(main_console, fov_px, fov_py, '@',
                         libtcod.BKGND_NONE)
libtcod.console_blit(main_console,
                     0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                     0, SCREEN_X, SCREEN_Y)
libtcod.console_set_default_foreground(None, libtcod.grey)
libtcod.console_set_default_background(None, libtcod.black)
libtcod.console_flush()
while not libtcod.console_is_window_closed():

    key = libtcod.console_wait_for_keypress(True)  # turn-based
    libtcod.console_flush()
    if key.vk == libtcod.KEY_ESCAPE:
        break
    (hasUpdate, newPos) = handle_keys(key, fov_px, fov_py)
    if hasUpdate == "move":
        (pos_x, pos_y) = newPos
        while ((fov_px != pos_x) or (fov_py != pos_y)):
            if current_map.checkWalkable(pos_x, pos_y):
                onStep = current_map.checkOnStep(pos_x, pos_y)
                if (not onStep):
                    (fov_px, fov_py) = (pos_x, pos_y)
                elif (onStep.__name__ == "trigger"):
                    (fov_px, fov_py) = (pos_x, pos_y)
                    onStep("door1", current_map)
                elif (onStep.__name__ == "gennewmap"):
                    gen_new()
                else:
                    (tx, ty) = (pos_x, pos_y)
                    print "t: ", (tx, ty)
                    print "fov: ", (fov_px, fov_py)
                    (pos_x, pos_y) = onStep(fov_px, fov_py, pos_x, pos_y)
                    print "pos: ", (pos_x, pos_y)
                    (fov_px, fov_py) = (tx, ty)
                    print "fov: ", (fov_px, fov_py)
            else:
                (pos_x, pos_y) = (fov_px, fov_py)
            print "cur: ", (fov_px, fov_py)
            current_map.update_fov(fov_px, fov_py)
            current_map.draw_map()
            libtcod.console_put_char(main_console, fov_px, fov_py, '@',
                                     libtcod.BKGND_NONE)
            libtcod.console_blit(main_console,
                                 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                 0, SCREEN_X, SCREEN_Y)
            libtcod.console_flush()
    elif hasUpdate:
        libtcod.console_clear(None)
        libtcod.console_clear(main_console)
        libtcod.console_flush()
        gen = MapGenerator.MapGenerator()
        newMap = gen.generateCave(100, 80, main_console)
        libtcod.console_clear(None)
        libtcod.console_clear(main_console)
        libtcod.console_flush()
        while True:
            rx = randrange(20, 60)
            ry = randrange(30, 50)
            if (newMap[ry][rx] == ' '):
                break
        (fov_px, fov_py) = (rx, ry)
        while True:
            rx = randrange(20, 60)
            ry = randrange(30, 50)
            if (newMap[ry][rx] == ' '):
                break
        newMap[ry][rx] = 's'
        current_map.convert_crude(newMap)
        current_map.update_fov(fov_px, fov_py)
        current_map.draw_map()
        libtcod.console_put_char(main_console, fov_px, fov_py, '@',
                                 libtcod.BKGND_NONE)
        libtcod.console_blit(main_console,
                             0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                             0, SCREEN_X, SCREEN_Y)
        libtcod.console_flush()
        print "done"
        #fov_px = 20
        #fov_py = 10

       # current_map = Map.Map(main_console)
       # current_map.convert_crude(smap1)
       # current_map.update_fov(fov_px, fov_py)
       # current_map.draw_map()
       # libtcod.console_put_char(main_console, fov_px, fov_py, '@',
       #                          libtcod.BKGND_NONE)
       # libtcod.console_blit(main_console,
       #                      0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
       # 0, SCREEN_X, SCREEN_Y)
        #libtcod.console_set_default_foreground(None, libtcod.grey)
        #libtcod.console_set_default_background(None, libtcod.black)
        # libtcod.console_flush()
