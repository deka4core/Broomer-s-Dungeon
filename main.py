from entities import *
from camera import Camera, camera_configure
from entities import Hero, Enemy


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
    monster = Enemy((int(TILE_SIZE * (3 * ROOM_SIZE[0] + ROOM_SIZE[0] // 2 - 1)),
                     int(TILE_SIZE * (3 * ROOM_SIZE[1] + ROOM_SIZE[1] // 2 - 2))), speed=HERO_SPEED - 2,
                    images=MONSTER_CLASSIC_IMAGES)

    monsters = [monster]
    splashes = []

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
            if event.type == pygame.USEREVENT:
                global CURRENT_MUSIC
                play_next_music()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cooldown_tracker <= 0:
                    shoot_splash(event, hero, splashes)
                    cooldown_tracker = SHOOT_COOLDOWN
        draw_all(frame, camera, hero, monsters, splashes)
        pygame.display.flip()
        clock.tick(FPS)


def draw_all(frame, camera, hero, monsters, splashes):
    all_entities.update(frame)
    screen.fill(BACKGROUND_COLOR)
    camera.update(hero)
    for e in all_sprites:
        screen.blit(e.image, camera.apply(e))
    for m in monsters:
        m.update_e(arr=monsters, frame=frame)
        screen.blit(m.image, camera.apply(m))
    screen.blit(hero.image, camera.apply(hero))
    for splash in splashes:
        splash.move(splashes)
        screen.blit(splash.image, camera.apply(splash))
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        screen.blit(load_image('cursor.png'), pos)


main()
