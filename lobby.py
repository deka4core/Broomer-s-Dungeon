import sys

import pygame
import pytmx

from camera import Camera, camera_configure
from chest import all_tiles
from constants import WIDTH, HEIGHT, HERO_SPEED, PLAYER_IMAGES_IDLE, PLAYER_IMAGES_RUN, FPS, TILE_SIZE
from entities import Hero, all_entities
from gui import PressToStartTitle
from map_generator import default_tiles, borders, BorderTile, Tile


class Lobby:
    """                              Класс Лобби                                              """
    def __init__(self, free_tiles, clock, screen):
        self.hero = Hero((WIDTH, HEIGHT), speed=HERO_SPEED, images_idle=PLAYER_IMAGES_IDLE,
                         images_run=PLAYER_IMAGES_RUN, size=(57, 64))
        self.free_tiles = free_tiles
        self.surface = screen
        self.started = False
        pygame.init()
        self.map_ = pytmx.load_pygame('data/maps/lobby_map2.tmx')
        camera = Camera(camera_configure, WIDTH, HEIGHT)
        self.run(clock, camera)

    # Основной цикл
    def run(self, clock, camera):

        spaceb_title = PressToStartTitle(self.surface)

        self.draw_map()
        pygame.mouse.set_visible(False)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.started = True

            # Обновление положений
            camera.update(self.hero, sides_minmax=[0, 0, HEIGHT, WIDTH])
            all_entities.update()

            # Отрисовка
            self.surface.fill((104, 144, 35))
            for e in all_tiles:
                self.surface.blit(e.image, camera.apply(e))
            self.surface.blit(self.hero.image, camera.apply(self.hero))

            # Анимация кнопки SPACE
            spaceb_title.update()

            # Очистка всех данных при начале игры
            if self.started:
                break

            pygame.display.flip()
            clock.tick(FPS)
        self.destruct()

    # Проверка на свободную клетку
    def is_free(self, position, layer) -> bool:
        return self.map_.tiledgidmap[self.map_.get_tile_gid(*position, layer)] in self.free_tiles

    # Отрисовка карты
    def draw_map(self):
        for sprite in default_tiles:
            sprite.kill()
        for sprite in borders:
            sprite.kill()
        for y in range(self.map_.height):
            for x in range(self.map_.width):
                for i in range(0, 3):
                    image = self.map_.get_tile_image(x, y, layer=i)
                    if image:
                        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                        if not self.is_free((x, y), i):
                            BorderTile((x * TILE_SIZE, y * TILE_SIZE), image, borders)
                        else:
                            Tile((x * TILE_SIZE, y * TILE_SIZE), image, default_tiles)

    def destruct(self):
        for sprite in all_tiles:
            sprite.kill()

    # Завершение процесса (Деструктор класса)
    def terminate(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
