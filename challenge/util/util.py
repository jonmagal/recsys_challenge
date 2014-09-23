# -*- coding: utf8 -*-
'''
Created on 28/05/2014

@author: Jonathas Magalhães
'''
import json
import os

def save_file(file_name, content):
    with open(file_name, 'w') as file_:
        file_.write(content)

def read_sheet(file_name, fieldnames = None, delimiter = ",", quotechar = "\n"):
    from csv import DictReader
    
    reader = DictReader(open(file_name,'rb'), fieldnames = fieldnames, delimiter = delimiter, quotechar=quotechar)
    return reader

def concatenate_csv(csv1_file, csv2_file, out_file):
    fout = open(out_file, 'a')
    with file(csv1_file,'r') as infile:
        for line in infile:
            fout.write(line)
    header = True
    with file(csv2_file,'r') as infile:
        for line in infile:
            if header:
                header = False
                continue # Skip the CSV header line
            fout.write(line)        
    fout.close()


def save_sheet(file_name, content, title):        
    import csv
    with open(file_name, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(title)
        for c in content:
            csv_writer.writerow(c)
        
def write_the_solution_file(solutions, the_solution_file):
    lines = list()
    lines.append('userid,tweetid,engagement' + '\n')
    # Prepare the writing...
    for (user, tweet, engagement) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + '\n'
        lines.append(line)
    # Actual writing
    with file(the_solution_file,'w') as outfile:
        outfile.writelines(lines)

def ranking_prediction(predictions):
    solutions = sorted(predictions, key=lambda data: (-int(data['userid']), -float(data['engagement']), 
                                                                -int(data['tweetid'])))
    solution_final = []
    user = None
    solutions_list = list(solutions)
    temp_solution = []
    for i in range(len(solutions_list)):
        if user == None:
            user = solutions_list[i]['userid']
        temp_user = solutions_list[i]['userid']
        if temp_user != user or i == len(solutions_list)-1:
            if i == len(solutions_list)-1:
                temp_solution.append(i)
            tam = len(temp_solution)
            for x in temp_solution:
                solution_final.append({'userid': solutions_list[x]['userid'], 'tweetid': solutions_list[x]['tweetid'], 
                                       'engagement': tam})
                tam -= 1
            temp_solution = []
            user = temp_user
            temp_solution.append(i)
        else:
            temp_solution.append(i)
    return solution_final
    
def discretize_solution(file_out, file_in = None, prediction_in = None):
    if prediction_in == None:
        solutions = read_sheet(file_in)
    else:
        solutions = prediction_in
    solutions = sorted(solutions, key=lambda data: (-int(data['userid']), -float(data['engagement']), 
                                                                -int(data['tweetid'])))
    solution_final = []
    user = None
    solutions_list = list(solutions)
    temp_solution = []
    for i in range(len(solutions_list)):
        if user == None:
            user = solutions_list[i]['userid']
        temp_user = solutions_list[i]['userid']
        if temp_user != user or i == len(solutions_list)-1:
            if i == len(solutions_list)-1:
                temp_solution.append(i)
            tam = len(temp_solution)
            for x in temp_solution:
                solution_final.append([solutions_list[x]['userid'], solutions_list[x]['tweetid'], tam])
                tam -= 1
            temp_solution = []
            user = temp_user
            temp_solution.append(i)
        else:
            temp_solution.append(i)
    solution_final = sorted(solution_final, key=lambda data: (-int(data[0]), -int(data[2]), -int(data[1])))
    # Write the _solution file
    write_the_solution_file(solution_final, file_out)
    
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

def integer_to_datetime(date):
    import datetime
    return datetime.datetime.fromtimestamp(date)

def convert_twitter_time(date):
    import time
    td = time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')
    return time.mktime(td)
    
def create_empty_solution(the_dataset_file, output_file):
    try:
        todos   = read_the_dataset(the_dataset_file)
        title   = ['userid', 'tweetid']
    
        content = []
        
        for todo in todos:
            user_id     = int(todo[0])
            tweet_id    = int(todo[4]['id'])
            
            row = [user_id, tweet_id]
            
            content.append(row)
        save_sheet(file_name = output_file, content = content, title = title)
    except Exception, e:
        print e
        print todo
        return
    
def create_subdataset(the_dataset_file, output_file, final = False):
    try:
        todos   = read_the_dataset(the_dataset_file)
        title   = ['id_move', 'movie_rating', 'crawled_time', 'tweet_time', 'followers_count', 'statuses_count', 
                   'favourites_count', 'engagement']
             
        content = []
        
        for todo in todos:
            id_move             = int(todo[1])
            movie_rating        = int(todo[2]) 
            crawled_time        = int(todo[3])
            tweet_time          = int(convert_twitter_time(todo[4]['created_at']))
            followers_count     = int(todo[4]['user']['followers_count'])
            statuses_count      = int(todo[4]['user']['statuses_count'])
            favourites_count    = int(todo[4]['user']['favourites_count'])
            #language            = str(todo[4]['user']['lang'])
            #retweet_count       = int(todo[4]['retweet_count'])
            #favorite_count      = int(todo[4]['favorite_count'])
            if final:
                engagement          = 0
            else:
                retweet_count       = int(todo[4]['retweet_count'])
                favorite_count      = int(todo[4]['favorite_count'])
                engagement          = retweet_count + favorite_count
            
            row = [id_move, movie_rating, crawled_time, tweet_time, followers_count, statuses_count, 
                   favourites_count, engagement]
            
            content.append(row)
        save_sheet(file_name = output_file, content = content, title = title)
    except Exception, e:
        print e
        print todo
        return

def create_subdataset_test(the_dataset_file, output_file, final = False):
    try:
        todos   = read_the_dataset(the_dataset_file)
        title   = ['user_id', 'id_move', 'movie_rating', 'crawled_time', 'tweet_time', 'followers_count', 'statuses_count', 
                   'favourites_count', 'engagement']
             
        content = []
        
        for todo in todos:
            user_id             = int(todo[0])
            id_move             = int(todo[1])
            movie_rating        = int(todo[2]) 
            crawled_time        = int(todo[3])
            tweet_time          = todo[4]['created_at']
            followers_count     = int(todo[4]['user']['followers_count'])
            statuses_count      = int(todo[4]['user']['statuses_count'])
            favourites_count    = int(todo[4]['user']['favourites_count'])
            #language            = str(todo[4]['user']['lang'])
            #retweet_count       = int(todo[4]['retweet_count'])
            #favorite_count      = int(todo[4]['favorite_count'])
            if final:
                engagement          = 0
            else:
                retweet_count       = int(todo[4]['retweet_count'])
                favorite_count      = int(todo[4]['favorite_count'])
                engagement          = retweet_count + favorite_count
            
            row = [user_id, id_move, movie_rating, crawled_time, tweet_time, followers_count, statuses_count, 
                   favourites_count, engagement]
            
            content.append(row)
        
        #content_ordered = sorted(content, key=lambda data: (-int(data[0]), ))
        save_sheet(file_name = output_file, content = content, title = title)
    except Exception, e:
        print e
        print todo
        return
    
def create_subdataset_test2(the_dataset_file, output_file, final = False):
    try:
        todos   = read_the_dataset(the_dataset_file)
        title   = ['user_id', 'tweet_time']
             
        content = []
        
        for todo in todos:
            user_id             = int(todo[0])
            tweet_time          = todo[4]['created_at']
            row = [user_id, tweet_time]
            
            content.append(row)
        
        #content_ordered = sorted(content, key=lambda data: (-int(data[0]), ))
        save_sheet(file_name = output_file, content = content, title = title)
    except Exception, e:
        print e
        print todo
        return