"""! @brief Файл с функциями"""
##
# @file static_func.py
#
# @brief Файл с функциями
#
# @section description_chest Описание
# Функции используются меж классов, поэтому я создал для них отдельный файл.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St. All rights reserved.
import os
import sys

import pygame


def load_image(name: str) -> pygame.image:
    """Загрузка изображения"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


def get_minimal_width(rooms) -> int:
    """Выводит (X) координату самой левой комнаты

    Необходимо для расчетов размеров карты и конфигурации камеры."""
    min_w = 9999
    for i in rooms:
        for j in i:
            if j != -1:
                min_w = j[-2] if j[-2] < min_w else min_w
    return min_w


def get_maximal_width(rooms) -> int:
    """Выводит (X) координату самой правой комнаты

    Необходимо для расчетов размеров карты и конфигурации камеры."""
    max_w = 0
    for i in rooms:
        for j in i:
            if j != -1:
                max_w = j[-2] if j[-2] > max_w else max_w
    return max_w


def get_minimal_height(rooms) -> int:
    """Выводит (Y) координату самой верхней комнаты

    Необходимо для расчетов размеров карты и конфигурации камеры."""
    min_h = 9999
    for i in rooms:
        for j in i:
            if j != -1:
                min_h = j[-1] if j[-1] < min_h else min_h
    return min_h


def get_maximal_height(rooms) -> int:
    """Выводит (Y) координату самой нижней комнаты

    Необходимо для расчетов размеров карты и конфигурации камеры."""
    max_h = 0
    for i in rooms:
        for j in i:
            if j != -1:
                max_h = j[-1] if j[-1] > max_h else max_h
    return max_h


def more(x, y) -> bool:
    """Сравнение >"""
    return x > y


def less(x, y) -> bool:
    """Сравнение <"""
    return x < y


def update_fps(clock, font):
    """Счетчик ФПС

    Отображается в верхнем правом углу."""
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'FPS: {fps}', True, pygame.Color("white"))
    return fps_text
