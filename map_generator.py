"""! @brief Файл генератора карты"""
##
# @file map_generator.py
#
# @brief Файл генератора карты
#
# @section description_chest Описание
# Класс генератора карты, карты, дверей, комнат и всех типов тайлов.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 25/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import random
import pygame
import pytmx
from chest import all_tiles, spawn_chest
from constants import MAPS_DIR, MAP_MAX_WIDTH, MAP_MAX_HEIGHT, ROOM_SIZE, TILE_SIZE, ROOM_NUMBER
from static_func import less, more

borders = pygame.sprite.Group()  # группа границ
door_borders = pygame.sprite.Group()  # двери в переходах
door_tiles = pygame.sprite.Group()  # Пол в переходах
default_tiles = pygame.sprite.Group()  # все другие свободные тайлы


class MapGenerator:
    """Класс генератора карты

    Создание начальной комнаты и других, определение соседей, постройка необходимых проходов между ними."""
    def __init__(self, screen):
        """Инициализация"""
        self.spawned_rooms = []
        self.ROOM_MAPS = []  # список карт всех комнат
        self.screen = screen
        self.start()

    def start(self):
        """Происходит при запуске

        Создание начальной комнаты и пустой карты, её дальнейшее заполнение."""
        self.ROOM_MAPS = [pytmx.load_pygame(f'{MAPS_DIR}/map{i}.tmx') for i in range(1, 4)]
        self.spawned_rooms = [[-1] * MAP_MAX_WIDTH for i in range(MAP_MAX_HEIGHT)]

        # Создаем начальную комнату
        new_room = Room(ROOM_SIZE, self.ROOM_MAPS[2])
        new_room.have_monsters = False

        # Ставим начальную комнату в координаты (3, 3)
        self.spawned_rooms[3][3] = (new_room, 3 * TILE_SIZE * ROOM_SIZE[0], 3 * TILE_SIZE * ROOM_SIZE[1])

        # Добавляем определенное кол-во комнат
        for i in range(ROOM_NUMBER):
            self.place_one_room()

        # Соединяет все комнаты между собой
        for x in range(len(self.spawned_rooms)):
            for y in range(len(self.spawned_rooms[0])):
                if self.spawned_rooms[x][y] != -1:
                    room = self.spawned_rooms[x][y][0]
                    self.connect_room(room, (x, y))

    def build_passage_to(self, position, map_position, door, map):
        """Создает проход промеж двух соседей"""
        x, y = position
        map_x, map_y = map_position
        if not door.is_builded():
            for tile in door.nf_tiles:
                x1, y1 = tile
                image = map.get_tile_image(2, 2, layer=0)
                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                Tile((x1 * TILE_SIZE + map_x, map_y + (y1 * TILE_SIZE)), image, door_tiles)
            for tile in door.borders_tiles:
                image = map.get_tile_image(0, 0, layer=0)
                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                x1, y1 = tile
                BorderTile((x1 * TILE_SIZE + map_x, map_y + (y1 * TILE_SIZE)), image, door_borders)
            door.build_passage()
        image = map.get_tile_image(1, 1, layer=0)
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        Tile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image, default_tiles)

    def place_one_room(self):
        """Генерация комнат"""
        vacantPlaces = set()  # Свободные места
        for x in range(len(self.spawned_rooms)):
            for y in range(len(self.spawned_rooms[0])):
                if self.spawned_rooms[x][y] == -1:
                    continue

                max_x = len(self.spawned_rooms) - 1
                max_y = len(self.spawned_rooms[0]) - 1

                if x > 0 and self.spawned_rooms[x - 1][y] == -1:
                    vacantPlaces.add((x - 1, y))
                if y > 0 and self.spawned_rooms[x][y - 1] == -1:
                    vacantPlaces.add((x, y - 1))
                if x < max_x and self.spawned_rooms[x + 1][y] == -1:
                    vacantPlaces.add((x + 1, y))
                if y < max_y and self.spawned_rooms[x][y + 1] == -1:
                    vacantPlaces.add((x, y + 1))

        # Выбираем случайную комнату и конвертируем координаты в настоящие
        newRoom = Room(ROOM_SIZE, self.ROOM_MAPS[2])
        vacantPlaces = list(vacantPlaces)
        position = random.choice(vacantPlaces)
        width, height = ROOM_SIZE
        room_x, room_y = position[0] * TILE_SIZE * width, position[1] * TILE_SIZE * height
        # Выставляем комнату на её место в списке
        self.spawned_rooms[position[0]][position[1]] = (newRoom, room_x, room_y)

    def connect_room(self, room, position):
        """Разрешает постройку прохода между комнатами"""
        # макс.индекс комнаты по X и Y
        max_x = len(self.spawned_rooms) - 1
        max_y = len(self.spawned_rooms[0]) - 1
        room_x, room_y = position

        neighbours = list()  # список всех возможных дверей (1-DOWN_UP, 2-UP_DOWN, 3-RIGHT_LEFT, 4-LEFT_RIGHT)

        DOWN_UP, UP_DOWN, RIGHT_LEFT, LEFT_RIGHT = 1, 2, 3, 4

        # Добавление всех возможных проходов
        if not room.DoorD.is_open() and less(room_y, max_y) and self.check_room(room_x, room_y + 1) and \
                not self.room_at(room_x, room_y + 1).DoorU.is_open():
            neighbours.append(DOWN_UP)
        if not room.DoorU.is_open() and more(room_y, 0) and self.check_room(room_x, room_y - 1) and \
                not self.room_at(room_x, room_y - 1).DoorD.is_open():
            neighbours.append(UP_DOWN)
        if not room.DoorR.is_open() and less(room_x, max_x) and self.check_room(room_x + 1, room_y) and \
                not self.room_at(room_x + 1, room_y).DoorL.is_open():
            neighbours.append(RIGHT_LEFT)
        if not room.DoorL.is_open() and more(room_x, 0) and self.check_room(room_x - 1, room_y) and \
                not self.room_at(room_x - 1, room_y).DoorR.is_open():
            neighbours.append(LEFT_RIGHT)

        # Применение изменений
        if neighbours:
            for select_direction in neighbours:
                if select_direction == DOWN_UP:
                    room.DoorD.open_state()
                    if self.check_room(room_x, room_y + 1):
                        self.room_at(room_x, room_y + 1).DoorU.open_state()
                elif select_direction == UP_DOWN:
                    room.DoorU.open_state()
                    if self.check_room(room_x, room_y - 1):
                        self.room_at(room_x, room_y - 1).DoorD.open_state()
                elif select_direction == RIGHT_LEFT:
                    room.DoorR.open_state()
                    if self.check_room(room_x + 1, room_y):
                        self.room_at(room_x + 1, room_y).DoorL.open_state()
                elif select_direction == LEFT_RIGHT:
                    room.DoorL.open_state()
                    if self.check_room(room_x - 1, room_y):
                        self.room_at(room_x - 1, room_y).DoorR.open_state()

    def room_at(self, x, y):
        """Возвращает комнату из списка карты по её координатам"""
        return self.spawned_rooms[x][y][0]

    def check_room(self, x, y) -> bool:
        """Проверка на существование комнаты по координатам (x, y)"""
        return self.spawned_rooms[x][y] != -1


