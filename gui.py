from menu import pygame
from constants import WIDTH, HEIGHT
from static_func import load_image

hit_sprites = pygame.sprite.Group()


class Hit(pygame.sprite.Sprite):
    def __init__(self, damage: int, coords: tuple, arr: list, color: str):
        super().__init__(hit_sprites)
        self.damage = damage
        self.x, self.y = coords
        self.timer = 0
        arr.append(self)
        self.show(color)

    def show(self, color):
        font = pygame.font.SysFont('arialblack.ttf', 32)
        self.image = font.render(str(self.damage), True, color)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def destruct(self, arr: list):
        if self.timer > 500:
            del arr[arr.index(self)]
            self.kill()

    def do_timer(self, clock: pygame.time.Clock, arr: list):
        self.timer += clock.get_time()
        self.move()
        self.destruct(arr=arr)

    def move(self):
        self.rect.y -= 0.05


class Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.show()

    def show(self):
        font = pygame.font.SysFont('arialblack.ttf', 72)
        self.image = font.render('Комната зачищена', True, 'gold')
        self.rect = self.image.get_rect().move(WIDTH // 2 - self.image.get_width() // 2,
                                               HEIGHT // 2 - self.image.get_height())

    def destruct(self, arr: list):
        if self.timer > 1000:
            del arr[arr.index(self)]
            self.kill()

    def do_timer(self, clock: pygame.time.Clock, arr: list):
        self.timer += clock.get_time()
        self.destruct(arr=arr)


class HealthBar:
    def __init__(self, screen, hero):
        self.health_points = hero.health_points
        self.screen = screen
        self.image = pygame.transform.scale(load_image('gui/health_bar.png'), (236, 24))
        self.show()

    def show(self):
        pygame.draw.rect(self.screen, (0, 128, 0), (32, 31, 200, 20))
        pygame.draw.rect(self.screen, (255, 0, 0), (32, 31, self.health_points * 2, 20))
        self.screen.blit(self.image, (28, 30))

    def update(self, health_points):
        self.health_points = health_points
        self.show()
