import random

import pygame

from static_func import *
import pytmx

all_sprites = pygame.sprite.Group()  # группа всех спрайтов
borders = pygame.sprite.Group()  # группа границ
door_borders = pygame.sprite.Group()  # двери в переходах
door_tiles = pygame.sprite.Group()  # Пол в переходах
default_tiles = pygame.sprite.Group()  # все другие свободные тайлы

spawned_rooms = list()  # список установленных комнат
ROOM_MAPS = []  # список карт всех комнат

screen = pygame.display.set_mode(SIZE)  # экран


# Строит проход между двумя комнатами
def build_passage_to(position, map_position, door, map):
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


# При запуске
def start():
    global ROOM_MAPS, spawned_rooms
    ROOM_MAPS = [pytmx.load_pygame(f'{MAPS_DIR}/map{i}.tmx') for i in range(1, 4)]
    spawned_rooms = [[-1] * MAP_MAX_WIDTH for i in range(MAP_MAX_HEIGHT)]

    # Создаем начальную комнату
    new_room = Room(ROOM_SIZE, ROOM_MAPS[2])

    # Ставим начальную комнату в координаты (3, 3)
    spawned_rooms[3][3] = (new_room, 3 * TILE_SIZE * ROOM_SIZE[0], 3 * TILE_SIZE * ROOM_SIZE[1])

    # Добавляем определенное кол-во комнат
    for i in range(ROOM_NUMBER):
        place_one_room()

    # Соединяет все комнаты между собой
    for x in range(len(spawned_rooms)):
        for y in range(len(spawned_rooms[0])):
            if spawned_rooms[x][y] != -1:
                room = spawned_rooms[x][y][0]
                connect_room(room, (x, y))


# Генерация комнат
def place_one_room():
    vacantPlaces = set()  # Свободные места
    for x in range(len(spawned_rooms)):
        for y in range(len(spawned_rooms[0])):
            if spawned_rooms[x][y] == -1:
                continue

            max_x = len(spawned_rooms) - 1
            max_y = len(spawned_rooms[0]) - 1

            if x > 0 and spawned_rooms[x - 1][y] == -1:
                vacantPlaces.add((x - 1, y))
            if y > 0 and spawned_rooms[x][y - 1] == -1:
                vacantPlaces.add((x, y - 1))
            if x < max_x and spawned_rooms[x + 1][y] == -1:
                vacantPlaces.add((x + 1, y))
            if y < max_y and spawned_rooms[x][y + 1] == -1:
                vacantPlaces.add((x, y + 1))

    # Выбираем случайную комнату и конвертируем координаты в настоящие
    newRoom = Room(ROOM_SIZE, ROOM_MAPS[2])
    vacantPlaces = list(vacantPlaces)
    position = random.choice(vacantPlaces)
    width, height = ROOM_SIZE
    room_x, room_y = position[0] * TILE_SIZE * width, position[1] * TILE_SIZE * height
    # Выставляем комнату на её место в списке
    spawned_rooms[position[0]][position[1]] = (newRoom, room_x, room_y)


# соединить комнаты проходом
def connect_room(room, position):
    # макс.индекс комнаты по X и Y
    max_x = len(spawned_rooms) - 1
    max_y = len(spawned_rooms[0]) - 1
    room_x, room_y = position

    neighbours = list()  # список всех возможных дверей (1-DOWN_UP, 2-UP_DOWN, 3-RIGHT_LEFT, 4-LEFT_RIGHT)

    DOWN_UP, UP_DOWN, RIGHT_LEFT, LEFT_RIGHT = 1, 2, 3, 4

    # Добавление всех возможных проходов
    if not room.DoorD.is_open() and less(room_y, max_y) and check_room(room_x, room_y + 1, spawned_rooms) and \
            not room_at(room_x, room_y + 1, spawned_rooms).DoorU.is_open():
        neighbours.append(DOWN_UP)
    if not room.DoorU.is_open() and more(room_y, 0) and check_room(room_x, room_y - 1, spawned_rooms) and \
            not room_at(room_x, room_y - 1, spawned_rooms).DoorD.is_open():
        neighbours.append(UP_DOWN)
    if not room.DoorR.is_open() and less(room_x, max_x) and check_room(room_x + 1, room_y, spawned_rooms) and \
            not room_at(room_x + 1, room_y, spawned_rooms).DoorL.is_open():
        neighbours.append(RIGHT_LEFT)
    if not room.DoorL.is_open() and more(room_x, 0) and check_room(room_x - 1, room_y, spawned_rooms) and \
            not room_at(room_x - 1, room_y, spawned_rooms).DoorR.is_open():
        neighbours.append(LEFT_RIGHT)

    # Применение изменений
    if neighbours:
        for select_direction in neighbours:
            if select_direction == DOWN_UP:
                room.DoorD.open_state()
                if check_room(room_x, room_y + 1, spawned_rooms):
                    room_at(room_x, room_y + 1, spawned_rooms).DoorU.open_state()
            elif select_direction == UP_DOWN:
                room.DoorU.open_state()
                if check_room(room_x, room_y - 1, spawned_rooms):
                    room_at(room_x, room_y - 1, spawned_rooms).DoorD.open_state()
            elif select_direction == RIGHT_LEFT:
                room.DoorR.open_state()
                if check_room(room_x + 1, room_y, spawned_rooms):
                    room_at(room_x + 1, room_y, spawned_rooms).DoorL.open_state()
            elif select_direction == LEFT_RIGHT:
                room.DoorL.open_state()
                if check_room(room_x - 1, room_y, spawned_rooms):
                    room_at(room_x - 1, room_y, spawned_rooms).DoorR.open_state()


