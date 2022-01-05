import sys

import pygame

import mixer
from constants import WIDTH, HEIGHT, LOGO_NAME, FPS
from gui import Button


class Menu:
    """                 Класс окна главного меню                                   """
    def __init__(self, background_name, screen, load_image, clock):
        self.screen = screen
        self.bckg_img = pygame.transform.scale(load_image(background_name), (WIDTH, HEIGHT))
        self.logo = pygame.transform.scale(load_image(LOGO_NAME), (824, 199))
        self.is_started = False
        self.menu_buttons = []
        self.clock = clock
        self.run()

    # При запуске
    def run(self):

        # Инициализация кнопок
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

    # Метод отрисовки
    def draw(self):
        self.screen.blit(self.bckg_img, (0, 0))
        self.screen.blit(self.logo, (WIDTH // 2 - 400, HEIGHT // 2 - 400))
        for button in self.menu_buttons:
            button[0].draw(*button[1])
        pygame.display.flip()
        self.clock.tick(FPS)

    # Начать игру
    def start_game(self):
        self.is_started = True

    # Покинуть игру
    def terminate(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
