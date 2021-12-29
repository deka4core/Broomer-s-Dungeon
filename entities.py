from map_generator import *
from static_func import load_image


all_entities = pygame.sprite.Group()  # группа всех живых объектов


class Entity(pygame.sprite.Sprite):
    """
        Класс всех энтити
    """

    def __init__(self, position, speed, images, size):
        super().__init__(all_entities)
        all_sprites.add(self)

        # Позиция и скорость (вектор скорости)
        self.x, self.y = position
        self.speed = speed
        self.x_vel, self.y_vel = 0, 0

        # Номер кадра анимации // Графика
        self.image_number = 0
        self.image_size = size
        self.images = images
        self.image = pygame.transform.scale(load_image(self.images[self.image_number]), size)
        self.rect = self.image.get_rect().move(self.x, self.y)

        # Через сколько кадров смена спрайта
        self.frame_K = 5

        # Флаг направления спрайта
        self.look_right = False

    # Получить позицию
    def get_position(self):
        return self.x, self.y

    # Сменить позицию на ...
    def set_position(self, position):
        self.x, self.y = position
        self.rect = self.image.get_rect().move(self.x, self.y)

    # Смена спрайта анимации в зависимости от состояния
    def play_animation(self, frame: int, state: int) -> None:
        # Устанавливаем номер кадра
        if state == RUN:
            if frame == self.frame_K:
                self.image_number = (self.image_number + 1) % 4
        elif state == IDLE:
            self.image_number = 0

        # Обновляем изображение, если не смотрит в нужную сторону - разворачиваем
        self.image = pygame.transform.scale(load_image(self.images[self.image_number]), self.image_size)
        if not self.look_right:
            self.image = pygame.transform.flip(self.image, True, False)

    # Проверка на коллизию по оси X
    def collide_x(self) -> bool:
        for border in borders:
            if pygame.Rect(self.rect.x + self.x_vel, self.rect.y,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True

    # Проверка на коллизию по оси Y
    def collide_y(self) -> bool:
        for border in borders:
            if pygame.Rect(self.rect.x, self.rect.y + self.y_vel,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True


class Hero(Entity):
    """
        Класс главного героя
    """

    def __init__(self, position, speed, images, size=(TILE_SIZE, TILE_SIZE)):
        super().__init__(position, speed, images, size)

    def update(self, frame: int) -> None:
        # Проверка нажатых клавиш, изменение вектора направления и проигрывание анимации
        if pygame.key.get_pressed()[pygame.K_w]:
            self.play_animation(frame, state=RUN)
            self.y_vel = -self.speed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.play_animation(frame, state=RUN)
            self.y_vel = self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            # Поворот изображения в сторону ходьбы
            self.look_right = False
            self.play_animation(frame, state=RUN)
            self.x_vel = -self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.look_right = True
            self.play_animation(frame, state=RUN)
            self.x_vel = self.speed

        # Сброс векторов направления, если ни одна клавиша не зажата
        if not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
            self.y_vel = 0
        if not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]):
            self.x_vel = 0

        # IDLE Сброс всех анимаций при остановке
        if not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]) and \
                not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
            self.play_animation(frame, state=IDLE)

        # Проверка на коллизию. Если проходит, то перемещаем игрока
        if self.collide_x():
            self.rect.x += self.x_vel
        if self.collide_y():
            self.rect.y += self.y_vel


class Enemy(Entity):
    """
        Класс врага
    """

    def __init__(self, position, speed, images, size=(TILE_SIZE, TILE_SIZE)):
        super().__init__(position, speed, images, size)

        self.frame_K = 10

    def update(self, frame=0):
        if frame == self.frame_K:
            self.image_number = (self.image_number + 1) % 4
            self.image = pygame.transform.scale(load_image(self.images[self.image_number]), (63, 63))

    def play_animation(self, frame: int, state: int) -> None:
        if state == IDLE:
            if frame == self.frame_K:
                self.image_number = (self.image_number + 1) % 4
            self.image = pygame.transform.scale(load_image(self.images[self.image_number]), (63, 63))


class Splash(Entity):
    def __init__(self, position: tuple, speed: int, images: list, need_pos: tuple, size=(TILE_SIZE, TILE_SIZE)):
        super().__init__(position, speed, images, size)