"""! @brief Файл всех живых объектов"""
##
# @file entities.py
#
# @brief Файл всех живых объектов
#
# @section description_chest Описание
# Классы живых объектов, а также выстрелов и сплешей.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import math
import random
import pygame
from constants import IDLE, RUN, TILE_SIZE, SPLASH_IMAGE, PLAYER_SHOOT_COOLDOWN, DEFAULT_ENEMY_DAMAGE, ROOM_SIZE, \
    SHOTTER_SHOOT_COOLDOWN, SANDBULLET_IMG, BOOM_IMAGES, SHOOT
from gui import Hit, Title
from map_generator import borders, door_borders
from mixer import death_fall_sound, death_wave_sound, swish_attack_sounds
from static_func import load_image

all_entities = pygame.sprite.Group()  # Группа всех живых объектов
splash_sprites = pygame.sprite.Group()  # Группа всех пуль игрока
sand_bullet = pygame.sprite.Group()  # Группа всех пуль врагов

titles = []  # Список всех заголовков


class Entity(pygame.sprite.Sprite):
    """Класс всех энтити

    Объект способен проверять коллизии и проигрывать анимации, получать урон"""
    def __init__(self, position, speed, images_idle, images_run, size):
        """Инициализация"""
        super().__init__(all_entities)
        self.health_points = 100

        # Позиция и скорость (вектор скорости)
        self.x, self.y = position
        self.speed = speed
        self.x_vel, self.y_vel = 0, 0
        self.damage = 5

        # Номер кадра анимации // Графика
        self.count_image = 0
        self.image_size = size
        self.images_idle = images_idle
        self.images_run = images_run
        self.image = pygame.transform.scale(load_image(self.images_idle[0]), size)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.state = IDLE

        # Флаг направления спрайта
        self.look_right = False

    def get_position(self) -> tuple:
        """Получить позицию живого существа"""
        return self.x, self.y

    def set_position(self, position: tuple) -> None:
        """Сменить позицию на..."""
        self.x, self.y = position
        self.rect = self.image.get_rect().move(self.x, self.y)

    def change_state(self, state: int) -> None:
        """Изменить положение анимаций на ..."""
        if self.state != state:
            self.state = state
            self.count_image = 0

    def play_animation(self) -> None:
        """ Смена спрайта анимации в зависимости от состояния"""
        self.count_image += 0.1
        if int(self.count_image) >= max(len(self.images_idle), len(self.images_run)):
            self.count_image = 0

        # Устанавливаем номер кадра
        if self.state == RUN:
            self.image = pygame.transform.scale(load_image(self.images_run[int(self.count_image)]), self.image_size)
        elif self.state == IDLE:
            if int(self.count_image) >= len(self.images_idle):
                self.count_image = 0
            self.image = pygame.transform.scale(load_image(self.images_idle[int(self.count_image)]),
                                                self.image_size)

        # Если не смотрит в нужную сторону - разворачиваем
        if not self.look_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def collide_x(self) -> bool:
        """Проверка на коллизию по оси X"""
        next_rect = pygame.Rect(self.rect.x + self.x_vel + 2, self.rect.y + 2,
                                TILE_SIZE - 4, TILE_SIZE - 4)
        for border in borders:
            if next_rect.colliderect(border.rect):
                return False
        for border in door_borders:
            if next_rect.colliderect(border.rect):
                return False
        return True

    def collide_y(self) -> bool:
        """Проверка на коллизию по оси Y"""
        next_rect = pygame.Rect(self.rect.x + 2, self.rect.y + self.y_vel + 2,
                                TILE_SIZE - 4, TILE_SIZE - 4)
        for border in borders:
            if next_rect.colliderect(border.rect):
                return False
        for border in door_borders:
            if next_rect.colliderect(border.rect):
                return False
        return True

    def get_damage(self, damage: int, arr_hit: list, color: str) -> None:
        """Получение урона"""
        self.health_points -= damage
        Hit(damage=damage, coords=(self.rect.x, self.rect.y), color=color)


