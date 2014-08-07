# -*- coding: utf8 -*-

'''
Created on 07/08/2014

@author: Jonathas Magalhães
'''

from challenge.settings import DATASET_PATH
from challenge.solution.solution_settings import PREDICTORS_CONF, CLASSIFIERS_CONF

from weka.classifiers       import Classifier, Evaluation

import weka.core.serialization  as serialization


import os.path
from challenge.util.util import read_sheet, write_the_solution_file


class Model(object):
    '''
    classdocs
    '''
    name                = None
    classname           = None
    options             = None
    model_file          = None
    prediction_file     = None
    
    def train(self, training_data):
        if os.path.isfile(self.model_file):
            print 'Model ' + self.name + ' already trained.'
        else:
            model_weka = Classifier(classname = self.classname, options = self.options) 
            
            model_weka.build_classifier(data = training_data)
            serialization.write(filename = self.model_file, jobject = model_weka)
            print 'Model ' + self.name + ' trained and saved.'
            
    def test(self, test_data):
        if os.path.isfile(self.prediction_file):
            print 'Model ' + self.name + ' already tested.'
        elif not os.path.isfile(self.model_file):
            print 'Impossible testing this model. It should be trained first.'
        else: 
            if test_data == None:
                test_data = self.load_data(dfile = self.test_file)
                test_data = self.pre_process(dataset = test_data) 
            
            model_weka = Classifier(jobject = serialization.read(self.model_file)) 
            evaluation = Evaluation(data = test_data)
            evaluation.test_model(classifier = model_weka, data = test_data)
            
            predictions = evaluation.predictions()
            rows        = read_sheet(file_name = DATASET_PATH + 'empty_real_solution.dat')
            solutions = []

            for row in rows:
                solution = [row['userid'], row['tweetid'], predictions.pop(0).predicted()]
                solutions.append(solution)
            write_the_solution_file(solutions, self.prediction_file)
            
    
class ModelManager(object):
    
    def get_models(self, model_key, model_type = 'predictor'):
        if model_type == 'predictor':
            models_conf = PREDICTORS_CONF
        else:
            models_conf = CLASSIFIERS_CONF
        if model_key == 'mean' or model_key == 'median' or model_key == 'ranking':
            
            return self._set_models(models_conf.values())
        else:
            return self._set_models([models_conf[model_key]])
            
    def _set_models(self, models_conf_list):
        models = []
        for model in models_conf_list:
            model_obj = Model()
            model_obj.name              = model['name']
            model_obj.classname         = model['classname']
            model_obj.options           = model['options']
            model_obj.model_file        = model['model_file']
            model_obj.prediction_file   = model['prediction_file']
            model_obj.solution_file     = model['solution_file']
            models.append(model_obj)
        return models
    
    
    """
    train_file  = None
    test_file   = None  
    
    def set_datafile(self, train_file = None, test_file = None):
        if train_file == None:
            self.train_file = TRAIN_FILE
        else:
            self.train_file = train_file
        
        if test_file == None:
            self.test_file = TEST_FILE
        else:
            self.test_file = test_file
            
    def train_classifiers_models(self):
        self.set_datafile()
        self.set_models(CLASSIFIERS_CONF)
        
        training_data   = None
        
        for model in self.models:
            if os.path.isfile(model.model_file):
                print 'Model already treined.'
            else:
                if training_data == None:
                    training_data = self.load_data(dfile = self.train_file)
                    training_data = self.pre_process(dataset = training_data) 
                
                model_weka = Classifier(classname = model.classname, options = model.options) 
                model_weka.build_classifier(data = training_data)
                serialization.write(filename = model.model_file, jobject = model_weka)
                
    def test_classifiers(self):
        self.set_datafile()
        self.set_models(CLASSIFIERS_CONF)
        
        test_data       = None
        
        for model in self.models:
            if not os.path.isfile(model.model_file):
                print 'Impossible training this model. It should be trained first.'
        
            else: 
                if test_data == None:
                    test_data = self.load_data(dfile = self.test_file)
                    test_data = self.pre_process(dataset = test_data) 
                
                model_weka = Classifier(jobject = serialization.read(model.model_file)) 
                #model_weka.build_classifier(data = training_data)
                #serialization.write(filename = model.model_file, jobject = model_weka)
                
                evaluation = Evaluation(data = test_data)
                evaluation.test_model(classifier = model_weka, data = test_data)
                
                print model.name, evaluation.kappa(), evaluation.precision(class_index = 0)
            
    def train_predictor_models(self):
        self.set_datafile()
        self.set_models()
        
        training_data   = None
        test_data       = None
    
        for model in self.models:
            if not os.path.isfile(model.prediction_file):
                if training_data == None:
                    training_data   = self.load_data(dfile = self.train_file)
                if test_data == None:
                    test_data       = self.load_data(dfile = self.test_file)
                
                model_weka = Classifier(classname = model.classname, options = model.options) 
                model_weka.build_classifier(data = training_data)
        
                evaluation = Evaluation(data = test_data)
                evaluation.test_model(classifier = model_weka, data = test_data)
                
                predictions = evaluation.predictions()
                print 'Model trained. Now saving the model and predictions...'
                
                rows        = read_sheet(file_name = DATASET_PATH + 'empty_real_solution.dat')
                solutions = []
    
                for row in rows:
                    solution = {}
                    solution['userid']      = row['userid']
                    solution['tweetid']     = row['tweetid']
                    solution['engagement']  = predictions.pop(0).predicted()
                    solutions.append(solution)
                
                solutions = sorted(solutions, key=lambda data: (-int(data['userid']), -float(data['engagement']), 
                                                                -int(data['tweetid'])))
    
                solution_final = []
    
                for solution in solutions:
                    solution_final.append([solution['userid'], solution['tweetid'], solution['engagement']])
                # Write the _solution file
                write_the_solution_file(solution_final, model.prediction_file)
                serialization.write(filename = model.model_file, jobject = model_weka)
                
                print 'Models and predictions saved with success.'
            else:
                print 'Model already treined.'
                
    def generate_solution(self):
        for model in self.models:
            discretize_solution(file_in = model.prediction_file, file_out = model.solution_file)
    
    def test_pre_process_data(self):
        self.set_datafile()
        #self.set_models()
        test_data   = self.load_data(dfile = self.test_file)
        #print type(test_data)
        filtered    = self.pre_process(test_data)
        print filtered
    """