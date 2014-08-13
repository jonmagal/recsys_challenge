# -*- coding: utf8 -*-
'''
Created on 06/08/2014

@author: Jonathas Magalhães
'''
from challenge.settings import DATASET_PATH, MODEL_PATH, PREDICTION_PATH, SOLUTION_PATH, PATH

EVALUATOR       = SOLUTION_PATH + 'rscevaluator-0.14-jar-with-dependencies.jar'
TEST_SOLUTION   = SOLUTION_PATH + 'test_solution.dat'
RESULTS_FILE    = PATH + 'results.csv'

DATASETS_CONF = {'tweets':
                 {'training_file'   : DATASET_PATH + 'training_engagement.csv',
                  'test_file'       : DATASET_PATH + 'test_engagement.csv'},
                 }

REGRESSORS_CONF = {'linear_regression1':
                   {'name'             : 'linear_regression1',
                    'classname'        : 'weka.classifiers.functions.LinearRegression',
                    'options'          : ['-S', '0', '-R', '1.0E-8'],
                    'model_file'       : MODEL_PATH + 'linear_regression1.model',
                    'prediction_file'  : PREDICTION_PATH + 'linear_regression1_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'linear_regression1_solution.dat', },
                   
                   'linear_regression2':
                   {'name'             : 'linear_regression2',
                    'classname'        : 'weka.classifiers.functions.LinearRegression',
                    'options'          : ['-S', '1', '-R', '1.0E-8'],
                    'model_file'       : MODEL_PATH + 'linear_regression2.model',
                    'prediction_file'  : PREDICTION_PATH + 'linear_regression2_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'linear_regression2_solution.dat', },
                   
                   'linear_regression3':
                   {'name'             : 'linear_regression3',
                    'classname'        : 'weka.classifiers.functions.LinearRegression',
                    'options'          : ['-S', '2', '-R', '1.0E-8'],
                    'model_file'       : MODEL_PATH + 'linear_regression3.model',
                    'prediction_file'  : PREDICTION_PATH + 'linear_regression3_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'linear_regression3_solution.dat', },
                   
                   'pace_regression1':
                   {'name'             : 'pace_regression1',
                    'classname'        : 'weka.classifiers.functions.PaceRegression',
                    'options'          : ['-E', 'eb'],
                    'model_file'       : MODEL_PATH + 'pace_regression1.model',
                    'prediction_file'  : PREDICTION_PATH + 'pace_regression1_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'pace_regression1_solution.dat', },
                   
                   'tree_m5p1':
                   {'name'             : 'tree_m5p1',
                    'classname'        : 'weka.classifiers.trees.M5P',
                    'options'          : [],
                    'model_file'       : MODEL_PATH + 'tree_m5p1.model',
                    'prediction_file'  : PREDICTION_PATH + 'tree_m5p1_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'tree_m5p1_solution.dat', },
                   
                   'tree_m5p2':
                   {'name'             : 'tree_m5p2',
                    'classname'        : 'weka.classifiers.trees.M5P',
                    'options'          : ['-N'],
                    'model_file'       : MODEL_PATH + 'tree_m5p2.model',
                    'prediction_file'  : PREDICTION_PATH + 'tree_m5p2_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'tree_m5p2_solution.dat', },
               } 


CLASSIFIERS_CONF = {'naive_bayes1':
                    {'name'             : 'naive_bayes1',
                     'classname'        : 'weka.classifiers.bayes.NaiveBayes',
                     'options'          : ['-K', ],
                     'model_file'       : MODEL_PATH + 'naive_bayes1.model',
                     'prediction_file'  : PREDICTION_PATH + 'naive_bayes1_prediction.dat',
                     'solution_file'    : SOLUTION_PATH + 'naive_bayes1_solution.dat', },
                    
                    'naive_bayes2':
                    {'name'             : 'naive_bayes2',
                     'classname'        : 'weka.classifiers.bayes.NaiveBayes',
                     'options'          : ['-D'],
                     'model_file'       : MODEL_PATH + 'naive_bayes2.model',
                     'prediction_file'  : PREDICTION_PATH + 'naive_bayes2_prediction.dat',
                     'solution_file'    : SOLUTION_PATH + 'naive_bayes2_solution.dat', },
                    
                    'svm1':
                    {'name'            : 'svm1',
                    'classname'        : 'weka.classifiers.functions.LibSVM',
                    'options'          : ['-S', '0',],
                    'model_file'       : MODEL_PATH + 'svm1.model',
                    'prediction_file'  : PREDICTION_PATH + 'svm1_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'svm1_solution.dat', },
                    
                    'svm2':
                    {'name'            : 'svm2',
                    'classname'        : 'weka.classifiers.functions.LibSVM',
                    'options'          : ['-K', '0',],
                    'model_file'       : MODEL_PATH + 'svm2.model',
                    'prediction_file'  : PREDICTION_PATH + 'svm2_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'svm2_solution.dat', },
                    
                    'svm3':
                    {'name'            : 'svm3',
                    'classname'        : 'weka.classifiers.functions.LibSVM',
                    'options'          : ['-K', '3',],
                    'model_file'       : MODEL_PATH + 'svm3.model',
                    'prediction_file'  : PREDICTION_PATH + 'svm3_prediction.dat',
                    'solution_file'    : SOLUTION_PATH + 'svm3_solution.dat', },
                    
                    } 

SOLUTIONS = [{'name'            : 's1',
              'regression'      : 'linear_regression1',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's1_solution.dat', },
             
             {'name'            : 's2',
              'regression'      : 'linear_regression2',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's2_solution.dat',},
             
             {'name'            : 's3',
              'regression'      : 'linear_regression3',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's3_solution.dat',},
             
             {'name'            : 's4',
              'regression'      : 'pace_regression1',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's4_solution.dat',},
             
             {'name'            : 's5',
              'regression'      : 'tree_m5p1',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's5_solution.dat',},
             
             {'name'            : 's6',
              'regression'      : 'tree_m5p2',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's6_solution.dat',},
             
             {'name'            : 's7',
              'regression'      : 'mean',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's7_solution.dat',},
             
             {'name'            : 's8',
              'regression'      : 'median',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's8_solution.dat',},
             
             {'name'            : 's9',
              'regression'      : 'ranking',
              'classification'  : None,
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's9_solution.dat',},
             
             {'name'            : 's10',
              'regression'      : 'tree_m5p1',
              'classification'  : 'naive_bayes2',
              'dataset_key'     : 'tweets',
              'solution_file'   : SOLUTION_PATH + 's10_solution.dat',},
             ]