"""
    Файл с камерой
"""
from menu import pygame
from map_generator import spawned_rooms
from constants import WIDTH, HEIGHT
import static_func


class Camera(object):
    """
        Объект камеры
    """

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    # Передвинуть объекты относительно камеры
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    # Обновить положение камеры
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


# настройка слежения камеры
def camera_configure(camera, target_rect) -> pygame.Rect:
    left, top = target_rect[0], target_rect[1]
    width, height = camera[-2], camera[-1]
    left, top = -left + WIDTH / 2, -top + HEIGHT / 2

    left = min(-minimal_w + WIDTH / 4, left)  # Не движемся дальше левой границы
    left = max(-maximal_w + WIDTH / 4, left)  # Не движемся дальше правой границы
    top = min(-minimal_h + HEIGHT / 4, top)  # Не движемся дальше нижней границы
    top = max(-maximal_h + HEIGHT / 4, top)  # Не движемся дальше верхней границы

    return pygame.Rect(left, top, width, height)


# Находим необходимые для конфигурации камеры значения
minimal_w = static_func.get_minimal_width(spawned_rooms)
minimal_h = static_func.get_minimal_height(spawned_rooms)
maximal_h = static_func.get_maximal_height(spawned_rooms)
maximal_w = static_func.get_maximal_width(spawned_rooms)
