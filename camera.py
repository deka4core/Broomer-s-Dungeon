"""! @brief Файл камеры."""
##
# @file camera.py
#
# @brief Файл камеры
#
# @section description_camera Описание
# Файл камеры, следящей за игроком. Камера блокируется в одном из направлений, достигнув границы игровой зоны.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 13/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import pygame
import static_func
from constants import WIDTH, HEIGHT


class Camera(object):
    """Объект камеры

    Камера, следящая за главным героем"""
    def __init__(self, camera_func, width, height, rooms=None):
        """Инициализация параметров"""
        self.rooms = rooms
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        """Передвинуть объекты относительно камеры

        Объекты смещаются относительно левого верхнего угла Rect камеры"""
        return target.rect.move(self.state.topleft)

    def update(self, target, sides_minmax=None):
        """Обновить положение камеры

        :param target: Hero
        :param sides_minmax: None
        :return: None
        """
        if sides_minmax is None:
            sides_minmax = [static_func.get_minimal_width(self.rooms),
                            static_func.get_minimal_height(self.rooms),
                            static_func.get_maximal_height(self.rooms),
                            static_func.get_maximal_width(self.rooms)]
        self.state = self.camera_func(self.state, target.rect, sides_minmax)


def camera_configure(camera, target_rect, sides_minmax) -> pygame.Rect:
    """Метод конфигурации камеры

    :param camera: Camera
    :param target_rect: pygame.Rect
    :param sides_minmax: list
    :return: pygame.Rect
    """
    left, top = target_rect[0], target_rect[1]
    width, height = camera[-2], camera[-1]
    left, top = -left + WIDTH / 2, -top + HEIGHT / 2

    left = min(-sides_minmax[0] + WIDTH / 4, left)  # Не движемся дальше левой границы
    left = max(-sides_minmax[-1] + WIDTH / 4, left)  # Не движемся дальше правой границы
    top = min(-sides_minmax[1] + HEIGHT / 4, top)  # Не движемся дальше нижней границы
    top = max(-sides_minmax[-2] + HEIGHT / 4, top)  # Не движемся дальше верхней границы

    return pygame.Rect(left, top, width, height)
