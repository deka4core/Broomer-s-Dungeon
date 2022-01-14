"""! @brief Файл подземелья."""
##
# @file dungeon.py
#
# @brief Файл подземелья.
#
# @section description_chest Описание
# Содержит класс, осуществляющий игровой процесс в подземелье.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 13/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import sys
import pygame
from camera import camera_configure, Camera
from chest import chests, all_tiles, chests_sprites
from constants import TILE_SIZE, ROOM_SIZE, PLAYER_IMAGES_IDLE, PLAYER_IMAGES_RUN, HERO_SPEED, MONSTERS_NUMBER, SIZE, \
    WIDTH, FPS, BACKGROUND_COLOR, CURSOR_IMAGE
from entities import Hero, all_entities, splash_sprites, sand_bullet, titles
from gui import HealthBar, CoinsBar, hit_marks
from map_generator import Map
from monster_spawner import MonsterSpawner
from results import Database
from static_func import update_fps, load_image


class Dungeon:
    """Класс подземелья"""
    def __init__(self, screen, clock):
        """Инициализация параметров"""
        self.clock = clock
        self.screen = screen
        self.hero = Hero((int(TILE_SIZE * (3 * ROOM_SIZE[0] + ROOM_SIZE[0] // 2 - 1)),
                          int(TILE_SIZE * (3 * ROOM_SIZE[1] + ROOM_SIZE[1] // 2 - 1))), speed=HERO_SPEED,
                         images_idle=PLAYER_IMAGES_IDLE, images_run=PLAYER_IMAGES_RUN,
                         size=(45, 50))
        self.health_bar = HealthBar(self.screen, self.hero)
        self.map_ = Map([34, 6, 7, 8, 14, 15, 16, 22, 23, 24, 30], screen=self.screen)
        self.rooms = self.map_.generator.spawned_rooms
        self.camera = Camera(camera_configure, len(self.rooms[0]) * TILE_SIZE * 26,
                             len(self.rooms * TILE_SIZE * 26), self.rooms)
        self.monster_spawner = MonsterSpawner(MONSTERS_NUMBER, self.rooms)
        self.font = pygame.font.SysFont("Arial", 18)
        self.coins_bar = CoinsBar(self.screen, self.hero, self.font)
        self.alpha_value = 0  # альфа-канал затемнения
        self.death_bckg = pygame.Surface(SIZE)  # экран затемнения
        self.default_count_monsters = len(self.monster_spawner.monsters)
        self.start_time = pygame.time.get_ticks()
        self.start()

    def start(self):
        """Основной цикл"""
        # Эмбиент
        pygame.mixer.music.load('data/sounds/dungeon_ambient_1.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        # Различные флаги и переменные для отслеживания
        running = True
        pygame.mouse.set_visible(False)  # выключаем мышь
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.hero.shoot_splash(event, self.camera)
            self.update_all()
            self.draw_all()
            self.change_cursor()
            # Если герой умер
            if not self.hero.is_alive:
                if self.alpha_value < 250:
                    self.change_alpha_channel()
                else:
                    break
            elif len(self.monster_spawner.monsters) == 0:
                if self.alpha_value < 250:
                    self.change_alpha_channel()
                else:
                    break
            # ФПС
            self.screen.blit(update_fps(self.clock, self.font), (WIDTH - 100, 25))
            pygame.display.flip()
            self.clock.tick(FPS)
        self.destruct()

    def update_all(self):
        """Обновление всех положений"""
        self.hero.update_cooldown(self.clock)
        all_entities.update()
        self.camera.update(self.hero)
        self.map_.check_player_room(self.hero)
        for chest in chests:
            chest.update_hero(self.hero)
        for hit in hit_marks:
            hit.do_timer(clock=self.clock)
        for monster in self.monster_spawner.monsters:
            monster.update_enemy(arr=self.monster_spawner.monsters, arr_hit=hit_marks,
                                 hero=self.hero, clock=self.clock, rooms=self.rooms)
        for splash in splash_sprites:
            splash.move()
        for bullet in sand_bullet:
            bullet.move()
        for title in titles:
            title.do_timer(clock=self.clock, arr=titles)

    def draw_all(self):
        """Отрисовка разных слоев

        Слой 0: Задний фон
        Слой 1: Карта
        Слой 2: Объекты
        Слой 3: HUD"""
        # Слой 0
        self.screen.fill(BACKGROUND_COLOR)

        # Слой 1
        for tile in all_tiles:
            self.screen.blit(tile.image, self.camera.apply(tile))

        # Слой 2
        for chest in chests_sprites:
            self.screen.blit(chest.image, self.camera.apply(chest))
        self.screen.blit(self.hero.image, self.camera.apply(self.hero))
        for monster in self.monster_spawner.monsters:
            self.screen.blit(monster.image, self.camera.apply(monster))
        for splash in splash_sprites:
            self.screen.blit(splash.image, self.camera.apply(splash))
        for bullet in sand_bullet:
            self.screen.blit(bullet.image, self.camera.apply(bullet))

        # Слой 3
        for hit in hit_marks:
            self.screen.blit(hit.image, self.camera.apply(hit))
        for title in titles:
            self.screen.blit(title.image, (title.rect.x, title.rect.y))
        self.coins_bar.update(self.hero.coins)
        self.health_bar.update(self.hero.health_points)

    def change_cursor(self):
        """Смена курсора на более удобный прицел"""
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            self.screen.blit(load_image(CURSOR_IMAGE), pos)

    # Изменяем альфа-канал
    def change_alpha_channel(self):
        """Изменяем альфа канал

        Изменение альфа-канала на второй поверхности и дальнейшее её слитие с основным экраном"""
        self.alpha_value += 1
        self.death_bckg.set_alpha(self.alpha_value)
        self.screen.blit(self.death_bckg, (0, 0))

    def destruct(self):
        """Деструктор класса

        Удаление всех данных"""
        database = Database()
        alive = 1 if self.hero.is_alive else 0
        database.set_values(self.hero.coins, pygame.time.get_ticks() - self.start_time,
                            self.default_count_monsters - len(self.monster_spawner.monsters), alive)
        database.close_connection()
        pygame.mixer.music.stop()
        pygame.mouse.set_visible(True)
        for sprite in all_tiles:
            sprite.kill()
        for sprite in all_entities:
            sprite.kill()
        for sprite in chests_sprites:
            sprite.kill()

    def terminate(self):
        """Выход из приложения"""
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
