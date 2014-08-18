# -*- coding: utf8 -*-

'''
Created on 24/07/2014

@author: Jonathas Magalhães
'''
from challenge.solution.solution_settings import EVALUATOR, TEST_SOLUTION, RESULTS_FILE, CLASSIFIERS_CONF,\
    REGRESSORS_CONF, DATASETS_CONF

import os.path
import numpy as np

from challenge.solution.dataset import DatasetManager
from challenge.solution.model   import ModelManager
from challenge.util.util        import discretize_solution, save_sheet, read_sheet, write_the_solution_file,\
    ranking_prediction
import itertools
from challenge.settings import SOLUTION_PATH, DATASET_PATH

class Solution():
    name            = None
    solution_file   = None
    regression      = None
    classification  = None
    dataset_key     = None
    
    def _combine_regressions(self, *solutions):
        v1 = solutions[0]['userid']
        v2 = solutions[0]['tweetid']
        
        if self.regression == 'sum':
            engagement = sum([float(solution['engagement']) for solution in solutions])
        elif self.regression == 'mean':
            engagement = np.average([float(solution['engagement']) for solution in solutions])
        elif self.regression == 'median':
            engagement = np.median([float(solution['engagement']) for solution in solutions])
        elif self.regression == 'ranking':
            engagement = sum([int(solution['engagement']) for solution in solutions])
        
        return {'userid': v1, 'tweetid': v2, 'engagement': engagement}
    
    def _order(self, solution):
        return sorted(solution, key=lambda data: (-int(data['userid']), -int(data['tweetid']), 
                                                                -int(data['engagement'])))
        
    def _combine_classifications_regression(self, regression_solution, *classification_solutions):
        v1 = classification_solutions[0]['userid']
        v2 = classification_solutions[0]['tweetid']
        
        majority        = len(classification_solutions)/2+1
        votes           = filter(float(classification_solutions['engagement']) == 0, classification_solutions)
        number_votes    = len(votes)
        
        if number_votes >= majority:
            v3 = regression_solution['engagement']
        else:
            v3 = float(regression_solution['engagement'])+1000
        return {'userid': v1, 'tweetid': v2, 'engagement': v3}
        
    def _combine_classification_regression(self, regression_solution, classification_solution):
        v1 = regression_solution['userid']
        v2 = regression_solution['tweetid']
        if float(classification_solution['engagement']) == 0.0:
            v3 = regression_solution['engagement']
        else:
            v3 = float(regression_solution['engagement'])+1000
        return {'userid': v1, 'tweetid': v2, 'engagement': v3}
    
               
    def create_solution(self, dataset):
        models_manager = ModelManager()
        if os.path.isfile(self.solution_file):
            print 'Solution ' + self.name + ' ' + self.classification + ' ' + self.regression + ' already created.'
            return
        elif self.classification == 'None':
            models  = models_manager.get_models(dataset = dataset, model_key = self.regression)
            if len(models) == 1:
                discretize_solution(file_in = models[0].prediction_file, file_out = self.solution_file)
            else:
                if self.regression == 'ranking':
                    solutions_models    = [read_sheet(file_name = SOLUTION_PATH + 's' + str(i) + '_solution.dat') 
                                           for i in range(1, 9)]
                    regressions         = map(lambda x: self._order(x), solutions_models)
            
                else:
                    regressions = [read_sheet(file_name = model.prediction_file) for model in models]
                
                regression  = map(lambda *args: self._combine_regressions(*args), *regressions)
                discretize_solution(prediction_in = regression, file_out = self.solution_file)
        else:
            regression_models       = models_manager.get_models(dataset = dataset, model_key = self.regression)
            classification_models   = models_manager.get_models(dataset = dataset, model_key = self.classification, 
                                                                model_type = 'classifier')
            regression_solution     = read_sheet(file_name = regression_models[0].prediction_file)
            
            if self.classification == 'majority':
                classification_solutions = [read_sheet(file_name = classification.prediction_file) 
                                            for classification in classification_models]
                solution = map(lambda r, *c: self._combine_classifications_regression(r, *c), regression_solution, 
                                  classification_solutions)
            else:
                classification_solution = read_sheet(file_name = classification_models[0].prediction_file)
                solution    = map(lambda x, y: self._combine_classification_regression(x, y), regression_solution, 
                                  classification_solution)
                
                
            
            discretize_solution(prediction_in = solution, file_out = self.solution_file)
        print 'Solution ' + self.name + ' ' + self.classification + ' ' + self.regression + ' created.'
            
class SolutionManager():
    
    solutions   = []
    datasets    = None
    
    def __init__(self, train = True):
        self._set_solutions()
        self._set_datasets()
        if train == True:
            for dataset_key in self.datasets:
                dataset = self.datasets[dataset_key] 
                self._train_test_models(dataset)
        
    def _set_solutions(self):
        classifier_keys = ['None'] + CLASSIFIERS_CONF.keys() + ['votation']
        regression_keys = REGRESSORS_CONF.keys() + ['mean', 'median', 'ranking'] 
        datasets_keys   = DATASETS_CONF.keys()
        
        solutions_combinations = itertools.product(datasets_keys, classifier_keys, regression_keys )
        i = 0
        for dataset_key, classification, regression in solutions_combinations:
            
            i += 1

            solution_obj                = Solution()
            solution_obj.name           = 's' + str(i)
            solution_obj.regression     = regression
            solution_obj.classification = classification
            solution_obj.dataset_key    = dataset_key
            solution_obj.solution_file  = SOLUTION_PATH + 's' + str(i) + '_solution.dat'
            
            self.solutions.append(solution_obj)
    
    def _set_datasets(self): 
        dataset_manager = DatasetManager()
        self.datasets = dataset_manager.get_datasets()
    
    def _train_test_models(self, dataset):
        model = ModelManager()
        model.train_models(dataset)
        model.test_models(dataset)
            
    def create_solutions(self):
        for solution in self.solutions:
            solution.create_solution(dataset = self.datasets[solution.dataset_key])
    
    def evaluate_classifiers(self):
        models_manager = ModelManager()
        dataset = self.datasets['tweets']
        print dataset
        classification_models   = models_manager.get_models(model_key = 'votation', model_type = 'classifier')
        for classification in classification_models:
            classification.test_evaluate(dataset.test_data_classification)
    
    def evaluate_solutions(self):
        from subprocess import Popen, PIPE, STDOUT
        
        rows = []
        title = ['Name', 'Prediction', 'Classification', 'DataSet', 'nDCG']
        
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
            row = [solution.name, solution.regression, solution.classification, solution.dataset_key, ndcg]
            rows.append(row)
        save_sheet(file_name = RESULTS_FILE, content = rows, title = title)
        
    def test_solution(self):
        rows        = read_sheet(file_name = DATASET_PATH + 'empty_real_solution.dat')
        solutions = []

        for row in rows:
            solution = {'userid': row['userid'], 'tweetid': row['tweetid'], 'engagement': 0.0}
            solutions.append(solution)
        discretize_solution(prediction_in = solutions, file_out = DATASET_PATH + 'teste_zeros.dat')
        #write_the_solution_file(solutions, self.prediction_file)
        