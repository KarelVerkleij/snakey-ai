from snake.snake import App
from snake.snake_bot import BotApp
from snake.snake_bot_logic_greedy import LogicGreedyBotApp

from time import sleep

from multiprocessing import Process

import logging
import os


class Analysis:

    def __init__(self):
        self.logging_config = "COMMANDLINE"
        
        # mp set up
        self.n_jobs = 0
        self.n_processes=4

    def studyLogicGreedy(self):

        
        for i in range(0,10):
            theApp = LogicGreedyBotApp(bot_study_name=f"_{str(i)}")
            theApp.log_file_path = f'../logs/bot_logic_greedy/study_1_iteration_{str(i)}.log'
            theApp.snake_speed=1000
            
            print(f"i : {str(i)}")
            p = Process(target=theApp.on_execute)        
            p.start()
            p.join()


#TODO refactor to be able to spawn multiple processes with arguments
if __name__ == '__main__':
    analysis = Analysis()
    analysis.studyLogicGreedy()


# ALL STUFF FOR MULTIPROCESSING NEED TO FIGURE OUT ONE DAY


    # p = Pool(2)

    # processes = [Process(target=LogicGreedyBotApp().on_execute(), 
    #                      args=({
    #                                 "bot_study_name" : f"_{str(i)}",
    #                                 "log_file_path" : f"../logs/bot_logic_greedy/study_1_iteration_{str(i)}.log"
    #                            })
    #                     ) for i in range(4)]
    
    # processes = [Process(target=LogicGreedyBotApp(bot_study_name = f"_{str(i)}",
    #                                               log_file_path = f"../logs/bot_logic_greedy/study_1_iteration_{str(i)}.log").on_execute()
    #                     ) for i in range(8)]
    # print(processes)

    # # Run processes
    # for p in processes:
    #     p.start()

    # # Exit the completed processes
    # for p in processes:
    #     p.join() 





# def mp_perform_study(self, tasks_to_accomplish, tasks_that_are_done):
#     while True:
#         try:
#             '''
#                 try to get task from the queue. get_nowait() function will 
#                 raise queue.Empty exception if the queue is empty. 
#                 queue(False) function would do the same task also.
#             '''
#             task = tasks_to_accomplish.get_nowait()
#         except queue.Empty:
#             break

#         else:
#             '''
#                 if no exception has been raised, add the task completion 
#                 message to task_that_are_done queue
#             '''
#             print(task)
#             tasks_that_are_done.put(task + ' is done by ' + current_process().name)
    
#     return True

# def mp_main(self):
#     tasks_to_accomplish = Queue()
#     tasks_that_are_done = Queue()
#     processes = []
    
#     for i in range(self.n_jobs):
#         tasks_to_accomplish.put("Task no " + str(i))

#     for w in range(self.n_processes):
#         p = Process(target=self.mp_perform_study, args=(tasks_to_accomplish, tasks_that_are_done))
#         processes.append(p)
#         p.start()

#     # completing process
#     for p in processes:
#         p.join()

#     # print the output
#     while not tasks_that_are_done.empty():
#         print(tasks_that_are_done.get())

#     return True
