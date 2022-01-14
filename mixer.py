"""! @brief Файл музыки"""
##
# @file mixer.py
#
# @brief Файл музыки
#
# @section description_chest Описание
# Импорт всех звуков, музыки, метод переключения фоновой музыки.
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 23/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St.  All rights reserved.
import pygame.mixer
from constants import BACKGROUND_MUSICS, CURRENT_MUSIC
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
    """Переключить фоновую мелодию на следующую"""
    global CURRENT_MUSIC
    CURRENT_MUSIC = (CURRENT_MUSIC + 1) % 3
    pygame.mixer.music.load(BACKGROUND_MUSICS[CURRENT_MUSIC])
    pygame.mixer.music.play()

