from menu import pygame

gui_sprites = pygame.sprite.Group()


class Hit(pygame.sprite.Sprite):
    def __init__(self, damage: int, coords: tuple, arr: list, color: str):
        super().__init__(gui_sprites)
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
        self.destruct(arr=arr)