class Hero(Entity):
    """Класс главного героя

    Перемещение героя, смерть и его стрельба"""
    def __init__(self, position, speed, images_idle, images_run, size=(TILE_SIZE, TILE_SIZE)):
        super().__init__(position, speed, images_idle, images_run, size)
        self.is_alive = True
        self.coins = 0
        self.health_points = 100
        self.cooldown_tracker = 0

    def update(self) -> None:
        """Обновление всех положений

        Перемещение и анимация"""
        # Если жив
        if self.health_points > 0:
            # Проверка нажатых клавиш, изменение вектора направления и проигрывание анимации
            if pygame.key.get_pressed()[pygame.K_w]:
                self.change_state(RUN)
                self.y_vel = -self.speed
            if pygame.key.get_pressed()[pygame.K_s]:
                self.change_state(RUN)
                self.y_vel = self.speed
            if pygame.key.get_pressed()[pygame.K_a]:
                self.change_state(RUN)
                # Поворот изображения в сторону ходьбы
                self.look_right = False
                self.x_vel = -self.speed
            if pygame.key.get_pressed()[pygame.K_d]:
                self.change_state(RUN)
                self.look_right = True
                self.x_vel = self.speed

            # Сброс векторов направления, если ни одна клавиша не зажата
            if not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
                self.y_vel = 0
            if not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]):
                self.x_vel = 0

            # IDLE Сброс всех анимаций при остановке
            if not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]) and \
                    not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]):
                self.change_state(IDLE)
            # Проигрываем анимацию
            self.play_animation()

            # Проверка на коллизию. Если проходит, то перемещаем игрока
            if self.collide_x():
                self.rect.x += self.x_vel
            if self.collide_y():
                self.rect.y += self.y_vel
        else:
            if self.is_alive:
                self.image = pygame.transform.rotate(self.image, -90)
                self.death()

    # Смерть игрока
    def death(self):
        pygame.mixer.Sound.play(death_fall_sound)
        pygame.mixer.Sound.play(death_wave_sound)
        self.is_alive = False

    def update_cooldown(self, clock):
        self.cooldown_tracker -= clock.get_time() if self.cooldown_tracker > 0 else 0

    # Стрельба по КД
    def shoot_splash(self, event, camera):
        """Стрельба

        По истечению КД и если игрок жив - стреляем."""
        if self.cooldown_tracker <= 0 and self.is_alive:
            pygame.mixer.Sound.play(random.choice(swish_attack_sounds))
            mx, my = event.pos
            mx, my = abs(camera.state.x) + mx, abs(camera.state.y) + my
            Splash((self.rect.x, self.rect.y), 20, images=SPLASH_IMAGE, need_pos=(mx, my),
                   tiles_group=splash_sprites)
            self.cooldown_tracker = PLAYER_SHOOT_COOLDOWN


class Enemy(Entity):
    """Класс врага

    Перемещение врага, удар по КД"""
    def __init__(self, position, speed: int, images_idle, images_run, room_index: tuple,
                 size=(TILE_SIZE, TILE_SIZE)):
        """Инициализация"""
        super().__init__(position, speed, images_idle, images_run, size)
        self.damaged_from = None
        self.change_K = 1
        self.health_points = 20
        self.damage = DEFAULT_ENEMY_DAMAGE
        self.room_index = room_index
        self.size = size
        self.timer = 0  # Таймер для КД

    def update_enemy(self, arr: list, arr_hit: list, hero: Hero, clock, rooms: list):
        """Обновление врага

        Проверка на попадание в себя и анимации"""
        player_pos = (hero.rect.x, hero.rect.y)
        self.play_animation()
        self.check_damage(hero, arr_hit)

        if self.health_points <= 0:
            self.destruct(rooms, arr)

        self.move_to_player(player_pos, rooms)
        self.do_timer(clock)
        self.attack(hero, arr_hit)

    def collide_splash(self) -> bool:
        """Проверка коллизии с пулей игрока"""
        for splash in splash_sprites:
            if self.rect.colliderect(splash.rect):
                if splash != self.damaged_from:
                    self.damaged_from = splash
                    return True
        return False

    def attack(self, hero: Hero, arr_hit: list) -> None:
        """Атакуем героя если рядом и прошел КД"""
        if self.rect.colliderect(hero.rect):
            if self.timer > 600:
                hero.get_damage(self.damage, arr_hit, 'red')
                self.timer = 0

    def check_damage(self, hero: Hero, arr_hit: list) -> None:
        """Проверяем под атакой ли существо?"""
        if self.collide_splash():
            self.get_damage(hero.damage, arr_hit, 'yellow')

    def do_timer(self, clock: pygame.time.Clock):
        """Обновляем счетчик КД"""
        self.timer += clock.get_time()

    def move_to_player(self, player_pos: tuple, rooms: list) -> None:
        """Передвигаемся до игрока

        Если игрок в комнате"""
        first_ind, second_ind = self.room_index
        room, room_x, room_y = rooms[first_ind][second_ind]
        px, py = player_pos
        # Если игрок в комнате
        if (room_x < px < room_x + (ROOM_SIZE[0] - 5) * TILE_SIZE) and \
                (room_y < py < room_y + (ROOM_SIZE[1] - 5) * TILE_SIZE):
            px, py = player_pos
            dx, dy = px - self.rect.x, py - self.rect.y
            length = math.hypot(dx, dy)
            if 0 < abs(length) < 500:
                self.x_vel = dx / length
                self.y_vel = dy / length
                if self.collide_x():
                    self.rect.x += self.x_vel * self.speed
                    self.look_right = False if self.x_vel >= 0 else True
                    self.change_state(state=RUN)
                if self.collide_y():
                    self.rect.y += self.y_vel * self.speed
                    self.change_state(state=RUN)
            else:
                self.change_state(state=IDLE)

    def destruct(self, rooms: list, arr: list):
        """Деструктор при смерти

        Удаление всех используемых данных"""
        first_ind, second_ind = self.room_index
        lst = rooms[first_ind][second_ind][0].mobs
        del lst[lst.index(self)]
        if len(lst) == 0:
            rooms[first_ind][second_ind][0].have_monsters = False
            titles.append(Title(titles))
        del arr[arr.index(self)]
        self.kill()


