"""! @brief Основной файл проекта."""
##
# @mainpage Broomer's Dungeon
#
# @section description_project Описание проекта
#
# Классический RPG Rogue-Like инди-проект с видом сверху. Игрок
# проходит комнаты с разными врагами - Бомбер, Бегун, Стреляющий Монстр - и получает за успешное прохождение награды
# в виде монет. К каждому врагу нужно применять особую тактику. Например, от Бегуна стоит держаться подальше и
# стрелять по нему издалека. Если игрок находится в помещении, двери закрываются, это сделано для более интересного
# процесса, во избежание нечестной игры.
#
# Чтобы начать играть вы можете склонировать мой репозиторий и установить
# необходимые модули в requirements.txt введя команду в терминал: pip install -r requirements.txt (Если вы на OS
# Windows)
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
##
# @file main.py
#
# @brief Основной файл проекта
#
# @section description_main Описание
# Основной файл проекта с игровым циклом. Запускает все три этапа (Меню, Лобби, Подземелье)
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 23/12/2021.
# - Modified by dekacore on 13/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import pygame
from constants import SIZE, BACKGROUND_IMAGE
from dungeon import Dungeon
from lobby import Lobby
from menu import Menu
from results import Results
from static_func import load_image

# Инициализация нужных переменных
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


def main():
    """Основной цикл

    Открытие меню, лобби, данжа, результатов"""
    running = True
    while running:
        # Открытие меню
        Menu(BACKGROUND_IMAGE, screen, load_image, clock)
        # Открываем лобби
        Lobby([533, 534, 535, 536, 573, 574, 575, 576, 1207, 1208], clock, screen)
        # Открываем данж
        Dungeon(screen, clock)

        Results(screen, clock)


if __name__ == "__main__":
    main()
