import random

from map_generator import spawned_rooms
from constants import ROOM_SIZE, TILE_SIZE, MONSTER_CLASSIC_IMAGES, HERO_SPEED
from entities import Enemy


def spawn_monsters(number):
    for row in spawned_rooms:
        for room in row:
            if room != -1:
                _, map_x, map_y = room
                start_xy = (map_x + TILE_SIZE, map_y + TILE_SIZE)
                end_xy = (map_x + ((ROOM_SIZE[0] - 8) * TILE_SIZE), map_y + ((ROOM_SIZE[1] - 7) * TILE_SIZE))
                for i in range(number):
                    x = random.randint(start_xy[0], end_xy[0])
                    y = random.randint(start_xy[1], end_xy[1])
                    Enemy((x, y), speed=HERO_SPEED - 2,
                                  images=MONSTER_CLASSIC_IMAGES, size=(45, 50))