# -*- coding: utf8 -*-

'''
Created on 24/07/2014

@author: Jonathas Magalhães
'''
from challenge.settings import DATASET_PATH, PREDICTORS_CONF, TRAIN_FILE, TEST_FILE, MODEL_PATH, PREDICTION_PATH,\
    SOLUTION_PATH, CLASSIFIERS_CONF
from weka.core.converters   import Loader
from weka.classifiers       import Classifier, Evaluation

import weka.core.jvm            as jvm 
import weka.core.serialization  as serialization

import os.path

from challenge.util.util    import read_sheet, write_the_solution_file, discretize_solution
from weka.filters           import Filter

class Model(object):
    '''
    classdocs
    '''
    name                = None
    classname           = None
    options             = None
    model_file          = None
    prediction_file     = None
    solution_file       = None

class Solution():
    name        = None
    predictors  = None
    classifiers = None
    dataset     = None
    
class ModelManager(object):
    
    models      = []
    train_file  = None
    test_file   = None
    
    def __init__(self):
        jvm.start(packages = True)
        if not os.path.exists(MODEL_PATH):
            os.makedirs(MODEL_PATH)
        if not os.path.exists(PREDICTION_PATH):
            os.makedirs(PREDICTION_PATH)
        if not os.path.exists(SOLUTION_PATH):
            os.makedirs(SOLUTION_PATH)   
    
    def pre_process(self, dataset):   
        
        filter_data = Filter(classname = 'weka.filters.unsupervised.attribute.MathExpression', 
                             options = ['-unset-class-temporarily', '-E', "ifelse ( A>0, 1, 0 )", 
                                        '-V', '-R', 'last'])
        
        filter_data.set_inputformat(dataset)
        filtered = filter_data.filter(dataset)
        
        discretize_data = Filter(classname = 'weka.filters.unsupervised.attribute.NumericToNominal', 
                             options = ['-R', 'last'])
        
        discretize_data.set_inputformat(filtered)
        discretized = discretize_data.filter(filtered)
        
        return discretized
             
    def load_data(self, dfile, index = None):
        loader = Loader(classname = 'weka.core.converters.CSVLoader')
        data = loader.load_file(dfile = dfile)
        if index == None:
            data.set_class_index(data.num_attributes() - 1)
        else:
            data.set_class_index(index)
        return data

    def set_datafile(self, train_file = None, test_file = None):
        if train_file == None:
            self.train_file = TRAIN_FILE
        else:
            self.train_file = train_file
        
        if test_file == None:
            self.test_file = TEST_FILE
        else:
            self.test_file = test_file
        
    def set_models(self, models_conf = None):
        if models_conf == None:
            models_conf = PREDICTORS_CONF
    
        for model in models_conf:
            model_obj = Model()
            model_obj.name         = model['name']
            model_obj.classname         = model['classname']
            model_obj.options           = model['options']
            model_obj.model_file        = model['model_file']
            model_obj.prediction_file   = model['prediction_file']
            model_obj.solution_file     = model['solution_file']
            self.models.append(model_obj)
    
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
    