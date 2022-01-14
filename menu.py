"""! @brief Файл главного меню."""
##
# @file menu.py
#
# @brief Файл главного меню
#
# @section description_doxygen_example Описание
# Файл главного меню с кнопками входа/выхода.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 23/12/2021.
# - Modified by dekacore on 13/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import sys
import pygame
import mixer
from constants import WIDTH, HEIGHT, LOGO_NAME, FPS
from gui import Button


class Menu:
    """Класс окна главного меню.

    """
    def __init__(self, background_name, screen, load_image, clock) -> None:
        """Инициализация параметров класса.

        """
        self.screen = screen
        self.bckg_img = pygame.transform.scale(load_image(background_name), (WIDTH, HEIGHT))
        self.logo = pygame.transform.scale(load_image(LOGO_NAME), (824, 199))
        self.is_started = False
        self.menu_buttons = []
        self.clock = clock
        self.run()

    def run(self) -> None:
        """Происходит при запуске.

        Основной цикл вместе с инициализацией графических модулей."""
        start_button = Button(self.screen, width=300, height=70, inactive_color=(60, 63, 65),
                              active_color=(43, 43, 43),
                              border_radius=5)
        exit_button = Button(self.screen, width=300, height=70, inactive_color=(60, 63, 65),
                             active_color=(43, 43, 43),
                             border_radius=5)
        self.menu_buttons.append((start_button, (WIDTH // 2 - 150, HEIGHT // 2 - 70, 'Начать игру',
                                                 self.start_game)))
        self.menu_buttons.append(
            (exit_button, (WIDTH // 2 - 150, HEIGHT // 2 + 70, 'Выйти из игры', self.terminate)))

        # Основной цикл
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.USEREVENT:
                    mixer.play_next_music()
            self.draw()

            # Выход из меню
            if self.is_started:
                self.screen.fill('black')
                break

    def draw(self) -> None:
        """Метод отрисовки каждого кадра."""
        self.screen.blit(self.bckg_img, (0, 0))
        self.screen.blit(self.logo, (WIDTH // 2 - 400, HEIGHT // 2 - 400))
        for button in self.menu_buttons:
            button[0].draw(*button[1])
        pygame.display.flip()
        self.clock.tick(FPS)

    def start_game(self) -> None:
        """Метод начала игры."""
        self.is_started = True

    def terminate(self) -> None:
        """Метод выхода из игры."""
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
