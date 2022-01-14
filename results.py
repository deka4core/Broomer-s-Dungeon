"""! @brief Файл окна результатов"""
##
# @file results.py
#
# @brief Файл окна результатов
#
# @section description_chest Описание
# Выводит на экран результаты из БД
#
# @section author_doxygen_example Автор(ы)
# - Created by dekacore on 28/12/2021.
# - Modified by dekacore on 14/01/2022.
#
# Copyright (c) 2022 Etherlong St. All rights reserved.
import sqlite3
import sys
import pygame
from constants import RESULTS_IMAGE, WIDTH, HEIGHT, FPS
from static_func import load_image


class Database:
    """Класс БД"""
    def __init__(self):
        self.connect()

    def connect(self):
        """Соединение с БД"""
        self.connection = sqlite3.connect(f"data/databases/dungeon.db")
        self.cursor = self.connection.cursor()

    def get_all_coins_value(self):
        """Получить значение всех монет"""
        return self.cursor.execute("""SELECT value FROM player where feature = 'coins'""").fetchone()[0]

    def set_all_coins_value(self, value):
        """Установить значение всех монет"""
        self.cursor.execute(f"""UPDATE player SET value = {value} WHERE feature = 'coins'""")
        self.connection.commit()

    def get_coins_value(self):
        """Получить значение раунд-монет"""
        return self.cursor.execute("""SELECT value FROM player where feature = 'coins_last_round'""").fetchone()[0]

    def get_timer_value(self):
        """Получить значение таймера"""
        return self.cursor.execute("""SELECT value FROM player where feature = 'timer'""").fetchone()[0]

    def get_kills_value(self):
        """Получить значение всех убийств"""
        return self.cursor.execute("""SELECT value FROM player where feature = 'kills'""").fetchone()[0]

    def get_alive_value(self):
        """Получить значение состояния игрока"""
        return self.cursor.execute("""SELECT value FROM player where feature = 'alive'""").fetchone()[0]

    def set_values(self, coins, timer, kills, alive):
        """Установить опрд. значения"""
        self.cursor.execute(f"""UPDATE player SET value = {coins} WHERE feature = 'coins_last_round'""")
        self.cursor.execute(f"""UPDATE player SET value = {timer} WHERE feature = 'timer'""")
        kills_ = self.get_kills_value()
        self.cursor.execute(f"""UPDATE player SET value = {kills_ + kills} WHERE feature = 'kills'""")
        self.cursor.execute(f"""UPDATE player SET value = {alive} WHERE feature = 'alive'""")
        self.connection.commit()

    def close_connection(self):
        """Закрыть соединение"""
        self.connection.close()


class Results:
    """Класс результатов.

    Окно результатов с данными из БД"""
    def __init__(self, screen, clock):
        """Инициализация"""
        self.screen = screen
        self.clock = clock
        self.results_image = pygame.transform.scale(load_image(RESULTS_IMAGE), (HEIGHT, HEIGHT))
        self.font = pygame.font.SysFont("data/font/BreakPassword.otf", 40)
        self.player_is_alive = True
        self.ended = False
        self.run()

    def run(self):
        """Основной цикл

        Отображение на экране итогов"""
        database = Database()
        coins_in_round = database.get_coins_value()
        timer = database.get_timer_value()
        kills = database.get_kills_value()
        alive = database.get_alive_value()
        database.close_connection()
        values = [timer, coins_in_round, kills, alive]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ended = True
            if self.ended:
                break
            self.draw(values)
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw(self, values):
        """Метод отрисовки"""
        self.screen.fill('black')
        self.screen.blit(self.results_image, (WIDTH // 2 - HEIGHT // 2, 0))
        result = self.font.render('LEVEL COMPLETED' if values[3] == 1 else 'YOU DIED', False, 'gold')
        self.screen.blit(result, (WIDTH // 2 - result.get_width() // 2, result.get_height() * 7))
        coins = self.font.render('COINS', False, 'gold')
        self.screen.blit(coins, (WIDTH // 2 - coins.get_width() * 3, HEIGHT // 2 - coins.get_height() // 1.75))
        coins_value = self.font.render(f'{values[1]}', False, 'black')
        self.screen.blit(coins_value, (WIDTH // 2 + HEIGHT // 6 - coins_value.get_width() // 2,
                                       HEIGHT // 2 - coins.get_height() // 1.75))
        time = self.font.render('TIME', False, 'gold')
        self.screen.blit(time, (WIDTH // 2 - time.get_width() * 3.75, HEIGHT // 2 - time.get_height() * 6))
        time_value = self.font.render(f'{int(values[0] / 60000)}:{int(values[0] / 1000 % 60)}', False, 'black')
        self.screen.blit(time_value, (WIDTH // 2 + HEIGHT // 6 - time_value.get_width() // 2,
                                      HEIGHT // 2 - time.get_height() * 6))
        kills = self.font.render('TOTAL KILLS', False, 'gold')
        self.screen.blit(kills, (WIDTH // 2 - kills.get_width() * 1.75, HEIGHT // 2 + kills.get_height() * 4.75))
        kills_value = self.font.render(f'{values[2]}', False, 'black')
        self.screen.blit(kills_value, (WIDTH // 2 + HEIGHT // 6 - kills_value.get_width() // 2,
                                       HEIGHT // 2 + kills.get_height() * 4.75))

    def terminate(self):
        """Выход из игры"""
        pygame.quit()
        sys.exit()