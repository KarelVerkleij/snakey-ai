from snake.snake_bot import BotApp
from snake.utils import overrides

import pygame

# algorithm https://kychin.netlify.app/snake-blog/hamiltonian-cycle/#:~:text=When%20applied%20to%20the%20game,(like%20in%20my%20case).
# potential example python https://github.com/CheranMahalingam/Snake_Hamiltonian_Cycle_Solver/blob/master/Snake_Solver.py

class LogicBotApp(BotApp):

    def __init__(self, _logging=True):
        super().__init__(_logging)

        self.bot_name = 'LOGIC_BOT'

    @overrides 
    def bot_input(self) -> pygame.event.Event:

        chosen_direction = self.direction_picker()

        return pygame.event.Event(pygame.KEYDOWN, key=chosen_direction)

    def direction_picker(self):
        
        list_of_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] 

