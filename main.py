from entities import *
from camera import Camera, camera_configure
from entities import Hero, monsters
from gui import gui_sprites
from monster_spawner import spawn_monsters


def main():
    """
            Инициализация переменных
    """
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    # Открытие меню
    Menu('background_menu.png', screen, load_image, clock)

    # Инициализация классов
    hero = Hero((int(TILE_SIZE * (3 * ROOM_SIZE[0] + ROOM_SIZE[0] // 2 - 1)),
                 int(TILE_SIZE * (3 * ROOM_SIZE[1] + ROOM_SIZE[1] // 2 - 1))), speed=HERO_SPEED, images=PLAYER_IMAGES,
                size=(45, 50))
    map_ = Map([34, 6, 7, 8, 14, 15, 16, 22, 23, 24, 30])
    camera = Camera(camera_configure, len(spawned_rooms) * TILE_SIZE * 26, len(spawned_rooms) * TILE_SIZE * 26)
    spawn_monsters(MONSTERS_NUMBER)

    splashes = []
    hit_marks = []

    # Эмбиент
    pygame.mixer.music.load('data/sounds/dungeon_ambient_1.ogg')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Основной цикл
    running = True
    frame = 0  # счетчик кадра
    pygame.mouse.set_visible(False)
    cooldown_tracker = 0
    while running:
        cooldown_tracker -= clock.get_time() if cooldown_tracker > 0 else 0
        frame = (frame + 1) % 11
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cooldown_tracker <= 0:
                    shoot_splash(event, hero, splashes)
                    cooldown_tracker = SHOOT_COOLDOWN
        draw_all(frame, camera, hero, monsters, splashes, hit_marks, clock)
        pygame.display.flip()
        clock.tick(FPS)


def draw_all(frame, camera, hero, monsters, splashes, hit_marks, clock):
    screen.fill(BACKGROUND_COLOR)

    all_entities.update(frame)
    camera.update(hero)

    for e in all_sprites:
        screen.blit(e.image, camera.apply(e))

    for m in monsters:
        m.update_e(arr=monsters, frame=frame, hero_damage=hero.damage, arr_hit=hit_marks,
                   player_pos=(hero.rect.x, hero.rect.y))
        screen.blit(m.image, camera.apply(m))

    screen.blit(hero.image, camera.apply(hero))

    for splash in splashes:
        splash.move(splashes)
        screen.blit(splash.image, camera.apply(splash))

    for hit in hit_marks:
        hit.do_timer(clock=clock, arr=hit_marks)

    for hit in gui_sprites:
        screen.blit(hit.image, camera.apply(hit))

    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        screen.blit(load_image(CURSOR_IMAGE), pos)


main()
