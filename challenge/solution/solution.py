# -*- coding: utf8 -*-

'''
Created on 24/07/2014

@author: Jonathas Magalhães
'''
from challenge.solution.solution_settings import SOLUTIONS, EVALUATOR, TEST_SOLUTION, RESULTS_FILE

import os.path
from challenge.solution.dataset import DatasetManager
from challenge.solution.model   import ModelManager
from challenge.util.util        import discretize_solution, save_sheet, read_sheet

class Solution():
    name            = None
    solution_file   = None
    prediction      = None
    classification  = None
    dataset_key     = None
    
    def create_solution(self, dataset):
        models_manager = ModelManager()
        if os.path.isfile(self.solution_file):
            print 'Solution already created.'
        elif self.classification == None:
            if self.prediction == 'mean':
                models = models_manager.get_models(model_key = self.prediction)
                solutions = read_sheet(file_in = models[0].prediction_file)
                
            elif self.prediction == 'median':
                pass
            elif self.prediction == 'ranking':
                pass
            else:
                models = models_manager.get_models(model_key = self.prediction)
                discretize_solution(file_in = models[0].prediction_file, file_out = self.solution_file)
            print 'Solution created.'
        else:
            pass
        
        
class SolutionManager():
    
    solutions   = []
    datasets    = None
            
    def _set_solutions(self):
        for solution in SOLUTIONS:
            solution_obj                = Solution()
            solution_obj.name           = solution['name']
            solution_obj.prediction     = solution['prediction']
            solution_obj.classification = solution['classification']
            solution_obj.dataset_key    = solution['dataset_key']
            solution_obj.solution_file  = solution['solution_file']
            
            self.solutions.append(solution_obj)
    
    def _set_datasets(self): 
        dataset_manager = DatasetManager()
        self.datasets = dataset_manager.get_datasets()
        
    def create_solutions(self):
        self._set_solutions()
        self._set_datasets()
        for solution in self.solutions:
            solution.create_solution(dataset = self.datasets[solution.dataset_key])
    
    def evaluate_solutions(self):
        from subprocess import Popen, PIPE, STDOUT
        
        rows = []
        title = ['Name', 'Prediction', 'Classification', 'DataSet', 'nDCG']
        self._set_solutions()
        for solution in self.solutions:
            row = []
            p = Popen(['java','-jar', EVALUATOR, solution.solution_file, TEST_SOLUTION], stdout = PIPE, 
                             stderr = STDOUT)
            
            ndcg = 0.0
            for line in p.stdout:
                if 'nDCG@10:' in line:
                    ndcg = line.replace('nDCG@10:', '')
                    ndcg = float(ndcg)
                    break
            row = [solution.name, solution.prediction, solution.classification, solution.dataset_key, ndcg]
            rows.append(row)
        save_sheet(file_name = RESULTS_FILE, content = rows, title = title)