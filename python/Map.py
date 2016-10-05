import libtcodpy as libtcod
import Tile


class Map:
    def __init__(self, console):
        self.console = console
        self.map = None
        self.map_data = []
        self.map_size = (0, 0)
        self.objects = {}

    def load_map(self, map_data):
        self.map_data = map_data
        self.map = libtcod.map_new(len(map_data[0]), len(map_data))
        self.map_size = (len(map_data[0]), len(map_data))
        for y in range(len(map_data)):
            for x in range(len(map_data[y])):
                libtcod.map_set_properties(self.map, x, y,
                                           map_data[y][x].isVisible,
                                           map_data[y][x].isWalkable)

    def update_fov(self, x, y):
        libtcod.console_clear(self.console)
        libtcod.console_set_default_foreground(self.console, libtcod.black)
        libtcod.map_compute_fov(self.map, x, y, 0)

    def checkWalkable(self, x, y):
        return libtcod.map_is_walkable(self.map, x, y)

    def checkOnStep(self, x, y):
        return self.map_data[y][x].onStep

    def draw_map(self):
        (x_size, y_size) = self.map_size
        for y in range(y_size):
            for x in range(x_size):
                if self.map_data[y][x].text != ' ':
                    self.draw_tile(x, y)
                visible = libtcod.map_is_in_fov(self.map, x, y)
                wasSeen = self.map_data[y][x].wasSeen

                if visible:
                    if not wasSeen:
                        self.map_data[y][x].wasSeen = True
                    libtcod.console_set_char_background(self.console, x, y,
                                                        self.map_data[y][x].color_light,
                                                        libtcod.BKGND_SET)
                else:
                    if wasSeen:
                        libtcod.console_set_char_background(self.console, x, y,
                                                            self.map_data[y][x].color_dark,
                                                            libtcod.BKGND_SET)

    def draw_tile(self, x, y):
        libtcod.console_put_char(self.console, x, y,
                                 self.map_data[y][x].text,
                                 libtcod.BKGND_NONE)

    def changeWalkable(self, obj, walkable):
        (x, y) = self.objects[obj]
        self.map_data[y][x].isWalkable = walkable
        self.load_map(self.map_data)

    def changeVisible(self, obj, visible):
        (x, y) = self.objects[obj]
        self.map_data[y][x].isVisible = visible
        self.load_map(self.map_data)

    def changeText(self, obj, txt):
        (x, y) = self.objects[obj]
        self.map_data[y][x].text = txt
        self.load_map(self.map_data)

    def convert_crude(self, smap, debug=False):
        fov_dark_wall = libtcod.Color(0, 0, 100)
        fov_light_wall = libtcod.Color(130, 110, 50)
        fov_dark_ground = libtcod.Color(50, 50, 150)
        fov_light_ground = libtcod.Color(200, 180, 50)

        map_data = []
        for y in range(len(smap)):
            collector = []
            for x in range(len(smap[y])):
                walkable = False
                visible = False
                text = ' '
                color_dark = fov_dark_wall
                color_light = fov_light_wall
                onStep = False
                if smap[y][x] == ' ':
                    walkable = True
                    visible = True
                    color_dark = fov_dark_ground
                    color_light = fov_light_ground
                elif smap[y][x] == 'B':
                    walkable = True
                    visible = False
                    color_dark = fov_dark_ground
                    color_light = fov_light_ground
                    text = 'B'
                elif smap[y][x] == '=':
                    visible = True
                    color_dark = fov_dark_ground
                    color_light = fov_light_ground
                    text = libtcod.CHAR_DHLINE
                    self.objects["door1"] = (x, y)
                elif smap[y][x] == 'i':
                    visible = True
                    walkable = True
                    color_dark = fov_dark_ground
                    color_light = fov_light_ground
                    text = 'i'
                    onStep = slip
                elif smap[y][x] == 't':
                    visible = True
                    walkable = True
                    color_dark = fov_dark_ground
                    color_light = fov_light_ground
                    text = 't'
                    onStep = trigger
                elif smap[y][x] == 's':
                    visible = True
                    walkable = True
                    color_dark = fov_dark_ground
                    color_light = fov_light_ground
                    text = 't'
                    onStep = gennewmap 
                currentTile = Tile.Tile(
                    walkable, visible, text, color_light, color_dark, onStep, debug)
                collector.append(currentTile)
            map_data.append(collector)
            self.load_map(map_data)

def gennewmap():
    pass 

def slip(x1, y1, x2, y2):
    return (x1 + (x2 - x1) * 2, y1 + (y2 - y1) * 2)


def trigger(obj, map):
    map.changeWalkable(obj, True)
    map.changeText(obj, ' ')
