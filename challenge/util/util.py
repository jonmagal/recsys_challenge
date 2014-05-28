# -*- coding: utf8 -*-
'''
Created on 28/05/2014

@author: Jonathas Magalhães
'''
import json

def read_the_dataset(the_dataset_file):
    tweets = list()
    header = True
    with file(the_dataset_file,'r') as infile:
        for line in infile:
            if header:
                header = False
                continue # Skip the CSV header line
            line_array      = line.strip().split(',')
            user_id         = line_array[0]
            item_id         = line_array[1]
            rating          = line_array[2]
            scraping_time   = line_array[3]
            tweet           = ','.join(line_array[4:]) # The json format also contains commas
            json_obj        = json.loads(tweet) # Convert the tweet data string to a JSON object
            # Use the json_obj to easy access the tweet data
            # e.g. the tweet id: json_obj['id']
            # e.g. the retweet count: json_obj['retweet_count']
            tweets.append((user_id, item_id, rating, scraping_time, json_obj))
    return tweets

def read_todo_from_empty_file(the_dataset_file):
    todos = list()
    header = True
    with file(the_dataset_file,'r') as infile:
        for line in infile:
            if header:
                header = False
                continue # Skip the CSV header line
            line_array  = line.strip().split(',')
            tweet       = ','.join(line_array[4:]) # The json format also contains commas
            json_obj    = json.loads(tweet) # Convert the tweet data string to a JSON object
            user_id     = line_array[0]
            tweet_id    = json_obj['id']
            todos.append((user_id,tweet_id)) # The todo (user,tweet) pair
    return todos

def write_the_solution_file(solutions, the_solution_file):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')
    # Prepare the writing...
    for (user,tweet,engagement) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + '\n'
        lines.append(line)
    # Actual writing
    with file(the_solution_file,'w') as outfile:
        outfile.writelines(lines)