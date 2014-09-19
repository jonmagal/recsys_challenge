# -*- coding: utf8 -*-
'''
Created on 06/08/2014

@author: Jonathas Magalhães
'''
from challenge.settings import DATASET_PATH, MODEL_PATH, PREDICTION_PATH, SOLUTION_PATH, PATH

EVALUATOR       = DATASET_PATH + 'rscevaluator-0.14-jar-with-dependencies.jar'
RESULTS_FILE    = PATH + 'results.csv'

RESULTS_ORDERED_FILE = PATH + 'results_ordered.csv'

"""'tweets_norm':
                 {'training_file'   : DATASET_PATH + 'tweets_training.csv',
                  'test_file'       : DATASET_PATH + 'tweets_test.csv',
                  'empty_solution'  : DATASET_PATH + 'empty_solution.dat', 
                  'test_solution'   : DATASET_PATH + 'test_solution.dat',  
                  'norm'            : True, },"""
                  
DATASETS_CONF = {'tweets':
                 {'training_file'   : DATASET_PATH + 'tweets_training.csv',
                  'test_file'       : DATASET_PATH + 'tweets_test.csv',
                  'empty_solution'  : DATASET_PATH + 'empty_solution.dat', 
                  'test_solution'   : DATASET_PATH + 'test_solution.dat', 
                  'norm'            : False, },
    
                 'imdb':
                 {'training_file'   : DATASET_PATH + 'imdb_training.csv',
                  'test_file'       : DATASET_PATH + 'imdb_test.csv',
                  'empty_solution'  : DATASET_PATH + 'empty_solution.dat', 
                  'test_solution'   : DATASET_PATH + 'test_solution.dat',  
                  'norm'            : False, },
                 
                 'final':
                 {'training_file'   : DATASET_PATH + 'final_training.csv',
                  'test_file'       : DATASET_PATH + 'final_test.csv',
                  'empty_solution'  : DATASET_PATH + 'final_empty_solution.dat', 
                  'test_solution'   : None,  
                  'norm'            : False, },
                 }

REGRESSORS_CONF = {'linear_regression1':
                   {'name'             : 'linear_regression1',
                    'classname'        : 'weka.classifiers.functions.LinearRegression',
                    'options'          : ['-S', '0', '-R', '1.0E-8'], },
                   
                   'linear_regression2':
                   {'name'             : 'linear_regression2',
                    'classname'        : 'weka.classifiers.functions.LinearRegression',
                    'options'          : ['-S', '1', '-R', '1.0E-8'], },
                   
                   'linear_regression3':
                   {'name'             : 'linear_regression3',
                    'classname'        : 'weka.classifiers.functions.LinearRegression',
                    'options'          : ['-S', '2', '-R', '1.0E-8'], },
                   
                   'pace_regression1':
                   {'name'             : 'pace_regression1',
                    'classname'        : 'weka.classifiers.functions.PaceRegression',
                    'options'          : ['-E', 'eb'], },
                   
                   'tree_m5p1':
                   {'name'             : 'tree_m5p1',
                    'classname'        : 'weka.classifiers.trees.M5P',
                    'options'          : [], },
                   
                   'tree_m5p2':
                   {'name'             : 'tree_m5p2',
                    'classname'        : 'weka.classifiers.trees.M5P',
                    'options'          : ['-N'], },
               } 

'''
'''

CLASSIFIERS_CONF = {'naive_bayes1':
                    {'name'             : 'naive_bayes1',
                     'classname'        : 'weka.classifiers.bayes.NaiveBayes',
                     'options'          : ['-K', ], },
                    
                    'naive_bayes2':
                    {'name'             : 'naive_bayes2',
                     'classname'        : 'weka.classifiers.bayes.NaiveBayes',
                     'options'          : ['-D'], },
                    
                    'svm1':
                    {'name'            : 'svm1',
                    'classname'        : 'weka.classifiers.functions.LibSVM',
                    'options'          : ['-K', '0',], },
                    
                    'svm2':
                    {'name'            : 'svm2',
                    'classname'        : 'weka.classifiers.functions.LibSVM',
                    'options'          : ['-K', '3',],
                    'model_file'       : MODEL_PATH + 'svm2.model',
                    'prediction_file'  : PREDICTION_PATH + 'svm2_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'svm2_solution.dat', },
                    
                    'ibk1':
                    {'name'            : 'ibk1',
                    'classname'        : 'weka.classifiers.lazy.IBk',
                    'options'          : ['-K', '11',], },
                    
                    'ibk2':
                    {'name'            : 'ibk2',
                    'classname'        : 'weka.classifiers.lazy.IBk',
                    'options'          : ['-K', '51',], },
                    
                    'ibk3':
                    {'name'            : 'ibk3',
                    'classname'        : 'weka.classifiers.lazy.IBk',
                    'options'          : ['-K', '101',], },
                    
                    } 