class Splash(Entity):
    """Снаряд игрока

    Передвижение и проверка на коллизию"""
    def __init__(self, position: tuple, speed: int, images: list, need_pos: tuple, tiles_group,
                 size=(TILE_SIZE - 8, TILE_SIZE - 8)):
        """Инициализация"""
        super().__init__(position, speed, images, images, size)
        tiles_group.add(self)
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

    def move(self) -> None:
        """Передвижение снаряда

        Проверяем на коллизию и двигаем, если можем"""
        if not self.collide():
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
        else:
            self.kill()

    def collide(self) -> bool:
        """Проверка коллизии"""
        for border in borders:
            if self.rect.colliderect(border.rect):
                return True
        for border in door_borders:
            if self.rect.colliderect(border.rect):
                return True
        return False


class ShootingEnemy(Enemy):
    """Стреляющий враг

    Стрельба по откату, проигрывание анимации"""
    def __init__(self, position, speed: int, images_idle, images_shoot, room_index: tuple):
        """Инициализация"""
        super().__init__(position, speed, images_idle, images_idle, room_index)
        self.images_shoot = images_shoot

    def shoot(self, hero: Hero, arr_hit: list, rooms: list) -> None:
        """Стрельба по КД

        Если игрок в комнате - стреляем."""
        first_ind, second_ind = self.room_index
        room, room_x, room_y = rooms[first_ind][second_ind]
        px, py = hero.rect.x, hero.rect.y
        if (room_x < px < room_x + (ROOM_SIZE[0] - 5) * TILE_SIZE) and \
                (room_y < py < room_y + (ROOM_SIZE[1] - 5) * TILE_SIZE):
            needed_pos = (hero.rect.x, hero.rect.y)
            if self.timer > SHOTTER_SHOOT_COOLDOWN:
                self.change_state(SHOOT)
                SandBullet((self.rect.x, self.rect.y), 7, images=SANDBULLET_IMG, need_pos=needed_pos,
                           arr_hit=arr_hit, hero=hero, tile_group=sand_bullet)
                self.timer = 0

    def update_enemy(self, arr, arr_hit: list, hero, clock, rooms: list) -> None:
        """Проверка на ранение и смена кадра

        Обновление таймера, анимаций, проверка урона."""
        self.check_damage(hero, arr_hit)
        self.play_animation()

        if self.health_points <= 0:
            self.destruct(rooms, arr)

        self.do_timer(clock)
        self.shoot(hero, arr_hit, rooms)

    def play_animation(self) -> None:
        """Смена спрайта анимации в зависимости от состояния

        Прибавляем константу к переменной, затем округляем её, тем самым сменяем кадры с
        определенной частотой по индексу"""
        self.count_image += 0.05
        if int(self.count_image) >= max(len(self.images_idle), len(self.images_shoot)):
            self.count_image = 0
        # Устанавливаем номер кадра
        if self.state == SHOOT and int(self.count_image) < len(self.images_shoot):
            self.image = pygame.transform.scale(load_image(self.images_shoot[int(self.count_image)]), self.image_size)
        elif int(self.count_image) >= len(self.images_shoot):
            self.change_state(IDLE)
        elif self.state == IDLE:
            if int(self.count_image) >= len(self.images_idle):
                self.count_image = 0
            self.image = pygame.transform.scale(load_image(self.images_idle[int(self.count_image)]),
                                                self.image_size)
        # Если не смотрит в нужную сторону - разворачиваем
        if not self.look_right:
            self.image = pygame.transform.flip(self.image, True, False)


