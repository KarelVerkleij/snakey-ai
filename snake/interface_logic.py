from main import App
from boiler_plate import overrides

import pygame
from random import choice


class BotApp(App):

    @overrides(App)
    def on_loop(self):
        pygame.event.post(self.random_direction())
        self.game_loop()

    def random_direction(self):
        
        list_of_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] 

        chosen_direction = choice(list_of_directions)

        return pygame.event.Event(pygame.KEYDOWN, key=chosen_direction)

if __name__ == '__main__':
    theApp = BotApp()
    theApp.on_execute()
