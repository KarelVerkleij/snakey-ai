from snake.snake import App
from snake.snake_bot import BotApp
from snake.snake_bot_logic_greedy import LogicGreedyBotApp

from time import sleep
import multiprocessing as mp

import logging
import os


class Analysis:

    def __init__(self):
        self.logging_config = "COMMANDLINE"

    def studyLogicGreedy(self):

        # self._logger_init()

        for i in range(0,2):
            theApp = LogicGreedyBotApp(bot_study_name=f"_{str(i)}")
            theApp.log_file_path = f'../logs/bot_logic_greedy/study_1_iteration_{str(i)}.log'
            
            print(f"i : {str(i)}")
            p = mp.Process(target=theApp.on_execute)        
            p.start()
            p.join()
            

                # if theApp._game_over:
                    
                #     bot_name = theApp.bot_name
                #     final_n_cylce = theApp.cycle_n
                #     final_score = theApp.score
                #     print(f"bot: {bot_name}, max_cycle: {final_n_cylce}, final_score {final_score}")
                #     theApp.game_exit()
                #     print("done")
                #     break
                    

            
            # self.logger_module.info(f"bot: {bot_name}, max_cycle: {final_n_cylce}, final_score {final_score}")

    # TODO fix logger
    def _logger_init(self):
        if self.logging_config == "COMMANDLINE":
            logging.basicConfig(
                                # filename=filename,
                                # filemode='a',
                                # force=True,
                                format='%(message)s,',
                                datefmt='%H:%M:%S',
                                level=logging.NOTSET)
        
        elif self.logging_config == "LOGFILE":
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.log_file_path)
            logging.basicConfig(
                                filename=filename,
                                filemode='a',
                                force=True,
                                format='%(message)s,',
                                datefmt='%H:%M:%S',
                                level=logging.NOTSET)
            
        logging.root.setLevel(logging.NOTSET)
        self.logger_module = logging.getLogger(__name__)

#TODO refactor to be able to spawn multiple processes with arguments
if __name__ == '__main__':
    analysis = Analysis()
    analysis.studyLogicGreedy()