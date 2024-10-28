from snake.snake_bot import BotApp
from snake.utils import overrides

from random import randint

import pygame

# algorithm https://kychin.netlify.app/snake-blog/hamiltonian-cycle/#:~:text=When%20applied%20to%20the%20game,(like%20in%20my%20case).
# derived from python code https://github.com/CheranMahalingam/Snake_Hamiltonian_Cycle_Solver/blob/master/Snake_Solver.py

class LogicInfintyBotApp(BotApp):

    def __init__(self, bot_study_name='', log_file_path='../logs/bot_logic_inifity/test_log.log'):
        super().__init__()

        self.initial_snake_position = self.snake_position
        self.next_move = ""

        self.dict_of_direction_and_events = {'LEFT' : pygame.K_LEFT,
                                             'RIGHT': pygame.K_RIGHT,
                                             'UP'   : pygame.K_UP,
                                             'DOWN' : pygame.K_DOWN}
        
        self.snake_speed = 1000
        
        self.window_x, self.window_y = 200, 240

        self.snake_position = [randint(1,self.window_x/10 -1) * 10, randint(1,self.window_y/10 -1) * 10]
        self.snake_body = [self.snake_position]

    @overrides(BotApp)
    def bot_input(self):
        self.calculate_path()
        self.calculate_next_move()

        return pygame.event.Event(pygame.KEYDOWN, key=self.dict_of_direction_and_events[self.next_move])


    def calculate_next_move(self):
        # Identifies the starting position of the snake
        position = (int(self.snake_position[0]/10), int(self.snake_position[1]/10))
        
        # to ensure no out of bounds error
        self.doubled_circuit = self.circuit + self.circuit 

        print(position)
        print(self.circuit)

        # Identifies the position in the hamiltonian cycle at which the snake begins
        current_index_in_path = self.circuit.index(position)
        next_position_in_path = self.doubled_circuit[current_index_in_path+1]

        print(f"current_index_in_path: {current_index_in_path}")
        print(f"current_position_in_path: {position},  next_position_in_path: {next_position_in_path}")

        # calculate required change
        change_in_x = next_position_in_path[0] - position[0]
        change_in_y = next_position_in_path[1] - position[1]
        
        print(f"change_in_x: {change_in_x},  change_in_y: {change_in_y}")

        # convert into commands 
        if change_in_x == -1 and change_in_y == 0:
            self.next_move = 'LEFT'
        elif change_in_x == 1 and change_in_y == 0:
            self.next_move = 'RIGHT'
        elif change_in_x == 0 and change_in_y == 1:
            self.next_move = 'DOWN'
        elif change_in_x == 0 and change_in_y == -1:
            self.next_move = 'UP'
        else:
            print("something went wrong - illegal move")

        print(f"self.next_move: {self.next_move}")


    def calculate_path(self):
        self.circuit = self.prim_maze_generator(int(self.window_y/20), int(self.window_x/20))

    def prim_maze_generator(self, grid_rows, grid_columns):

        directions = dict()
        vertices = grid_rows * grid_columns

        # Creates keys for the directions dictionary
        # Note that the maze has half the width and length of the grid for the hamiltonian cycle
        for i in range(grid_rows):
            for j in range(grid_columns):
                directions[j, i] = []

        # The initial cell for maze generation is chosen randomly
        x = randint(0, grid_columns - 1)
        y = randint(0, grid_rows - 1)
        initial_cell = (x, y)

        current_cell = initial_cell

        # Stores all cells that have been visited
        visited = [initial_cell]

        # Contains all neighbouring cells to cells that have been visited
        adjacent_cells = set()

        # Generates walls in grid randomly to create a randomized maze
        while len(visited) != vertices:

            # Stores the position of the current cell in the grid
            x_position = current_cell[0]
            y_position = current_cell[1]

            # Finds adjacent cells when the current cell does not lie on the edge of the grid
            if x_position != 0 and y_position != 0 and x_position != grid_columns - 1 and y_position != grid_rows - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the left top corner of the grid
            elif x_position == 0 and y_position == 0:
                adjacent_cells.add((x_position + 1, y_position))
                adjacent_cells.add((x_position, y_position + 1))

            # Finds adjacent cells when the current cell lies in the bottom left corner of the grid
            elif x_position == 0 and y_position == grid_rows - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the left column of the grid
            elif x_position == 0:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the top right corner of the grid
            elif x_position == grid_columns - 1 and y_position == 0:
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))

            # Finds adjacent cells when the current cell lies in the bottom right corner of the grid
            elif x_position == grid_columns - 1 and y_position == grid_rows - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position - 1, y_position))

            # Finds adjacent cells when the current cell lies in the right column of the grid
            elif x_position == grid_columns - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))

            # Finds adjacent cells when the current cell lies in the top row of the grid
            elif y_position == 0:
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the bottom row of the grid
            else:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position + 1, y_position))
                adjacent_cells.add((x_position - 1, y_position))

            # Generates a wall between two cells in the grid
            while current_cell:

                current_cell = (adjacent_cells.pop())

                # The neighbouring cell is disregarded if it is already a wall in the maze
                if current_cell not in visited:

                    # The neighbouring cell is now classified as having been visited
                    visited.append(current_cell)
                    x = current_cell[0]
                    y = current_cell[1]

                    # To generate a wall, a cell adjacent to the current cell must already have been visited
                    # The direction of the wall between cells is stored
                    # The process is simplified by only considering a wall to be to the right or down
                    if (x + 1, y) in visited:
                        directions[x, y] += ['right']
                    elif (x - 1, y) in visited:
                        directions[x-1, y] += ['right']
                    elif (x, y + 1) in visited:
                        directions[x, y] += ['down']
                    elif (x, y - 1) in visited:
                        directions[x, y-1] += ['down']

                    break

        # Provides the hamiltonian cycle generating algorithm with the direction of the walls to avoid
        return self.hamiltonian_cycle(grid_rows, grid_columns, directions)


    # Finds a hamiltonian cycle for the snake to follow to prevent collisions with its body segments
    # Note that the grid for the hamiltonian cycle is double the width and height of the grid for the maze
    def hamiltonian_cycle(self, grid_rows, grid_columns, orientation):

        # The path for the snake is stored in a dictionary
        # The keys are the (x, y) positions in the grid
        # The values are the adjacent (x, y) positions that the snake can travel towards
        hamiltonian_graph = dict()

        # Uses the coordinates of the walls to generate available adjacent cells for each cell
        # Simplified by only considering the right and down directions
        for i in range(grid_rows):
            for j in range(grid_columns):

                # Finds available adjacent cells if current cell does not lie on an edge of the grid
                if j != grid_columns - 1 and i != grid_rows - 1 and j != 0 and i != 0:
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                        if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                    else:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'down' not in orientation[j, i-1]:
                        hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    if 'right' not in orientation[j-1, i]:
                        if (j*2, i*2) in hamiltonian_graph:
                            hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                        else:
                            hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]

                # Finds available adjacent cells if current cell is in the bottom right corner
                elif j == grid_columns - 1 and i == grid_rows - 1:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' not in orientation[j, i-1]:
                        hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    elif 'right' not in orientation[j-1, i]:
                        hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]

                # Finds available adjacent cells if current cell is in the top right corner
                elif j == grid_columns - 1 and i == 0:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                    else:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'right' not in orientation[j-1, i]:
                        hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]

                # Finds available adjacent cells if current cell is in the right column
                elif j == grid_columns - 1:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                    else:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'down' not in orientation[j, i-1]:
                        hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    if 'right' not in orientation[j-1, i]:
                        if (j*2, i*2) in hamiltonian_graph:
                            hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                        else:
                            hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]

                # Finds available adjacent cells if current cell is in the top left corner
                elif j == 0 and i == 0:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                        if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                    else:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]

                # Finds available adjacent cells if current cell is in the bottom left corner
                elif j == 0 and i == grid_rows - 1:
                    hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' not in orientation[j, i-1]:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2 + 1, i * 2)]

                # Finds available adjacent cells if current cell is in the left corner
                elif j == 0:
                    hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                        if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j*2 + 1, i*2 + 1] += [(j*2 + 1, i*2 + 2)]
                        else:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'down' not in orientation[j, i-1]:
                        hamiltonian_graph[j*2, i*2] += [(j*2 + 1, i*2)]

                # Finds available adjacent cells if current cell is in the top row
                elif i == 0:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                        if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                    else:
                        hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'right' not in orientation[j-1, i]:
                        hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]

                # Finds available adjacent cells if current cell is in the bottom row
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                    if 'down' not in orientation[j, i-1]:
                        hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                    if 'right' not in orientation[j-1, i]:
                        if (j*2, i*2) in hamiltonian_graph:
                            hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]
                        else:
                            hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

        # Provides the coordinates of available adjacent cells to generate directions for the snake's movement
        return self.path_generator(hamiltonian_graph, grid_rows*grid_columns*4)


    # Generates a path composed of coordinates for the snake to travel along
    def path_generator(self, graph, cells):

        # The starting position for the path is at cell (0, 0)
        path = [(0, 0)]

        previous_cell = path[0]
        previous_direction = None

        # Generates a path that is a hamiltonian cycle by following a set of general laws
        # 1. If the right cell is available, travel to the right
        # 2. If the cell underneath is available, travel down
        # 3. If the left cell is available, travel left
        # 4. If the cell above is available, travel up
        # 5. The current direction cannot oppose the previous direction (e.g. left --> right)
        while len(path) != cells:

            if previous_cell in graph and (previous_cell[0] + 1, previous_cell[1]) in graph[previous_cell] \
                    and previous_direction != 'left':
                path.append((previous_cell[0] + 1, previous_cell[1]))
                previous_cell = (previous_cell[0] + 1, previous_cell[1])
                previous_direction = 'right'
            elif previous_cell in graph and (previous_cell[0], previous_cell[1] + 1) in graph[previous_cell]  \
                    and previous_direction != 'up':
                path.append((previous_cell[0], previous_cell[1] + 1))
                previous_cell = (previous_cell[0], previous_cell[1] + 1)
                previous_direction = 'down'
            elif (previous_cell[0] - 1, previous_cell[1]) in graph \
                    and previous_cell in graph[previous_cell[0] - 1, previous_cell[1]] and previous_direction != 'right':
                path.append((previous_cell[0] - 1, previous_cell[1]))
                previous_cell = (previous_cell[0] - 1, previous_cell[1])
                previous_direction = 'left'
            else:
                path.append((previous_cell[0], previous_cell[1] - 1))
                previous_cell = (previous_cell[0], previous_cell[1] - 1)
                previous_direction = 'up'

        # Returns the coordinates of the hamiltonian cycle path
        return path


if __name__ == "__main__":
    TheApp = LogicInfintyBotApp()
    TheApp.on_execute()
