"""! @brief Файл Лобби"""
##
# @file lobby.py
#
# @brief Файл лобби
#
# @section description_chest Описание
# Класс лобби и его игровой процесс
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
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
    """Класс Лобби"""
    def __init__(self, free_tiles, clock, screen):
        """Инициализация"""
        self.hero = Hero((WIDTH, HEIGHT), speed=HERO_SPEED, images_idle=PLAYER_IMAGES_IDLE,
                         images_run=PLAYER_IMAGES_RUN, size=(57, 64))
        self.free_tiles = free_tiles
        self.surface = screen
        self.started = False
        pygame.init()
        self.map_ = pytmx.load_pygame('data/maps/lobby_map2.tmx')
        camera = Camera(camera_configure, WIDTH, HEIGHT)
        self.run(clock, camera)

    def run(self, clock, camera):
        """Основной цикл

        Обновление положений, отрисовка, анимация, очистка мусора"""
        spaceb_title = PressToStartTitle(self.surface)  # сокрщ. от space bar
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

    def is_free(self, position: tuple, layer) -> bool:
        """Проверка на свободную клетку"""
        return self.map_.tiledgidmap[self.map_.get_tile_gid(*position, layer)] in self.free_tiles

    def draw_map(self):
        """Отрисовка карты"""
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
        """Деструктор"""
        for sprite in all_tiles:
            sprite.kill()

    def terminate(self):
        """Завершение процесса игры"""
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
