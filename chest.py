"""! @brief Файл сундука."""
##
# @file chest.py
#
# @brief Файл сундука
#
# @section description_chest Описание
# Файл сундука, открываемого игроком, при прохождении уровня. Содержит монеты.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 13/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import random
import pygame
from constants import CHEST_CLOSED_IMG, CHEST_OPENED_IMG
from mixer import coins_sounds
from static_func import load_image

chests_sprites = pygame.sprite.Group()
all_tiles = pygame.sprite.Group()
chests = []


class Chest(pygame.sprite.Sprite):
    """Класс сундука"""
    def __init__(self, pos):
        """Инициализация параметров"""
        super().__init__(chests_sprites)
        self.x, self.y = pos
        self.image = pygame.transform.scale(load_image(CHEST_CLOSED_IMG), (46, 46))
        x = random.randint(self.x + 5 * 46, self.x + 15 * 46)
        y = random.randint(self.y + 3 * 46, self.y + 7 * 46)
        self.rect = self.image.get_rect().move(x, y)
        self.opened = False
        self.already_gained = False
        self.coins = random.randint(20, 50)

    def update_hero(self, hero):
        """Проверка на коллизию с героем

        Проверка коллизии pygame.Rect.colliderect()"""
        if self.rect.colliderect(hero.rect):
            self.open_chest()
            if not self.already_gained:
                hero.coins += self.coins
                self.already_gained = True
                pygame.mixer.Sound.play(random.choice(coins_sounds))

    def open_chest(self):
        """Открытие сундука

        Сопровождается звуком и изменением изображения"""
        self.opened = True
        self.image = pygame.transform.scale(load_image(CHEST_OPENED_IMG), (46, 46))


def spawn_chest(pos):
    """Спавн сундука"""
    chest = Chest(pos)
    chests.append(chest)