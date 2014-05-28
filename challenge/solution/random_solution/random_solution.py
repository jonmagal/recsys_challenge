# -*- coding: utf8 -*-
'''
Created on 28/05/2014

@author: Jonathas Magalhães
'''
import random
from challenge.util.util    import read_todo_from_empty_file, write_the_solution_file
from settings               import DATASET_PATH

def random_solution():
    # Read the training file

    # Read the _empty file (the task)
    todos = read_todo_from_empty_file(DATASET_PATH + 'test_empty.dat')

    # For all (user,tweet) pairs, generate their engagement
    solutions = list()
    #random.seed(1)
    for (user,tweet) in todos:
        # Random guess the engagement between 0-50
        engagement = random.randint(0,50)
        solutions.append((user,tweet,engagement))

    # Sort the solutions on user id (desc), engagement (desc) and tweet id (desc)
    solutions = sorted(solutions, key=lambda data: (-int(data[0]), -int(data[2]), -int(data[1])))

    # Write the _solution file
    write_the_solution_file(solutions, DATASET_PATH + 'random_solution.dat')

    print 'done.'