class Door:
    """Класс двери"""
    def __init__(self, free_tiles_coords, not_free_tiles_coords, borders_tiles):
        """Инициализация"""
        self.f_tiles = free_tiles_coords
        self.nf_tiles = not_free_tiles_coords
        self.borders_tiles = borders_tiles

        self.opened = False
        self.already_done = False

    def is_open(self) -> bool:
        """Можно построить?"""
        return self.opened

    def open_state(self) -> None:
        """Разрешить строительство"""
        self.opened = True

    def close_state(self) -> None:
        """Запретить строительство"""
        self.opened = False

    def build_passage(self) -> None:
        """Построить проход

        Изменяем переменную построенной двери"""
        self.already_done = not self.already_done

    def is_builded(self) -> bool:
        """Уже построена?"""
        return self.already_done


class Room:
    """Класс комнаты

    Имеет 4 двери"""
    def __init__(self, size, map):
        """Инициализация"""
        self.x, self.y = size
        self.map = map

        # Создаем возможность поставить двери в 4 стороны
        self.DoorU = Door([(8, 0), (9, 0)], [(8, -1), (9, -1), (8, -2), (9, -2)],
                          [(7, -1), (10, -1), (7, -2), (10, -2)])
        self.DoorD = Door([(8, 9), (9, 9)], [(8, 10), (9, 10), (8, 11), (9, 11)],
                          [(7, 10), (10, 10), (7, 11), (10, 11)])
        self.DoorR = Door([(19, 4), (19, 5)], [(20, 4), (20, 5), (21, 4), (21, 5)],
                          [(20, 3), (20, 6), (21, 3), (21, 6)])
        self.DoorL = Door([(0, 4), (0, 5)], [(-1, 4), (-1, 5), (-2, 4), (-2, 5)],
                          [(-1, 3), (-1, 6), (-2, 3), (-2, 6)])

        self.Doors = [self.DoorU, self.DoorD, self.DoorR, self.DoorL]

        # Есть ли монстры внутри комнаты?
        self.have_monsters = True
        self.mobs = []

    def block(self):
        """Блокировка дверей"""
        for door in self.Doors:
            if door.is_builded():
                door.close_state()

    def unblock(self):
        """Разблокировка дверей"""
        for door in self.Doors:
            if door.is_builded():
                door.open_state()

    def is_opened(self) -> bool:
        """Открыта ли комната?"""
        return any([self.DoorU.is_open(), self.DoorD.is_open(), self.DoorR.is_open(), self.DoorL.is_open()])


