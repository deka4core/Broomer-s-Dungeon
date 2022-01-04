"""
    Файл с константами
"""

SIZE = WIDTH, HEIGHT = 1920, 1080
FPS = 60
TILE_SIZE = 64
MAPS_DIR = 'data/maps'
PLAYER_IMAGES = [f'player/player{i}.png' for i in range(1, 5)]
MAP_MAX_WIDTH = 5
MAP_MAX_HEIGHT = 5
ROOM_NUMBER = 5
MARGIN_ROOMS = 4
ROOM_SIZE = (20 + MARGIN_ROOMS, 10 + MARGIN_ROOMS)
HERO_SPEED = 6
BACKGROUND_COLOR = (162, 152, 98)
MONSTER_SHOTTER_IMAGES = [f'monster_classic/monster_classic{i}.png' for i in range(1, 5)]
MONSTER_CLASSIC_IMAGES = [f'enemy2.png']
BACKGROUND_MUSICS = [f'data/music/theme{i}.mp3' for i in range(1, 4)]
SPLASH_IMAGE = ['splash.png']  # Костыль НЕ ТРОГАТЬ
CURRENT_MUSIC = 0
LOGO_NAME = 'logo.png'
SHOOT_COOLDOWN = 400
MONSTERS_NUMBER = 5
CURSOR_IMAGE = 'cursor.png'
CHEST_OPENED_IMG = 'chest_opened.png'
CHEST_CLOSED_IMG = 'chest_closed.png'
SANDBULLET_IMG = ['sand_ball.png']

IDLE = 0
RUN = 1
