import pygame.mixer
from constants import BACKGROUND_MUSICS, CURRENT_MUSIC

"""
                    Импорт звуков
"""
pygame.mixer.init()

button_sound = pygame.mixer.Sound('data/sounds/button.wav')
death_fall_sound = pygame.mixer.Sound('data/sounds/death_fall.wav')
death_wave_sound = pygame.mixer.Sound('data/sounds/death_wave.wav')
swish_attack_sounds = [pygame.mixer.Sound('data/sounds/swish-1.wav'), pygame.mixer.Sound('data/sounds/swish-2.wav'),
                       pygame.mixer.Sound('data/sounds/swish-3.wav')]
coins_sounds = [pygame.mixer.Sound('data/sounds/coins1.wav'), pygame.mixer.Sound('data/sounds/coins2.wav')]

pygame.mixer.music.load(BACKGROUND_MUSICS[CURRENT_MUSIC])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
pygame.mixer.music.set_endevent(pygame.USEREVENT)


def play_next_music():
    global CURRENT_MUSIC
    CURRENT_MUSIC = (CURRENT_MUSIC + 1) % 3
    pygame.mixer.music.load(BACKGROUND_MUSICS[CURRENT_MUSIC])
    pygame.mixer.music.play()