class Tile(pygame.sprite.Sprite):
    """Класс тайла

    По нему можно ходить."""
    def __init__(self, position, image, tile_group):
        """Инициализация

        Добавление в группы тайлов"""
        super().__init__(all_tiles)
        self.x, self.y = position
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        tile_group.add(self)


class BorderTile(Tile):
    """Класс тайла на который нельзя наступать"""
    def __init__(self, position, image, group_tile):
        super().__init__(position, image, group_tile)


class Map:
    """Класс карты"""
    def __init__(self, free_tiles, screen):
        """Инициализация"""
        self.generator = MapGenerator(screen)
        maps = self.generator.spawned_rooms
        self.free_tiles = free_tiles
        self.sort_tiles(maps)

    def get_tile_id(self, position, map_):
        """Получить ID тайла из Tileset'а"""
        return map_.tiledgidmap[map_.get_tile_gid(*position, layer=0)]

    def is_free(self, position, map_) -> bool:
        """Можно ли наступать на клетку?"""
        return self.get_tile_id(position, map_) in self.free_tiles

    def sort_tiles(self, maps: list):
        """Сортировка тайлов и проходов

        Очистка мусора, отрисовка новых тайлов"""
        for border in borders:
            border.kill()
        for tile in default_tiles:
            tile.kill()
        for row in maps:
            for item in row:
                if item != -1:
                    map_class, map_x, map_y = item
                    dup, ddown, dleft, dright = map_class.DoorU, map_class.DoorD, map_class.DoorL, map_class.DoorR
                    map_ = map_class.map
                    for y in range(map_.height):
                        for x in range(map_.width):
                            if dup.is_open() and (x, y) in dup.f_tiles:
                                self.generator.build_passage_to(position=(x, y), map_position=(map_x, map_y), door=dup, map=map_)
                            elif ddown.is_open() and (x, y) in ddown.f_tiles:
                                self.generator.build_passage_to(position=(x, y), map_position=(map_x, map_y), door=ddown, map=map_)
                            elif dleft.is_open() and (x, y) in dleft.f_tiles:
                                self.generator.build_passage_to(position=(x, y), map_position=(map_x, map_y), door=dleft, map=map_)
                            elif dright.is_open() and (x, y) in dright.f_tiles:
                                self.generator.build_passage_to(position=(x, y), map_position=(map_x, map_y), door=dright, map=map_)
                            else:
                                image = map_.get_tile_image(x, y, layer=0)
                                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                                if not self.is_free((x, y), map_):
                                    BorderTile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image, borders)
                                else:
                                    Tile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image, default_tiles)

    def check_player_room(self, player):
        """Есть ли игрок в комнате?"""
        rooms = self.generator.spawned_rooms
        for row in rooms:
            for item in row:
                if item != -1:
                    room, room_x, room_y = item
                    px, py = player.rect.x, player.rect.y
                    if (room_x + TILE_SIZE < px < room_x + (ROOM_SIZE[0] - 6) * TILE_SIZE) and \
                            (room_y + TILE_SIZE < py < room_y + (ROOM_SIZE[1] - 6) * TILE_SIZE):
                        if room.have_monsters and room.is_opened():
                            room.block()
                            self.sort_tiles(rooms)
                        elif not room.have_monsters and not room.is_opened():
                            room.unblock()
                            spawn_chest((room_x, room_y))
                            self.sort_tiles(rooms)

