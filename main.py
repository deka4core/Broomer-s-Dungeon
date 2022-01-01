import pygame

from constants import SIZE
from dungeon import Dungeon
from lobby import Lobby
from menu import Menu
from static_func import load_image

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


def main():
    running = True
    while running:
        # Открытие меню
        Menu('background_menu.png', screen, load_image, clock)
        # Открываем лобби
        Lobby([533, 534, 535, 536, 573, 574, 575, 576, 1207, 1208], clock, screen)
        # Открываем данж
        Dungeon(screen, clock)


if __name__ == "__main__":
    main()
