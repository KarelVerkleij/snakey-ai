from snake.snake import App
from snake.utils import overrides

import pygame
from random import choice

class BotApp(App):

    def __init__(self, bot_study_name=''):
        super().__init__()
        
        self.default_bot_name = 'BOT_RANDOM'
        self.bot_name = self.default_bot_name + bot_study_name
        # self.log_file_path = '../logs/bot/test_log.log'
        self.logging_config="LOGFILE"

    @overrides(App)
    def on_loop(self):
        
        self.game_loop()
        pygame.event.post(self.bot_input())

    def bot_input(self) -> pygame.event.Event:
        
        list_of_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] 

        chosen_direction = choice(list_of_directions)

        return pygame.event.Event(pygame.KEYDOWN, key=chosen_direction)

if __name__ == '__main__':
    theApp = BotApp(log_file_path = '../logs/bot/test_log.log')
    theApp.on_execute()
