from snake_ml.snake_bot_ml import MLBotApp
from snake_ml.feed_foreward_neural_network import nn_snake

from multiprocessing import Process, Pipe
from random import randint, uniform

import matplotlib.pyplot as plt
import numpy as np

class Analysis:

    def __init__(self):
        self.logging_config = "COMMANDLINE"

        # neural network set-up
        self.neural_network_snake = nn_snake()
        self.num_weights = self.neural_network_snake.n_x*self.neural_network_snake.n_h + self.neural_network_snake.n_h*self.neural_network_snake.n_h2 + self.neural_network_snake.n_h2*self.neural_network_snake.n_y
        self.sol_per_pop = 50
        self.pop_size = (self.sol_per_pop, self.num_weights)
        self.new_population = np.random.choice(np.arange(-1, 1, step = 0.01), 
                                               size = self.pop_size, 
                                               replace=True)
        
        # genetic check set-up
        self.max_score = 0
        self.avg_score = 0
        self.test_games = 1
        self.score1 = 0
        self.steps_per_game = 2500 
        self.score2 = 0

        # genetic algo set-up / hyperparameters
        self.sol_per_pop = 50
        self.num_generations = 100
        self.crossover_percentage = 0.2
        self.mutation_intensity = 0.01
        self.num_parents_mating = (int)(self.crossover_percentage*self.sol_per_pop) # has to be even
        self.max_fitness = []
        
    def checkWeights(self, weights):

        parent_conn, child_conn = Pipe()
        for i in range(0,self.test_games):
            self.weights = weights
            

            theApp = MLBotApp(bot_study_name=f"_{str(i)}",
                              log_file_path = f'../logs/bot_ml/study_1_iteration_{str(i)}.log',
                              weights = self.weights,
                              steps_per_game=self.steps_per_game
                             )
            theApp.snake_speed=1000
            
            print(f"i : {str(i)}")
            p = Process(target=theApp.on_execute, args=(child_conn,))        
            p.start()
            p.join()

            self.collected_data = parent_conn.recv()
            self.score1, self.score2, self.max_score = self.collected_data["score1"], self.collected_data["score2"], self.collected_data["max_score"]

        # TODO how to tie this function to runTestGame / get updated values for this run
        # need to implement pipeline
        return self.score1 + self.score2 + self.max_score * 5000

# https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm/blob/main/Genetic_Algorithm.py

    def trainingGeneticModel(self):
        for generation in range(self.num_generations):
            # file1 = open(filename, "a+")
            # file1.write("##############        GENERATION " + str(generation)+ "  ############### \n")
            # file1.close()
            # print('##############        GENERATION ' + str(generation)+ '  ###############' )
            
            # Measuring the fitness of each chromosome in the population.
            fitness = self.cal_pop_fitness(self.new_population)
            self.max_fitness.append(np.max(fitness))
            
            # file1 = open(filename, "a+")
            # file1.write("#######  fittest chromosome in generation " + str(generation) + " is having fitness value:  " + str(np.max(fitness)) + "\n")
            # file1.close()
            # print('#######  fittest chromosome in generation ' + str(generation) + ' is having fitness value:  ', np.max(fitness))
            
            # Selecting the best parents in the population for mating.
            self.parents = self.select_mating_pool(self.new_population, fitness, self.num_parents_mating)
            # Generating next generation using crossover.
            self.offspring_crossover = self.crossover(self.parents, offspring_size = (self.pop_size[0] - self.parents.shape[0], 
                                                                                      self.num_weights))
            # Adding some variations to the offsrping using mutation.
            offspring_mutation = self.mutation(self.offspring_crossover, self.mutation_intensity)
            
            # Creating the new population based on the parents and offspring.
            self.new_population[0:self.parents.shape[0], :] = self.parents
            self.new_population[self.parents.shape[0]:, :] = offspring_mutation
            
        self.gen_count = list(range(1, self.num_generations+1))
        # #Plotting Graph
        plt.plot(self.gen_count, self.max_fitness )
        plt.xlabel('Generation count')
        plt.ylabel('Max Fitness value')
        plt.title('Plot')
        plt.show()

    # # TODO fix to class & remove circular dependency
    def cal_pop_fitness(self, pop, filename=None):
        # calculating the fitness value by playing a game with the given weights in chromosome
        fitness = []
        for i in range(pop.shape[0]):
            fit = self.checkWeights(pop[i])
            
            # file1 = open(filename, "a+")
            # file1.write("fitness value of chromosome " + str(i) + " :  " + str(fit) + "\n")
            # file1.close()
            # print('fitness value of chromosome '+ str(i) +' :  ', fit)
            fitness.append(fit)
        return np.array(fitness)

    def select_mating_pool(self, pop, fitness, num_parents):
        # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
        parents = np.empty((num_parents, pop.shape[1]))
        for parent_num in range(num_parents):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = pop[max_fitness_idx, :]
            fitness[max_fitness_idx] = -99999999
        return parents

    def crossover(self, parents, offspring_size):
        # creating children for next generation 
        offspring = np.empty(offspring_size)
        
        for k in range(offspring_size[0]): 
    
            while True:
                parent1_idx = randint(0, parents.shape[0] - 1)
                parent2_idx = randint(0, parents.shape[0] - 1)
                # produce offspring from two parents if they are different
                if parent1_idx != parent2_idx:
                    for j in range(offspring_size[1]):
                        if uniform(0, 1) < 0.5:
                            offspring[k, j] = parents[parent1_idx, j]
                        else:
                            offspring[k, j] = parents[parent2_idx, j]
                    break
        return offspring

    # two results with 0.1 and 0.01
    def mutation(self, offspring_crossover, mutation_intensity):
        # mutating the offsprings generated from crossover to maintain variation in the population
        for idx in range(offspring_crossover.shape[0]):
            for i in range(offspring_crossover.shape[1]):
                if uniform(0, 1) < mutation_intensity:
                    random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
                    offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
        return offspring_crossover

    # flat curve result
    # def mutation(offspring_crossover, mutation_intensity):
    #     # mutating the offsprings generated from crossover to maintain variation in the population
    #     num_genes_mutate = (int)(mutation_intensity*offspring_crossover.shape[1]/100)
    #     for idx in range(offspring_crossover.shape[0]):
    #         for _ in range(num_genes_mutate):
    #             i = randint(0, offspring_crossover.shape[1]-1)
    #             random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
    #             offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
    #     return offspring_crossover

if __name__ == "__main__":
    trainingAnalysis = Analysis()
    trainingAnalysis.trainingGeneticModel()