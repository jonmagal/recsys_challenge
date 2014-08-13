# -*- coding: utf8 -*-
'''
Created on 03/06/2014

@author: Jonathas Magalhães
'''
from challenge.settings import DATASET_PATH
from challenge.util.util import write_the_solution_file, read_sheet


def order_solution():
    solutions = read_sheet(DATASET_PATH + 'neural_solution.dat')
    
    # Sort the solutions on user id (desc), engagement (desc) and tweet id (desc)
    solutions = sorted(solutions, key=lambda data: (-int(data['userid']), -float(data['engagement']), -int(data['tweetid'])))
    
    solution_final = []
    
    for solution in solutions:
        solution_final.append([solution['userid'], solution['tweetid'], solution['engagement']])
    # Write the _solution file
    write_the_solution_file(solution_final, DATASET_PATH + 'neural_solution2.dat')