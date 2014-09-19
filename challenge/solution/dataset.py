# -*- coding: utf8 -*-

'''
Created on 07/08/2014

@author: Jonathas Magalhães
'''

from weka.core.converters   import Loader
from weka.filters           import Filter
from challenge.solution.solution_settings import DATASETS_CONF

class DataSet(object):
    
    dataset_key     = None
    training_file   = None
    test_file       = None
    
    empty_solution  = None
    test_solution   = None
    norm            = None
    
    training_data_regression    = None
    test_data_regression        = None  
          
    training_data_classification    = None
    test_data_classification        = None  
    
    def __init__(self, dataset_key):
        self.dataset_key = dataset_key
    
    def get_test_data_prediction(self):
        if self.test_data_regression == None:
            self.test_data_regression = self._load_data(dfile = self.test_file)
        return self.test_data_regression
        
    def set_dataset_file(self):
        dataset_conf = DATASETS_CONF[self.dataset_key]
        self.training_file  = dataset_conf['training_file']
        self.test_file      = dataset_conf['test_file']
        self.empty_solution = dataset_conf['empty_solution']
        self.test_solution  = dataset_conf['test_solution']
        self.norm           = dataset_conf['norm']
    
    
    def set_prediction_dataset(self): 
        if self.training_data_regression == None and self.training_file != None:
            self.training_data_regression = self._load_data(dfile = self.training_file)
            if self.norm:
                self.training_data_regression = self._normalize_dataset(dataset = self.training_data_regression)
        if self.test_data_regression == None and self.test_file != None:
            self.test_data_regression = self._load_data(dfile = self.test_file)
            if self.norm:
                self.test_data_regression = self._normalize_dataset(dataset = self.test_data_regression)
                
    def set_classification_dataset(self):
        self.set_prediction_dataset()
        if self.training_data_classification == None and self.training_file != None:
            self.training_data_classification = self._pre_process_to_classification(dataset = self.training_data_regression)
        if self.test_data_classification == None and self.test_file != None:
            self.test_data_classification = self._pre_process_to_classification(dataset = self.test_data_regression)
        
    def _normalize_dataset(self, dataset):
        normalize_data = Filter(classname = 'weka.filters.unsupervised.attribute.Normalize', 
                             options = [])
        normalize_data.set_inputformat(dataset)
        normalized = normalize_data.filter(dataset)
        return normalized
        
    def _pre_process_to_classification(self, dataset):   
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
       
    def _load_data(self, dfile, index = None):
        loader = Loader(classname = 'weka.core.converters.CSVLoader')
        data = loader.load_file(dfile = dfile)
        if index == None:
            data.set_class_index(data.num_attributes() - 1)
        else:
            data.set_class_index(index)
        return data
    
class DatasetManager():
    
    def get_datasets(self):
        datasets = {}
        for dataset in DATASETS_CONF:
            dataset_obj = DataSet(dataset)
            dataset_obj.set_dataset_file()
            dataset_obj.set_classification_dataset()
            datasets[dataset] = dataset_obj
        return datasets
        