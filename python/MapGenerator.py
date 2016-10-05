import Map
import libtcodpy as libtcod
import Tile
from random import random, randrange
import time
import copy


class MapGenerator:

    def __init__(self):
        pass

    def generateCave(self, x, y, main_console):
        newMap = []
        for i in range(y):
            collector = []
            for j in range(x):
                r = random()
                if (r <= 0.35):
                    collector.append('#')
                else:
                    collector.append(' ')
            newMap.append(collector)
        current_map = Map.Map(main_console)
        current_map.convert_crude(newMap, True)
        current_map.draw_map()
        libtcod.console_blit(main_console,
                             0, 0, x, y,
                             0, 0, 0)
        libtcod.console_set_default_foreground(None, libtcod.grey)
        libtcod.console_set_default_background(None, libtcod.black)
        libtcod.console_flush()
        for k in range(7):
            upMap = copy.deepcopy(newMap)
            for i in range(y):
                for j in range(x):
                    n = better_check(newMap, j, i, 5)
                    fill = False
                    if (k < 3 or k == 5):
                        if (n == 0):
                            fill = True
                    if ((n >= 5) or fill):
                        upMap[i][j] = '#'
                    else:
                  		upMap[i][j] = ' '
            del newMap
            newMap = copy.deepcopy(upMap)
            time.sleep(1)
            key = libtcod.console_check_for_keypress()
            if key.vk == libtcod.KEY_ESCAPE:
                break
            current_map.convert_crude(newMap, True)
            current_map.draw_map()
            libtcod.console_blit(main_console,
                                 0, 0, x, y,
                                 0, 0, 0)
            libtcod.console_set_default_foreground(None, libtcod.grey)
            libtcod.console_set_default_background(None, libtcod.black)
            libtcod.console_flush()
        return newMap


def better_check(in_map, x, y, n):
    max_x = (len(in_map[0]))
    max_y = (len(in_map))
    i = 0
    for off_x in [-1, 0, 1]:
        if (((x + off_x) >= max_x) or (x + off_x) < 0):
            i += 3
            continue
        for off_y in [-1, 0, 1]:
            if (((y + off_y) >= max_y) or (y + off_y) < 0):
                i += 1
            elif ((in_map[(y + off_y)][(x + off_x)]) == '#'):
                i += 1
    return i