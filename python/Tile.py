class Tile:

    def __init__(self, isWalkable, isVisible, text, color_light, color_dark, onStep=False, wasSeen=False):
        self.isWalkable = isWalkable
        self.isVisible = isVisible
        self.wasSeen = wasSeen
        self.text = text
        self.color_light = color_light
        self.color_dark = color_dark
        self.onStep = onStep
        self.properties = {}
