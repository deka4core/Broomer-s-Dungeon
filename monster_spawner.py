import random

from constants import TILE_SIZE, ROOM_SIZE, HERO_SPEED, MONSTER_CLASSIC_IMAGES_IDLE, MONSTER_CLASSIC_IMAGES_RUN, \
    MONSTER_SHOTTER_IMAGES, MONSTER_BOMBER_IDLE, MONSTER_SHOTTER_IMAGES_SHOOT
from entities import Enemy, ShootingEnemy, Bomber


class MonsterSpawner:
    def __init__(self, number, rooms):
        self.monsters = []
        self.spawn_monsters(number, rooms)

    def spawn_monsters(self, number, rooms):
        for row in rooms:
            for item in row:
                if item != -1:
                    if item != rooms[3][3]:
                        room, map_x, map_y = item
                        start_xy = (map_x + TILE_SIZE, map_y + TILE_SIZE)
                        end_xy = (map_x + ((ROOM_SIZE[0] - 8) * TILE_SIZE), map_y + ((ROOM_SIZE[1] - 7) * TILE_SIZE))
                        for i in range(number):
                            x = random.randint(start_xy[0], end_xy[0])
                            y = random.randint(start_xy[1], end_xy[1])
                            # rd_number = random.random()
                            # if rd_number >= 0.4:
                            #     enemy =
                            # elif rd_number > 0.6:
                            #     enemy = ShootingEnemy((x, y), speed=HERO_SPEED - 2,
                            #                           images=MONSTER_SHOTTER_IMAGES,
                            #                           room_index=(rooms.index(row), row.index(item)))
                            # elif rd_number:
                            # enemy = Bomber((x, y), speed=HERO_SPEED - 2,
                            #                     images=MONSTER_BOMBER_IDLE,
                            #                     room_index=(rooms.index(row), row.index(item)))
                            enemy = random.choice([Enemy((x, y), speed=HERO_SPEED - 2,
                                              images_idle=MONSTER_CLASSIC_IMAGES_IDLE,
                                              images_run=MONSTER_CLASSIC_IMAGES_RUN, room_index=(rooms.index(row),
                                                                                                 row.index(item))), ShootingEnemy((x, y), speed=HERO_SPEED - 2,
                                                      images_idle=MONSTER_SHOTTER_IMAGES, images_shoot=MONSTER_SHOTTER_IMAGES_SHOOT,
                                                      room_index=(rooms.index(row), row.index(item))), Bomber((x, y), speed=HERO_SPEED - 2,
                                                images=MONSTER_BOMBER_IDLE,
                                                room_index=(rooms.index(row), row.index(item)))])
                            room.mobs.append(enemy)
                            self.monsters.append(enemy)
