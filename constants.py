"""
    Файл с константами
"""

SIZE = WIDTH, HEIGHT = 1920, 1080
FPS = 60
TILE_SIZE = 64
MAPS_DIR = 'data/maps'
MAP_MAX_WIDTH = 5
MAP_MAX_HEIGHT = 5
ROOM_NUMBER = 5
MARGIN_ROOMS = 4
ROOM_SIZE = (20 + MARGIN_ROOMS, 10 + MARGIN_ROOMS)
HERO_SPEED = 6
PLAYER_SHOOT_COOLDOWN = 400
SHOTTER_SHOOT_COOLDOWN = 2000
MONSTERS_NUMBER = 5
DEFAULT_ENEMY_DAMAGE = 5

# Музыка
BACKGROUND_MUSICS = [f'data/music/theme{i}.mp3' for i in range(1, 4)]
CURRENT_MUSIC = 0

# Положения анимации
IDLE = 0
RUN = 1

# Изображения
PLAYER_IMAGES_IDLE = ['player/player1.png']
PLAYER_IMAGES_RUN = [f'player/player{i}.png' for i in range(2, 5)]

MONSTER_CLASSIC_IMAGES_IDLE = ['enemy2.png']
MONSTER_CLASSIC_IMAGES_RUN = ['enemy2.png']

CURSOR_IMAGE = 'cursor.png'
CHEST_OPENED_IMG = 'chest_opened.png'
CHEST_CLOSED_IMG = 'chest_closed.png'
SANDBULLET_IMG = ['sand_ball.png']
LOGO_NAME = 'logo.png'
SPLASH_IMAGE = ['splash.png']
MONSTER_SHOTTER_IMAGES = [f'monster_classic/monster_classic{i}.png' for i in range(1, 5)]
RESULTS_IMAGE = 'results.png'

BACKGROUND_COLOR = (162, 152, 98)
