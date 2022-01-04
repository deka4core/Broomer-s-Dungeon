from entities import *
from lobby import *
from chest import chests, chests_sprites
from camera import Camera, camera_configure
from gui import hit_sprites, HealthBar, CoinsBar
from monster_spawner import spawn_monsters
from static_func import update_fps


class Dungeon:
    def __init__(self, screen, clock):
        self.screen = screen
        self.start(clock)

    def start(self, clock):
        # Инициализация классов
        hero = Hero((int(TILE_SIZE * (3 * ROOM_SIZE[0] + ROOM_SIZE[0] // 2 - 1)),
                     int(TILE_SIZE * (3 * ROOM_SIZE[1] + ROOM_SIZE[1] // 2 - 1))), speed=HERO_SPEED,
                    images=PLAYER_IMAGES,
                    size=(45, 50))
        health_bar = HealthBar(self.screen, hero)

        map_ = Map([34, 6, 7, 8, 14, 15, 16, 22, 23, 24, 30])
        camera = Camera(camera_configure, len(spawned_rooms) * TILE_SIZE * 26, len(spawned_rooms) * TILE_SIZE * 26)
        spawn_monsters(MONSTERS_NUMBER)

        splashes = []
        hit_marks = []

        # Эмбиент
        pygame.mixer.music.load('data/sounds/dungeon_ambient_1.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Шрифт
        font = pygame.font.SysFont("Arial", 18)
        coins_bar = CoinsBar(self.screen, hero, font)

        # Различные флаги и переменные для отслеживания
        running = True
        frame = 0  # счетчик кадра
        alpha_value = 0  # альфа-канал затемнения
        death_bckg = pygame.Surface(SIZE)  # экран затемнения
        pygame.mouse.set_visible(False)  # выключаем мышь
        cooldown_tracker = 0  # Todo: Сделать нормальный КД-трекер

        # Основной цикл
        while running:

            # Изменение переменных
            cooldown_tracker -= clock.get_time() if cooldown_tracker > 0 else 0
            frame = (frame + 1) % 11

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Стрельба
                    if cooldown_tracker <= 0:
                        shoot_splash(event, hero, splashes, camera)
                        cooldown_tracker = SHOOT_COOLDOWN

            # Обновление всех положений
            all_entities.update(frame)
            camera.update(hero)
            check_player_room(hero, map_)
            for chest in chests:
                chest.update_hero(hero)


            # Отрисовка
            self.screen.fill(BACKGROUND_COLOR)
            for e in all_sprites:
                self.screen.blit(e.image, camera.apply(e))
            for chest in chests_sprites:
                self.screen.blit(chest.image, camera.apply(chest))
            self.screen.blit(hero.image, camera.apply(hero))
            for m in monsters:
                m.update_e(arr=monsters, frame=frame, hero_damage=hero.damage, arr_hit=hit_marks,
                           hero=hero, clock=clock, rooms=spawned_rooms)
                self.screen.blit(m.image, camera.apply(m))
            for splash in splashes:
                splash.move(splashes)
                self.screen.blit(splash.image, camera.apply(splash))
            for bullet in sand_bullet:
                bullet.move(bullets, hero)
                self.screen.blit(bullet.image, camera.apply(bullet))
            for hit in hit_marks:
                hit.do_timer(clock=clock, arr=hit_marks)
            health_bar.update(hero.health_points)
            for title in titles:
                title.do_timer(clock=clock, arr=titles)
                self.screen.blit(title.image, (title.rect.x, title.rect.y))
            for hit in hit_sprites:
                self.screen.blit(hit.image, camera.apply(hit))
            coins_bar.update(hero.coins)

            # Смена курсора на более удобный прицел
            if pygame.mouse.get_focused():
                pos = pygame.mouse.get_pos()
                self.screen.blit(load_image(CURSOR_IMAGE), pos)

            # Если герой умер
            if not hero.is_alive:
                if alpha_value < 250:
                    alpha_value += 1
                    death_bckg.set_alpha(alpha_value)
                    self.screen.blit(death_bckg, (0, 0))
                else:
                    self.destruct()
                    break

            # ФПС
            self.screen.blit(update_fps(clock, font), (WIDTH - 100, 25))
            pygame.display.flip()
            clock.tick(FPS)

    # Деструктор класса
    def destruct(self):
        pygame.mouse.set_visible(True)
        for sprite in all_sprites:
            sprite.kill()

    # Выход из игры
    def terminate(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