class SandBullet(Splash):
    """Класс песочной пули врага

    Проверка на коллизию и урон по герою"""
    def __init__(self, position: tuple, speed: int, images: list, need_pos: tuple, arr_hit: list, tile_group, hero,
                 size=(TILE_SIZE - 20, TILE_SIZE - 20)):
        """Инициализация"""
        super().__init__(position, speed, images, need_pos, tile_group, size)
        self.arr_hit = arr_hit
        self.hero = hero
        self.image = pygame.transform.flip(self.image, True, False)

    def collide(self) -> bool:
        """Проверка на коллизию"""
        for border in borders:
            if self.rect.colliderect(border.rect):
                return True
        for border in door_borders:
            if self.rect.colliderect(border.rect):
                return True
        if self.rect.colliderect(self.hero.rect):
            self.hero.get_damage(self.damage, self.arr_hit, 'red')
            return True
        return False


class Bomber(Enemy):
    """Взрывающийся враг

    Подходит к герою и разрывается на 4 снаряда."""
    def __init__(self, position, speed: int, images, room_index: tuple):
        """Инициализация"""
        super().__init__(position, speed, images, images, room_index)
        self.radius = 10
        self.damage = 20
        self.timer_started = False
        self.boom_image_index = 0

    def update_enemy(self, arr, arr_hit: list, hero, clock, rooms: list):
        """Обновление всех положений

        Проигрываем анимации, проверка на урон, на смерть, инкрементация таймера, взрыв"""
        player_pos = (hero.rect.x, hero.rect.y)
        self.check_damage(hero, arr_hit)
        if self.health_points <= 0:
            if self.boom_image_index == len(BOOM_IMAGES):
                self.shoot_bullets(hero, arr_hit)
                self.destruct(rooms, arr)
            elif self.timer % 10 == 0 and self.boom_image_index < len(BOOM_IMAGES):
                self.image = pygame.transform.scale(load_image(BOOM_IMAGES[self.boom_image_index]),
                                                    self.image_size)  # Todo: немного переделать get по индексу
                self.boom_image_index += 1
        self.do_timer(clock)
        if not self.timer_started:
            self.play_animation()
            self.move_to_player(player_pos, rooms)
        self.boom(hero, arr_hit, rooms)

    def boom(self, hero: Hero, arr_hit, rooms: list) -> None:
        """Взрываем моба"""
        if not self.timer_started:
            first_ind, second_ind = self.room_index
            room, room_x, room_y = rooms[first_ind][second_ind]
            px, py = hero.rect.x, hero.rect.y
            if (room_x < px < room_x + (ROOM_SIZE[0] - 5) * TILE_SIZE) and \
                    (room_y < py < room_y + (ROOM_SIZE[1] - 5) * TILE_SIZE):
                if pygame.Rect(self.rect.x - self.radius, self.rect.y - self.radius,
                               self.rect.w + self.radius, self.rect.h + self.radius).colliderect(hero.rect):
                    self.timer_started = True
        else:
            if self.timer > 600:
                if pygame.Rect(self.rect.x - self.radius, self.rect.y - self.radius,
                               self.rect.w + self.radius, self.rect.h + self.radius).colliderect(hero.rect):
                    if self.health_points > 0:
                        hero.get_damage(self.damage, arr_hit=arr_hit, color='red')
                if self.health_points > 0:
                    self.get_damage(self.damage, arr_hit=arr_hit, color='yellow')

    def do_timer(self, clock) -> None:
        """Обновление таймера"""
        if self.timer_started:
            self.timer += clock.get_time()

    def shoot_bullets(self, hero, arr_hit) -> None:
        """Разрыв на 4 пули"""
        SandBullet((self.rect.x, self.rect.y), 7, images=SANDBULLET_IMG, need_pos=(0, self.rect.y),
                   arr_hit=arr_hit, hero=hero, tile_group=sand_bullet)
        SandBullet((self.rect.x, self.rect.y), 7, images=SANDBULLET_IMG, need_pos=(9999, self.rect.y),
                   arr_hit=arr_hit, hero=hero, tile_group=sand_bullet)
        SandBullet((self.rect.x, self.rect.y), 7, images=SANDBULLET_IMG, need_pos=(self.rect.x, 0),
                   arr_hit=arr_hit, hero=hero, tile_group=sand_bullet)
        SandBullet((self.rect.x, self.rect.y), 7, images=SANDBULLET_IMG, need_pos=(self.rect.x, 9999),
                   arr_hit=arr_hit, hero=hero, tile_group=sand_bullet)
