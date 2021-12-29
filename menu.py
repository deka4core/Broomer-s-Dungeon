import pygame
import sys

pygame.init()
from constants import *
from mixer import *

menu_buttons = []


class Menu:
    """
        Класс окна главного меню
    """

    def __init__(self, background_name, screen, load_image, clock):
        self.is_started = False
        self.bckg_img = pygame.transform.scale(load_image(background_name), (WIDTH, HEIGHT))
        self.logo = pygame.transform.scale(load_image(LOGO_NAME), (824, 199))
        self.on_start(screen, clock)

    """
        Инициализация кнопок и основной цикл с отрисовкой
    """

    def on_start(self, screen, clock):
        start_button = Button(screen, width=300, height=70, inactive_color=(60, 63, 65), active_color=(43, 43, 43),
                              border_radius=5)
        menu_buttons.append((start_button, (WIDTH // 2 - 150, HEIGHT // 2 - 70, 'Начать игру',
                                            self.start_game)))
        exit_button = Button(screen, width=300, height=70, inactive_color=(60, 63, 65), active_color=(43, 43, 43),
                             border_radius=5)
        menu_buttons.append((exit_button, (WIDTH // 2 - 150, HEIGHT // 2 + 70, 'Выйти из игры', self.terminate)))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.USEREVENT:
                    global CURRENT_MUSIC
                    play_next_music()
            screen.blit(self.bckg_img, (0, 0))
            screen.blit(self.logo, (WIDTH // 2 - 400, HEIGHT // 2 - 400))
            for button in menu_buttons:
                button[0].draw(*button[1])
            if self.is_started:
                break
            pygame.display.flip()
            clock.tick(FPS)

    """
        Начать игру
    """

    def start_game(self):
        self.is_started = True

    """
        Покинуть игру
    """

    def terminate(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()


class Button:
    """
        Класс кнопки
    """

    def __init__(self, screen, width, height, inactive_color, active_color, color_text=(255, 255, 255),
                 border_radius=0):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.screen = screen
        self.color_text = color_text
        self.border_radius = border_radius

    """
        Отрисовка прямоугольника кнопки
    """

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        """        курсор НЕ НА / НА кнопке         """
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:  # курсор на кнопке
            pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height),
                             border_radius=self.border_radius)
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:  # курсор не на кнопке
            pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.width, self.height),
                             border_radius=self.border_radius)
        font_size = self.width // len(message) if self.width // len(message) > 30 else 30  # вычисление размера шрифта
        # (изменить)
        self.draw_text(x, y, message=message, font_size=font_size if font_size < 70 else 70, margin=10,
                       color=self.color_text)

    """
        Отрисовка текста на кнопке
    """

    def draw_text(self, x, y, message, color, font=None, font_size=24, margin=10):
        font_text = pygame.font.Font(font, font_size)
        text = font_text.render(message, True, color)
        text_w = text.get_width()
        text_h = text.get_height()
        self.screen.blit(text, (x + self.width // 2 - text_w // 2, y + self.height // 2 - text_h // 2))
