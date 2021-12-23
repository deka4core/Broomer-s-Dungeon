import pygame
import os
import sys

import menu
from constants import *

"""
    Инициализация переменных
"""
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


MenuScreen = menu.Menu('background_menu.png', screen, load_image, clock)  # сцена с меню

"""
    Основной цикл
"""
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
