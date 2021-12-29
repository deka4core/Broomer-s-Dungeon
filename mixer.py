import pygame.mixer
from constants import BACKGROUND_MUSICS, CURRENT_MUSIC

"""
                    Импорт звуков
"""
button_sound = pygame.mixer.Sound('data/sounds/button.wav')

swish_attack_sounds = [pygame.mixer.Sound('data/sounds/swish-1.wav'), pygame.mixer.Sound('data/sounds/swish-2.wav'),
                       pygame.mixer.Sound('data/sounds/swish-3.wav')]

pygame.mixer.music.load(BACKGROUND_MUSICS[CURRENT_MUSIC])
pygame.mixer.music.play()
pygame.mixer.music.set_endevent(pygame.USEREVENT)


def play_next_music():
    global CURRENT_MUSIC
    CURRENT_MUSIC = (CURRENT_MUSIC + 1) % 3
    pygame.mixer.music.load(BACKGROUND_MUSICS[CURRENT_MUSIC])
    pygame.mixer.music.play()

