"""! @brief Файл спавнера мобов"""
##
# @file monster_spawner.py
#
# @brief Файл спавнера мобов
#
# @section description_chest Описание
# Класс спавнера мобов, распределяющий мобов по комнатам.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import random
from constants import TILE_SIZE, ROOM_SIZE, HERO_SPEED, MONSTER_CLASSIC_IMAGES_IDLE, MONSTER_CLASSIC_IMAGES_RUN, \
    MONSTER_SHOTTER_IMAGES, MONSTER_BOMBER_IDLE, MONSTER_SHOTTER_IMAGES_SHOOT
from entities import Enemy, ShootingEnemy, Bomber


class MonsterSpawner:
    """Класс спавнера мобов

    Распределяет мобов по комнатам случайным образом."""
    def __init__(self, number, rooms):
        """Инициализация"""
        self.monsters = []
        self.spawn_monsters(number, rooms)

    def spawn_monsters(self, number, rooms):
        """Спавн монстров

        Рандомно выбираем 5 монстров и закидываем их в комнату"""
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
