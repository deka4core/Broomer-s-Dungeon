import random
from constants import *
import pygame
import pytmx

spawned_rooms = list()
all_sprites = pygame.sprite.Group()
all_entities = pygame.sprite.Group()  # группа всех живых объектов
borders = pygame.sprite.Group()  # группа границ
ROOM_MAPS = []
screen = pygame.display.set_mode(SIZE)


def start():
    global ROOM_MAPS, spawned_rooms
    ROOM_MAPS = [pytmx.load_pygame(f'{MAPS_DIR}/map{i}.tmx') for i in range(1, 4)]
    spawned_rooms = [[0] * MAP_MAX_WIDTH for i in range(MAP_MAX_HEIGHT)]
    newRoom = Room((20, 10), ROOM_MAPS[2])
    spawned_rooms[3][3] = (newRoom, 3 * TILE_SIZE * 20, 3 * TILE_SIZE * 10)

    for i in range(7):
        place_one_room()


def place_one_room():
    vacantPlaces = set()
    for x in range(len(spawned_rooms)):
        for y in range(len(spawned_rooms[0])):
            if spawned_rooms[x][y] == 0:
                continue

            max_x = len(spawned_rooms) - 1
            max_y = len(spawned_rooms[0]) - 1

            if x > 0 and spawned_rooms[x - 1][y] == 0:
                vacantPlaces.add((x - 1, y))
            if y > 0 and spawned_rooms[x][y - 1] == 0:
                vacantPlaces.add((x, y - 1))
            if x < max_x and spawned_rooms[x + 1][y] == 0:
                vacantPlaces.add((x + 1, y))
            if y < max_y and spawned_rooms[x][y + 1] == 0:
                vacantPlaces.add((x, y + 1))
    # newRoom = random.choice(ROOM_MAPS)
    newRoom = Room((20, 10), ROOM_MAPS[2])
    vacantPlaces = list(vacantPlaces)
    position = random.choice(vacantPlaces)
    room_x, room_y = position[0] * TILE_SIZE * 20, position[1] * TILE_SIZE * 10

    spawned_rooms[position[0]][position[1]] = (newRoom, room_x, room_y)


class Room:
    def __init__(self, size, map):
        self.x, self.y = size
        self.map = map
        self.DoorU = (8, 0, False)
        self.DoorR = (19, 3, False)
        self.DoorD = (8, 9, False)
        self.DoorL = (0, 3, False)


def connect_room(room, position):
    max_x = len(spawned_rooms) - 1
    max_y = len(spawned_rooms[0]) - 1
    room_x, room_y = position

    neighbours = list()

    if room.DoorU[-1] == False and room_y < max_y and spawned_rooms[room_x][room_y + 1][0].DoorD[-1] == False:
        neighbours.append(1)
    if room.DoorD[-1] == False and room_y > 0 and spawned_rooms[room_x][room_y - 1][0].DoorU[-1] == False:
        neighbours.append(2)
    if room.DoorR[-1] == False and room_x < max_x and spawned_rooms[room_x][room_y + 1][0].DoorL[-1] == False:
        neighbours.append(3)
    if room.DoorL[-1] == False and room_x > 0 and spawned_rooms[room_x][room_y - 1][0].DoorR[-1] == False:
        neighbours.append(4)

    select_direction = neighbours[random.randint(0, len(neighbours) - 1)]

    if select_direction == 1:
        room.DoorU[-1] = True
        spawned_rooms[room_x][room_y + 1][0].DoorD[-1] = True
    elif select_direction == 2:
        room.DoorD[-1] = True
        spawned_rooms[room_x][room_y + 1][0].DoorU[-1] = True
    elif select_direction == 4:
        room.DoorL[-1] = True
        spawned_rooms[room_x][room_y + 1][0].DoorR[-1] = True
    elif select_direction == 3:
        room.DoorR[-1] = True
        spawned_rooms[room_x][room_y + 1][0].DoorL[-1] = True



start()





class Tile(pygame.sprite.Sprite):
    """           Класс тайла                """

    def __init__(self, position, image):
        super().__init__(all_sprites)
        self.x, self.y = position
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)


class BorderTile(Tile):
    """    Класс тайла на который нельзя наступать       """

    def __init__(self, position, image):
        super().__init__(position, image)
        borders.add(self)


class Map:
    """                 Класс карты                       """

    def __init__(self, free_tiles):
        maps = spawned_rooms
        self.free_tiles = free_tiles
        self.add_borders(maps)

    # узнаем ID тайла из тайлсета
    def get_tile_id(self, position, map):
        return map.tiledgidmap[map.get_tile_gid(*position, layer=0)]

    def is_free(self, position, map):
        return self.get_tile_id(position, map) in self.free_tiles

    def add_borders(self, maps):
        for row in maps:
            for item in row:
                if item != 0:
                    map_class, map_x, map_y = item
                    dup, ddown, dleft, dright = map_class.DoorU, map_class.DoorD, map_class.DoorL, map_class.DoorR
                    print(dup, ddown, dleft, dright)
                    map = map_class.map
                    for y in range(map.height):
                        for x in range(map.width):
                            if (dup[-1] and x == dup[0] and y == dup[1]) or \
                                    (ddown[-1] and x == ddown[0] and y == ddown[1]) or \
                                    (dleft[-1] and x == dleft[0] and y == dleft[1]) or \
                                    (dright[-1] and x == dright[0] and y == dright[1]):
                                print(1)
                                image = map.get_tile_image_by_gid(34)
                            else:
                                image = map.get_tile_image(x, y, layer=0)

                            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                            if not self.is_free((x, y), map):
                                BorderTile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image)
                            else:
                                Tile((x * TILE_SIZE + map_x, y * TILE_SIZE + map_y), image)
