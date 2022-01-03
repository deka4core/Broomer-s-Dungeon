import random

import pygame
from constants import CHEST_CLOSED_IMG, CHEST_OPENED_IMG
from mixer import coins_sounds
from static_func import load_image

chests_sprites = pygame.sprite.Group()
chests = []


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(chests_sprites)
        self.x, self.y = pos
        self.image = pygame.transform.scale(load_image(CHEST_CLOSED_IMG), (46, 46))
        x = random.randint(self.x + 5 * 46, self.x + 15 * 46)
        y = random.randint(self.y + 3 * 46, self.y + 7 * 46)
        self.rect = self.image.get_rect().move(x, y)
        self.opened = False
        self.already_gained = False
        self.coins = random.randint(20, 50)

    def update_hero(self, hero):
        if self.rect.colliderect(hero.rect):
            self.open_chest()
            if not self.already_gained:
                hero.coins += self.coins
                self.already_gained = True
                pygame.mixer.Sound.play(random.choice(coins_sounds))

    def open_chest(self):
        self.opened = True
        self.image = pygame.transform.scale(load_image(CHEST_OPENED_IMG), (46, 46))


def spawn_chest(pos):
    chest = Chest(pos)
    chests.append(chest)