from map_generator import *
from constants import *


class sEdge:
    sx, sy = 0, 0  # коорды начала
    ex, ey = 0, 0  # коорды конца


class sCell:
    edge_id = [0] * 4


NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

WORLD = {}


class ShadowCasting2D:
    def __init__(self, size):
        self.minimal_w, self.minimal_h, self.maximal_w, self.maximal_h = size
        self.maximal_w += TILE_SIZE * ROOM_SIZE[0]
        self.maximal_h += TILE_SIZE * ROOM_SIZE[1]

    def convert_to_polymap(self):
        SIDES = []
        for x in range(self.minimal_w, self.maximal_w, TILE_SIZE):
            for y in range(self.minimal_h, self.maximal_h, TILE_SIZE):
                if (x, y) in BORDER_TILES:

                    if (x - TILE_SIZE, y) not in BORDER_TILES:
                        if (x, y - TILE_SIZE) in BORDER_TILES:
                            for item in SIDES:
                                if (item.ex, item.ey) == (x, y):
                                    item.ex, item.ey = x, y + TILE_SIZE
                        else:
                            side = sEdge
                            side.sx, side.sy = x, y
                            side.ex, side.ey = x, y + TILE_SIZE
                            SIDES.append(side)

                    if (x + TILE_SIZE, y) not in BORDER_TILES:
                        if (x, y - TILE_SIZE) in BORDER_TILES:
                            for item in SIDES:
                                if (item.ex, item.ey) == (x + TILE_SIZE, y):
                                    item.ex, item.ey = x + TILE_SIZE, y + TILE_SIZE
                        else:
                            side = sEdge
                            side.sx, side.sy = x + TILE_SIZE, y
                            side.ex, side.ey = x + TILE_SIZE, y + TILE_SIZE
                            SIDES.append(side)

                    if (x, y - TILE_SIZE) not in BORDER_TILES:
                        if (x - TILE_SIZE, y) in BORDER_TILES:
                            for item in SIDES:
                                if (item.ex, item.ey) == (x, y):
                                    item.ex, item.ey = x + TILE_SIZE, y
                        else:
                            side = sEdge
                            side.sx, side.sy = x, y
                            side.ex, side.ey = x + TILE_SIZE, y
                            SIDES.append(side)

                    if (x, y + TILE_SIZE) not in BORDER_TILES:
                        if (x - TILE_SIZE, y) in BORDER_TILES:
                            for item in SIDES:
                                if (item.ex, item.ey) == (x, y + TILE_SIZE):
                                    item.ex, item.ey = x + TILE_SIZE, y + TILE_SIZE
                        else:
                            side = sEdge
                            side.sx, side.sy = x, y + TILE_SIZE
                            side.ex, side.ey = x + TILE_SIZE, y + TILE_SIZE
                            SIDES.append(side)
        return SIDES