class Door:
    """            Класс двери            """
    def __init__(self, free_tiles_coords, not_free_tiles_coords, borders_tiles):
        self.f_tiles = free_tiles_coords
        self.nf_tiles = not_free_tiles_coords
        self.borders_tiles = borders_tiles

        self.opened = False
        self.already_done = False

    # Можно построить?
    def is_open(self) -> bool:
        return self.opened

    # Разрешить строительство
    def open_state(self) -> None:
        self.opened = True

    def close_state(self) -> None:
        self.opened = False

    # Построить проход
    def build_passage(self) -> None:
        self.already_done = not self.already_done

    # Уже построена?
    def is_builded(self) -> bool:
        return self.already_done


class Room:
    """            Класс комнаты            """
    def __init__(self, size, map):
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
        for door in self.Doors:
            if door.is_builded():
                door.close_state()

    def unblock(self):
        for door in self.Doors:
            if door.is_builded():
                door.open_state()

    def is_opened(self):
        return any([self.DoorU.is_open(), self.DoorD.is_open(), self.DoorR.is_open(), self.DoorL.is_open()])


class Tile(pygame.sprite.Sprite):
    """           Класс тайла                """
    def __init__(self, position, image, tile_group):
        super().__init__(all_sprites)
        self.x, self.y = position
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        tile_group.add(self)


class BorderTile(Tile):
    """    Класс тайла на который нельзя наступать       """
    def __init__(self, position, image, group_tile):
        super().__init__(position, image, group_tile)


class Map:
    """                 Класс карты                       """

    def __init__(self, free_tiles):
        maps = spawned_rooms
        self.free_tiles = free_tiles
        self.sort_tiles(maps)

    # узнаем ID тайла из тайлсета
    def get_tile_id(self, position, map_):
        return map_.tiledgidmap[map_.get_tile_gid(*position, layer=0)]

    # Можно ли наступать на клетку?
    def is_free(self, position, map_) -> bool:
        return self.get_tile_id(position, map_) in self.free_tiles

    # Сортировка тайлов и проходов
    def sort_tiles(self, maps: list):
        for border in borders:
            border.kill()
        for tile in default_tiles:
            tile.kill()
        for row in maps:
            for item in row:
                if item != -1:
                    map_class, map_x, map_y = item
                    dup, ddown, dleft, dright = map_class.DoorU, map_class.DoorD, map_class.DoorL, map_class.DoorR
                    map = map_class.map
                    for y in range(map.height):
                        for x in range(map.width):
                            if dup.is_open() and (x, y) in dup.f_tiles:
                                build_passage_to(position=(x, y), map_position=(map_x, map_y), door=dup, map=map)
                            elif ddown.is_open() and (x, y) in ddown.f_tiles:
                                build_passage_to(position=(x, y), map_position=(map_x, map_y), door=ddown, map=map)
                            elif dleft.is_open() and (x, y) in dleft.f_tiles:
                                build_passage_to(position=(x, y), map_position=(map_x, map_y), door=dleft, map=map)
                            elif dright.is_open() and (x, y) in dright.f_tiles:
                                build_passage_to(position=(x, y), map_position=(map_x, map_y), door=dright, map=map)
                            else:
                                image = map.get_tile_image(x, y, layer=0)
                                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                                if not self.is_free((x, y), map):
                                    BorderTile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image, borders)
                                else:
                                    Tile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image, default_tiles)


def check_player_room(player, map):
    for row in spawned_rooms:
        for item in row:
            if item != -1:
                room, room_x, room_y = item
                px, py = player.rect.x, player.rect.y
                if (room_x + TILE_SIZE < px < room_x + (ROOM_SIZE[0] - 6) * TILE_SIZE) and \
                        (room_y + TILE_SIZE < py < room_y + (ROOM_SIZE[1] - 6) * TILE_SIZE):
                    if room.have_monsters and room.is_opened():
                        room.block()
                        map.sort_tiles(spawned_rooms)
                    elif not room.have_monsters and not room.is_opened():
                        room.unblock()
                        map.sort_tiles(spawned_rooms)


start()
