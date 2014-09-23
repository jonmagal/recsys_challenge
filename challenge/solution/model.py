# -*- coding: utf8 -*-

'''
Created on 07/08/2014

@author: Jonathas Magalhães
'''

from challenge.settings import DATASET_PATH, MODEL_PATH, PREDICTION_PATH, EVALUATION_PATH, PARAMETER_PATH
from challenge.solution.solution_settings import REGRESSORS_CONF, CLASSIFIERS_CONF

from weka.classifiers       import Classifier, Evaluation

import weka.core.serialization  as serialization


import os.path
from challenge.util.util import read_sheet, write_the_solution_file, save_file
from challenge.solution.dataset import DataSet


class Model(object):
    '''
    classdocs
    '''
    name                = None
    classname           = None
    options             = None
    model_file          = None
    prediction_file     = None
    evaluation_file     = None
    parameter_file      = None
    
    def train_model(self, training_data):
        model_weka = None
        if os.path.isfile(self.model_file):
            print 'Model ' + self.name + ' already trained.'
        else:
            print 'Starting to train_model model ' + self.name + '.'
            model_weka = Classifier(classname = self.classname, options = self.options) 
            
            model_weka.build_classifier(data = training_data)
            serialization.write(filename = self.model_file, jobject = model_weka)
            print 'Model ' + self.name + ' trained and saved.'
        if os.path.isfile(self.parameter_file):
            print 'Parameters of the model ' + self.name + ' already saved.'
        else:
            if model_weka == None:
                model_weka = Classifier(jobject = serialization.read(self.model_file))
            save_file(file_name = self.parameter_file, content = str(model_weka))
            print 'Parameters of the model ' + self.name + ' saved.'
            
    def test_model(self, test_data, empty_solution, evaluate = False):
        model_weka = None
        if os.path.isfile(self.prediction_file):
            print 'Model ' + self.name + ' already tested.'
        elif not os.path.isfile(self.model_file):
            print 'Impossible testing this model. It should be trained first.'
            return
        else: 
            print 'Starting to test_model model ' + self.name + '.'
            model_weka = Classifier(jobject = serialization.read(self.model_file)) 
            evaluation = Evaluation(data = test_data)
            evaluation.test_model(classifier = model_weka, data = test_data)
            
            predictions = evaluation.predictions()
            rows        = read_sheet(file_name = empty_solution)
            solutions   = []

            for row in rows:
                solution = [row['userid'], row['tweetid'], predictions.pop(0).predicted()]
                solutions.append(solution)
            write_the_solution_file(solutions, self.prediction_file)
            print 'Model ' + self.name + ' tested.'
        
        if evaluate == True:
            if os.path.isfile(self.evaluation_file):
                print 'Model ' + self.name + ' already evaluated.'
                return
            elif model_weka == None:
                model_weka = Classifier(jobject = serialization.read(self.model_file)) 
                evaluation = Evaluation(data = test_data)
                evaluation.test_model(classifier = model_weka, data = test_data)
            save_file(file_name = self.evaluation_file, content = evaluation.to_summary())
            print 'Model ' + self.name + ' evaluated.'
            
class ModelManager(object):
    
    def get_models(self, dataset, model_key = 'None', model_type = 'regressor'):
        models_conf = None
        if model_type == 'regressor':
            models_conf = REGRESSORS_CONF
        elif model_type == 'classifier':
            models_conf = CLASSIFIERS_CONF
        
        if model_key == 'voting' or model_key == 'mean' or model_key == 'median' or model_key == 'ranking' or model_key == 'sum' or model_key == 'None':
            return self._set_models(dataset, models_conf.values())
        else:
            return self._set_models(dataset, [models_conf[model_key]])
            
    def _set_models(self, dataset, models_conf_list):
        models = []
        for model in models_conf_list:
            model_obj = Model()
            model_obj.name              = model['name']
            model_obj.classname         = model['classname']
            model_obj.options           = model['options']
            
            model_obj.evaluation_file   = EVALUATION_PATH + model_obj.name + '_' + dataset.dataset_key + '_evaluation.dat'
            model_obj.model_file        = MODEL_PATH + model_obj.name + '_' + dataset.dataset_key + '.model'
            model_obj.prediction_file   = PREDICTION_PATH + model_obj.name + '_' + dataset.dataset_key + '_prediction.dat'
            model_obj.parameter_file    = PARAMETER_PATH + model_obj.name + '_' + dataset.dataset_key + '_parameter.dat'
            models.append(model_obj)
        return models
    
    def train_models(self, dataset):
        predictors  = self.get_models(dataset = dataset)
        classifiers = self.get_models(dataset = dataset, model_type = 'classifier')
        
        for predictor in predictors:
            predictor.train_model(dataset.training_data_regression)
            
        for classifier in classifiers:
            classifier.train_model(dataset.training_data_classification)
            
    def test_models(self, dataset):
        predictors  = self.get_models(dataset = dataset)
        classifiers = self.get_models(dataset = dataset, model_type = 'classifier')
        
        evaluate = True
        if dataset.dataset_key == 'final':
            evaluate = False
        
        for predictor in predictors:
            predictor.test_model(dataset.test_data_regression, dataset.empty_solution, evaluate = evaluate)
        
        for classifier in classifiers:
            classifier.test_model(dataset.test_data_classification, dataset.empty_solution, evaluate = evaluate)
   
