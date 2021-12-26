import os
import sys
import menu
from map_generator import *
from constants import *


# Загрузка изображения
def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# настройка слежения камеры
def camera_configure(camera, target_rect):
    left, top = target_rect[0], target_rect[1]
    width, height = camera[-2], camera[-1]
    left, top = -left + WIDTH / 2, -top + HEIGHT / 2

    left = min(0, left)  # Не движемся дальше левой границы
    left = max(-(camera.width - WIDTH), left)  # Не движемся дальше правой границы
    top = max(-(camera.height - HEIGHT), top)  # Не движемся дальше нижней границы
    top = min(0, top)  # Не движемся дальше верхней границы

    return pygame.Rect(left, top, width, height)


class Camera(object):
    """
        Объект камеры
    """
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    # Передвинуть объекты относительно камеры
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    # Обновить положение камеры
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Hero(pygame.sprite.Sprite):
    """
        Класс главного героя
    """
    def __init__(self, position, speed):
        super().__init__(all_entities)
        all_sprites.add(self)
        self.x, self.y = position
        self.image = pygame.transform.scale(load_image(PLAYER_IMAGE), (63, 63))
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.speed = speed
        self.xvel, self.yvel = 0, 0
        self.orientation_right = True

    # получить позицию
    def get_position(self):
        return self.x, self.y

    # сменить позицию на ...
    def set_position(self, position):
        self.x, self.y = position
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, map):
        # Проверка нажатых клавиш, изменение вектора направления
        if pygame.key.get_pressed()[pygame.K_w]:
            self.yvel = -self.speed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.yvel = self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            # поворот изображения в сторону ходьбы
            if not self.orientation_right:
                self.orientation_right = True
                self.image = pygame.transform.flip(self.image, True, False)
            self.xvel = -self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            # поворот изображения в сторону ходьбы
            if self.orientation_right:
                self.orientation_right = False
                self.image = pygame.transform.flip(self.image, True, False)
            self.xvel = self.speed

        # Сброс векторов направления, если ни одна клавиша не зажата
        if not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
            self.yvel = 0
        if not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]):
            self.xvel = 0

        # Проверка на коллизию. Если проходит, то перемещаем игрока
        if self.collide_x():
            self.rect.x += self.xvel
        if self.collide_y():
            self.rect.y += self.yvel

    # Проверка на коллизию по оси X
    def collide_x(self):
        for border in borders:
            if pygame.Rect(self.rect.x + self.xvel + 2, self.rect.y + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True

    # Проверка на коллизию по оси Y
    def collide_y(self):
        for border in borders:
            if pygame.Rect(self.rect.x + 2, self.rect.y + self.yvel + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True


def main():
    """
            Инициализация переменных
    """
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    # Открытие меню
    menu.Menu('background_menu.png', screen, load_image, clock)

    # Инициализация классов
    hero = Hero((int(3.5 * TILE_SIZE * 20), int(3.5 * TILE_SIZE * 10)), speed=6)
    map = Map([34, 6, 7, 8, 14, 15, 16, 22, 23, 24, 30])
    camera = Camera(camera_configure, len(spawned_rooms) * TILE_SIZE * 26, len(spawned_rooms) * TILE_SIZE * 26)

    # Основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        all_entities.update(map)
        screen.fill((98,88,56))
        camera.update(hero)
        for e in all_sprites:
            screen.blit(e.image, camera.apply(e))
        screen.blit(hero.image, camera.apply(hero))
        pygame.display.flip()
        clock.tick(FPS)


main()
