"""! @brief Файл Графического Пользовательского Интерфейса"""
##
# @file gui.py
#
# @brief Файл Графического Пользовательского Интерфейса
#
# @section description_chest Описание
# Классы HUD, кнопок, GUI
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import pygame
from constants import WIDTH, HEIGHT
from mixer import button_sound
from static_func import load_image

gui_sprites = pygame.sprite.Group()
hit_marks = []


class Hit(pygame.sprite.Sprite):
    """Класс отображения нанесенного урона

    При нанесении урона на экране отображается кол-во нанесенного урона."""

    def __init__(self, damage: int, coords: tuple, color: str):
        """Инициализация"""
        super().__init__(gui_sprites)
        self.damage = damage
        self.x, self.y = coords
        self.timer = 0
        self.font = pygame.font.SysFont('arialblack.ttf', 32)
        hit_marks.append(self)
        self.arr = hit_marks
        self.show(color)

    def show(self, color):
        """Отображение хитмаркера"""
        self.image = self.font.render(str(self.damage), True, color)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def destruct(self):
        """Деструктор по таймеру"""
        if self.timer > 500:
            del self.arr[self.arr.index(self)]
            self.kill()

    def do_timer(self, clock: pygame.time.Clock):
        """Обновление таймера"""
        self.timer += clock.get_time()
        self.move()
        self.destruct()

    def move(self):
        """Передвижение хитмаркера"""
        self.rect.y -= 0.05


class Title(pygame.sprite.Sprite):
    """Класс заголовка

    Всплывает над игроком при зачистке меню на определенное время."""

    def __init__(self, titles_list: list):
        """Инициализация"""
        super().__init__(gui_sprites)
        self.timer = 0
        self.font = pygame.font.SysFont('arialblack.ttf', 72)
        titles_list.append(self)
        self.show()

    def show(self):
        """Отображение заголовка"""
        self.image = self.font.render('Комната зачищена', True, 'gold')
        self.rect = self.image.get_rect().move(WIDTH // 2 - self.image.get_width() // 2,
                                               HEIGHT // 2 - self.image.get_height())

    def destruct(self, arr: list):
        """Деструктор по таймеру"""
        if self.timer > 1000:
            del arr[arr.index(self)]
            self.kill()

    def do_timer(self, clock: pygame.time.Clock, arr: list):
        """Обновление таймера"""
        self.timer += clock.get_time()
        self.show()
        self.destruct(arr)


class HealthBar:
    """Класс полоски ХП

    Находится в левом верхнем углу. Отображает количество оставшихся очков здоровья с помощью слайдера."""

    def __init__(self, screen, hero):
        """Инициализация"""
        self.health_points = hero.health_points
        self.screen = screen
        self.image = pygame.transform.scale(load_image('gui/health_bar.png'), (236, 24))
        self.show()

    def show(self):
        """Метод отображения полоски"""
        pygame.draw.rect(self.screen, (0, 128, 0), (32, 31, 200, 20))
        pygame.draw.rect(self.screen, (255, 0, 0), (32, 31, self.health_points * 2, 20))
        self.screen.blit(self.image, (28, 30))

    def update(self, health_points):
        """Обновление значения полоски"""
        self.health_points = health_points
        self.show()


class CoinsBar:
    """Класс счетчика монет

    Отображается в левом верхнем углу под HealthBar. Показывает кол-во монет в текущем раунде данжа."""

    def __init__(self, screen, hero, font):
        """Инициализация"""
        self.coins = hero.coins
        self.screen = screen
        self.font = font
        self.show()

    def show(self):
        """Метод отображения"""
        image = self.font.render(f'Coins: {self.coins}', True, pygame.Color("gold"))
        self.screen.blit(image, (28, 60))

    def update(self, coins):
        """Обновление значения счетчика монет"""
        self.coins = coins
        self.show()


class Button:
    """Класс кнопки"""

    def __init__(self, screen, width, height, inactive_color, active_color, color_text=(255, 255, 255),
                 border_radius=0):
        """Инициализация"""
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.screen = screen
        self.color_text = color_text
        self.border_radius = border_radius

    def draw(self, x, y, message, action=None):
        """Отрисовка прямоугольника кнопки"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Курсор НА / НЕ НА кнопке
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height),
                             border_radius=self.border_radius)
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.width, self.height),
                             border_radius=self.border_radius)
        self.draw_text(x, y, message=message,
                       color=self.color_text)

    def draw_text(self, x, y, message, color, font=None):
        """Отрисовка текста на кнопке

        Вычисление оптимальных размеров текста на кнопке и её отрисовка"""
        font_size = self.width // len(message) if self.width // len(message) > 30 else 30
        font_text = pygame.font.Font(font, font_size)
        text = font_text.render(message, True, color)
        text_w = text.get_width()
        text_h = text.get_height()
        self.screen.blit(text, (x + self.width // 2 - text_w // 2, y + self.height // 2 - text_h // 2))


class PressToStartTitle:
    """Анимированное фото: Нажмите, чтобы продолжить """

    def __init__(self, screen):
        """Инициализация"""
        self.screen = screen
        self.images = [pygame.transform.scale(load_image(f'gui/press_to_start{i}.png'),
                                              (432, 48)) for i in range(1, 3)]
        self.count_image = 0

    def update(self):
        """Анимация при обновлении кадра"""
        self.count_image += 0.03
        if int(self.count_image) >= 2:
            self.count_image = 0
        self.screen.blit(self.images[int(self.count_image)],
                         (WIDTH - 450, HEIGHT - 80))
