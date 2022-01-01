import random

import pygame.transform

from map_generator import *
from static_func import load_image
import math
from gui import Hit, Title

all_entities = pygame.sprite.Group()  # группа всех живых объектов
splash_sprites = pygame.sprite.Group()
monsters = []
titles = []


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
        self.damage = 5

        self.health_points = 100

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
            if pygame.Rect(self.rect.x + self.x_vel + 2, self.rect.y + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        for border in door_borders:
            if pygame.Rect(self.rect.x + self.x_vel + 2, self.rect.y + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True

    # Проверка на коллизию по оси Y
    def collide_y(self) -> bool:
        for border in borders:
            if pygame.Rect(self.rect.x + 2, self.rect.y + self.y_vel + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        for border in door_borders:
            if pygame.Rect(self.rect.x + 2, self.rect.y + self.y_vel + 2,
                           TILE_SIZE - 4, TILE_SIZE - 4).colliderect(border.rect):
                return False
        return True

    def get_damage(self, damage: int, arr_hit: list, color: str) -> None:
        self.health_points -= damage
        Hit(damage=damage, coords=(self.rect.x, self.rect.y), arr=arr_hit, color=color)


class Hero(Entity):
    """
        Класс главного героя
    """

    def __init__(self, position, speed, images, size=(TILE_SIZE, TILE_SIZE)):
        super().__init__(position, speed, images, size)
        self.is_alive = True

    def update(self, frame: int) -> None:
        if self.health_points > 0:
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
        else:
            if self.is_alive:
                self.image = pygame.transform.rotate(self.image, -90)
                self.death()

    def death(self):
        pygame.mixer.Sound.play(death_fall_sound)
        pygame.mixer.Sound.play(death_wave_sound)
        self.is_alive = False


class Enemy(Entity):
    """
        Класс врага
    """

    def __init__(self, position, speed: int, images, room_index: tuple, size=(TILE_SIZE, TILE_SIZE)):
        super().__init__(position, speed, images, size)

        self.damaged_from = None
        self.frame_K = 10
        self.health_points = 20
        self.damage = 5
        self.room_index = room_index

        self.timer = 0  # Todo: Таймер для ИИ
        self.behaviour = random.random()  # Todo: Поведение ИИ (60 % - шанс агрессивного ИИ)
        monsters.append(self)

    # Проверка на пробитие и смена кадра
    def update_e(self, arr: list, frame: int, hero_damage: int, arr_hit: list, hero, clock, rooms: list):
        player_pos = (hero.rect.x, hero.rect.y)
        if frame == self.frame_K:
            self.image_number = (self.image_number + 1) % 4
            self.image = pygame.transform.scale(load_image(self.images[self.image_number]), self.image_size)
        if self.collide_splash():
            self.health_points -= hero_damage
            self.get_damage(hero_damage, arr_hit, 'green')

        if self.health_points <= 0:
            first_ind, second_ind = self.room_index
            lst = rooms[first_ind][second_ind][0].mobs
            del lst[lst.index(self)]
            if len(lst) == 0:
                rooms[first_ind][second_ind][0].have_monsters = False
                titles.append(Title())
            del arr[arr.index(self)]
            self.kill()

        self.move_to_player(player_pos)
        self.do_timer(clock)
        self.attack(hero, arr_hit)

    def collide_splash(self) -> bool:
        for splash in splash_sprites:
            if self.rect.colliderect(splash.rect):
                if splash != self.damaged_from:
                    self.damaged_from = splash
                    return True
        return False

    # Атакуем героя если рядом и прошел КД
    def attack(self, hero: Hero, arr_hit: list) -> None:
        if self.rect.colliderect(hero.rect):
            if self.timer > 600:
                hero.get_damage(self.damage, arr_hit, 'red')
                self.timer = 0

    def do_timer(self, clock: pygame.time.Clock):
        self.timer += clock.get_time()

    def move_to_player(self, player_pos: tuple) -> None:
        if self.behaviour > 0.4:  # Приближается, чтобы дать игроку по голове
            px, py = player_pos
            dx, dy = px - self.rect.x, py - self.rect.y
            length = math.hypot(dx, dy)
            if 0 < abs(length) < 500:
                self.x_vel = dx / length
                self.y_vel = dy / length
                if self.collide_x():
                    self.rect.x += self.x_vel * self.speed
                if self.collide_y():
                    self.rect.y += self.y_vel * self.speed
        # else:  # Рандомно носится как ужаленный


class Splash(Entity):
    def __init__(self, position: tuple, speed: int, images: list, need_pos: tuple, size=(TILE_SIZE - 8, TILE_SIZE - 8)):
        super().__init__(position, speed, images, size)
        splash_sprites.add(self)
        # Mouse_x mouse_y
        self.need_pos = need_pos
        mx, my = need_pos
        # Delta_x delta_y
        dx, dy = mx - self.rect.x + TILE_SIZE // 2, my - self.rect.y
        # Траектория полета
        length = math.hypot(dx, dy)
        self.dx = dx / length
        self.dy = dy / length
        if dx < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, arr):
        if not self.collide():
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
        else:
            del arr[arr.index(self)]
            self.kill()

    def collide(self) -> bool:
        for border in borders:
            if self.rect.colliderect(border.rect):
                return True
        for border in door_borders:
            if self.rect.colliderect(border.rect):
                return True
        return False


def shoot_splash(event, hero, splashes, camera):
    pygame.mixer.Sound.play(random.choice(swish_attack_sounds))
    mx, my = event.pos
    mx, my = abs(camera.state.x) + mx, abs(camera.state.y) + my
    splash = Splash((hero.rect.x, hero.rect.y), 20, images=SPLASH_IMAGE, need_pos=(mx, my))
    splashes.append(splash)
