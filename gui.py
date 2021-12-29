from menu import pygame

gui_sprites = pygame.sprite.Group()


class Hit(pygame.sprite.Sprite):
    def __init__(self, damage: int, coords: tuple, arr: list):
        super().__init__(gui_sprites)
        self.damage = damage
        self.x, self.y = coords
        self.timer = 0
        arr.append(self)
        self.show()

    def show(self):
        font = pygame.font.SysFont('arialblack.ttf', 32)
        self.image = font.render(str(self.damage), True, self.get_color(self.damage))
        self.rect = self.image.get_rect().move(self.x, self.y)

    def destruct(self, arr: list):
        if self.timer > 500:
            del arr[arr.index(self)]
            self.kill()

    def get_color(self, damage: int) -> str:
        if damage < 50:
            return 'green'
        elif 50 <= damage <= 200:
            return 'yellow'
        elif damage > 200:
            return 'red'

    def do_timer(self, clock: pygame.time.Clock, arr: list):
        self.timer += clock.get_time()
        self.destruct(arr=arr)
