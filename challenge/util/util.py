# -*- coding: utf8 -*-
'''
Created on 28/05/2014

@author: Jonathas Magalh������es
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
    lines.append('userid, tweetid, engagement' + '\n')
    # Prepare the writing...
    for (user, tweet, engagement) in solutions:
        line = str(user) + ',' + str(tweet) + ',' + str(engagement) + '\n'
        lines.append(line)
    # Actual writing
    with file(the_solution_file,'w') as outfile:
        outfile.writelines(lines)

def read_sheet(file_name, fieldnames=None, delimiter=",", quotechar="\n"):
    from csv import DictReader
    reader = DictReader(open(file_name,'rb'), fieldnames = fieldnames, delimiter = delimiter, quotechar=quotechar)
    return reader

def save_sheet(file_name, content, title):        
    import csv
    csv_writer = csv.writer(open(file_name, 'wb'))
    csv_writer.writerow(title)
    for c in content:
        csv_writer.writerow(c)
    
def integer_to_datetime(date):
    import datetime
    return datetime.datetime.fromtimestamp(date)

def convert_twitter_time(date):
    import time
    td = time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')
    return time.mktime(td)
    
def create_subdataset(the_dataset_file, output_file):
    todos   = read_the_dataset(the_dataset_file)
    title   = ['id_move', 'movie_rating', 'crawled_time', 'tweet_time', 'followers_count', 'statuses_count', 
             'favourites_count', 'language', 'retweet_count', 'favorite_count', 'engagement']
    content = []
    
    for todo in todos:
        id_move             = todo[1]
        movie_rating        = todo[2] 
        crawled_time        = todo[3]
        tweet_time          = convert_twitter_time(todo[4]['created_at'])
        followers_count     = todo[4]['user']['followers_count']
        statuses_count      = todo[4]['user']['statuses_count']
        favourites_count    = todo[4]['user']['favourites_count']
        language            = todo[4]['user']['lang']
        retweet_count       = todo[4]['retweet_count']
        favorite_count      = todo[4]['favorite_count']
        engagement          = retweet_count + favorite_count
        
        row = [id_move, movie_rating, crawled_time, tweet_time, followers_count, statuses_count, favourites_count, 
               language, retweet_count, favorite_count, engagement]
        content.append(row)
    save_sheet(file_name = output_file, content = content, title = title)
    