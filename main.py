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


# Выводит координату самой левой комнаты
def get_minimal_width(spawned_rooms):
    min_w = 9999
    for i in spawned_rooms:
        for j in i:
            if j != -1:
                min_w = j[-2] if j[-2] < min_w else min_w
    return min_w


def get_minimal_height(spawned_rooms):
    min_h = 9999
    for i in spawned_rooms:
        for j in i:
            if j != -1:
                min_h = j[-1] if j[-1] < min_h else min_h
    return min_h


def get_maximal_height(spawned_rooms):
    max_h = 0
    for i in spawned_rooms:
        for j in i:
            if j != -1:
                max_h = j[-1] if j[-1] > max_h else max_h
    return max_h


def get_maximal_width(spawned_rooms):
    max_w = 0
    for i in spawned_rooms:
        for j in i:
            if j != -1:
                max_w = j[-2] if j[-2] > max_w else max_w
    return max_w


minimal_w = get_minimal_width(spawned_rooms)
minimal_h = get_minimal_height(spawned_rooms)
maximal_h = get_maximal_height(spawned_rooms)
maximal_w = get_maximal_width(spawned_rooms)


# настройка слежения камеры
def camera_configure(camera, target_rect):
    left, top = target_rect[0], target_rect[1]
    width, height = camera[-2], camera[-1]
    left, top = -left + WIDTH / 2, -top + HEIGHT / 2

    left = min(-minimal_w + WIDTH / 4, left)  # Не движемся дальше левой границы
    left = max(-maximal_w + WIDTH / 4, left)  # Не движемся дальше правой границы
    top = min(-minimal_h + HEIGHT / 4, top)  # Не движемся дальше нижней границы
    top = max(-maximal_h + HEIGHT / 4, top)  # Не движемся дальше верхней границы

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
    hero = Hero((int(TILE_SIZE * (3 * ROOM_SIZE[0] + ROOM_SIZE[0] // 2 - 1)),
                 int(TILE_SIZE * (3 * ROOM_SIZE[1] + ROOM_SIZE[1] // 2 - 1))), speed=HERO_SPEED)
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
        screen.fill(BACKGROUND_COLOR)
        camera.update(hero)
        for e in all_sprites:
            screen.blit(e.image, camera.apply(e))
        screen.blit(hero.image, camera.apply(hero))
        pygame.display.flip()
        clock.tick(FPS)


main()
