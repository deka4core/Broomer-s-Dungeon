"""
    Файл с функциями
"""
import os
import sys

import pygame


# Загрузка изображения
def load_image(name) -> pygame.image:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


# Выводит (X) координату самой левой комнаты
def get_minimal_width(rooms) -> int:
    min_w = 9999
    for i in rooms:
        for j in i:
            if j != -1:
                min_w = j[-2] if j[-2] < min_w else min_w
    return min_w


# Выводит (X) координату самой правой комнаты
def get_maximal_width(rooms) -> int:
    max_w = 0
    for i in rooms:
        for j in i:
            if j != -1:
                max_w = j[-2] if j[-2] > max_w else max_w
    return max_w


# Выводит (Y) координату самой верхней комнаты
def get_minimal_height(rooms) -> int:
    min_h = 9999
    for i in rooms:
        for j in i:
            if j != -1:
                min_h = j[-1] if j[-1] < min_h else min_h
    return min_h


# Выводит (Y) координату самой нижней комнаты
def get_maximal_height(rooms) -> int:
    max_h = 0
    for i in rooms:
        for j in i:
            if j != -1:
                max_h = j[-1] if j[-1] > max_h else max_h
    return max_h


def more(x, y) -> bool:
    return x > y


def less(x, y) -> bool:
    return x < y


# FPS Counter
def update_fps(clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'FPS: {fps}', True, pygame.Color("white"))
    return fps_text
