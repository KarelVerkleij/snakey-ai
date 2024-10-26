from snake.snake import App
from snake.utils import overrides

import pygame
from random import choice

class BotApp(App):

    def __init__(self, _logging=True):
        super().__init__(_logging)

        self.bot_name = 'RANDOM_BOT'

    @overrides(App)
    def on_loop(self):
        pygame.event.post(self.bot_input())
        self.game_loop()

    def bot_input(self) -> pygame.event.Event:
        
        list_of_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] 

        chosen_direction = choice(list_of_directions)

        return pygame.event.Event(pygame.KEYDOWN, key=chosen_direction)

if __name__ == '__main__':
    theApp = BotApp()
    theApp.on_execute()
