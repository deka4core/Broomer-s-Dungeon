import random

from map_generator import spawned_rooms
from constants import ROOM_SIZE, TILE_SIZE, MONSTER_SHOTTER_IMAGES, HERO_SPEED, MONSTER_CLASSIC_IMAGES
from entities import Enemy, ShootingEnemy


def spawn_monsters(number):
    for row in spawned_rooms:
        for item in row:
            if item != -1:
                if item != spawned_rooms[3][3]:
                    room, map_x, map_y = item
                    start_xy = (map_x + TILE_SIZE, map_y + TILE_SIZE)
                    end_xy = (map_x + ((ROOM_SIZE[0] - 8) * TILE_SIZE), map_y + ((ROOM_SIZE[1] - 7) * TILE_SIZE))
                    for i in range(number):
                        x = random.randint(start_xy[0], end_xy[0])
                        y = random.randint(start_xy[1], end_xy[1])
                        rd_number = random.random()
                        if rd_number > 0.4:
                            enemy = Enemy((x, y), speed=HERO_SPEED - 2,
                                          images=MONSTER_CLASSIC_IMAGES, room_index=(spawned_rooms.index(row),
                                                                                                    row.index(item)))
                        else:
                            enemy = ShootingEnemy((x, y), speed=HERO_SPEED - 2,
                                          images=MONSTER_SHOTTER_IMAGES, room_index=(spawned_rooms.index(row), row.index(item)))
                        room.mobs.append(enemy)
