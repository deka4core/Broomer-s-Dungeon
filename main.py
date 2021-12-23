import pygame
import os
import sys
import pytmx
import menu
from constants import *


# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Map:

    def __init__(self, filename, free_tiles):
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, layer=0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer=0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


def main():
    """
            Инициализация переменных
    """
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    menu.Menu('background_menu.png', screen, load_image, clock)

    Map('map.tmx', [30, 46])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                pass
        screen.fill('black')
        pygame.display.flip()  # смена кадра
        clock.tick(FPS)  # установление ограничения кадров


main()
