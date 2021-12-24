import pygame
import os
import sys
import pytmx
import menu
from constants import *

all_entities = pygame.sprite.Group()
borders = pygame.sprite.Group()


# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class BorderTile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(borders)
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)


class Map:
    def __init__(self, filename, free_tiles):
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.add_borders()

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, layer=0)
                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer=0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def add_borders(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_free((x, y)):
                    BorderTile((x * TILE_SIZE, y * TILE_SIZE))


class Hero(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        super().__init__(all_entities)
        self.x, self.y = position
        self.image = pygame.transform.scale(load_image(PLAYER_IMAGE), (63, 63))
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.speed = speed
        self.xvel, self.yvel = 0, 0

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, map):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.yvel = -self.speed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.yvel = self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            self.xvel = -self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.xvel = self.speed
        if not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
            self.yvel = 0
        if not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]):
            self.xvel = 0

        if self.collide_x():
            self.rect.x += self.xvel
        if self.collide_y():
            self.rect.y += self.yvel

    def collide_x(self):
        for border in borders:
            if pygame.Rect(self.rect.x + self.xvel + 2, self.rect.y + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True

    def collide_y(self):
        for border in borders:
            if pygame.Rect(self.rect.x + 2, self.rect.y + self.yvel + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True


class Game:
    def __init__(self, map, hero):
        self.map = map
        self.hero = hero

    def render(self, screen):
        self.map.render(screen)
        all_entities.draw(screen)


def main():
    """
            Инициализация переменных
    """
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    menu.Menu('background_menu.png', screen, load_image, clock)

    hero = Hero((WIDTH // 2, HEIGHT // 2), speed=6)
    map = Map('map1.tmx', [34, 6, 7, 8, 14, 15, 16, 22, 23, 24, 30])
    game = Game(map, hero)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        all_entities.update(map)
        screen.fill('black')
        game.render(screen)
        all_entities.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


main()
