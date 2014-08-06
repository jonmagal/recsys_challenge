# -*- coding: utf8 -*-
'''
Created on 28/05/2014

@author: Jonathas Magalh������������������������������������������������������es
'''
import json
import os

def discretize_solution(file_in, file_out):
    solutions = read_sheet(file_in)
    
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
             'favourites_count', 'language', 'engagement']
    content = []
    
    for todo in todos:
        id_move             = int(todo[1])
        movie_rating        = int(todo[2]) 
        crawled_time        = int(todo[3])
        tweet_time          = int(convert_twitter_time(todo[4]['created_at']))
        followers_count     = int(todo[4]['user']['followers_count'])
        statuses_count      = int(todo[4]['user']['statuses_count'])
        favourites_count    = int(todo[4]['user']['favourites_count'])
        language            = str(todo[4]['user']['lang'])
        retweet_count       = int(todo[4]['retweet_count'])
        favorite_count      = int(todo[4]['favorite_count'])
        engagement          = retweet_count + favorite_count
        
        row = [id_move, movie_rating, crawled_time, tweet_time, followers_count, statuses_count, favourites_count, 
               language, engagement]
        content.append(row)
    save_sheet(file_name = output_file, content = content, title = title)

"""
API IMDbPy - http://imdbpy.sourceforge.net/

������ s������ instalar via easy_install ou pip:
    sudo pip install IMDbPY
    sudo easy_install IMDbPY

Aqui eu tive que atualizar o arquivo setup_tools do python.
Com a seguinte linha no terminal:
    sudo easy_install -U setuptools 
"""

def get_movie_info(codigo_do_filme):
    import imdb
    ia = imdb.IMDb()
    movie = ia.get_movie(codigo_do_filme)
    return {'titulo': movie['title'], 'rating': movie['rating'], 'votes': movie['votes'], 'ano': movie['year'], 'genero': movie['genre'][0], 'pais': movie['countries'][0], 'idioma': movie['lang'][0], 'directors': movie['director']} 


"""
Below, a list of the main keys you can encounter, the type of the value
returned by movieObject[key] and a short description/example:

title; string; the "usual" title of the movie, like "The Untouchables".
long imdb title; string; "Uncommon Valor (1983/II) (TV)"
canonical title; string; the title in the canonical format,
                         like "Untouchables, The".
long imdb canonical title; string; "Patriot, The (2000)".
year; string; the year of release or '????' if unknown.
kind; string; one in ('movie', 'tv series', 'tv mini series', 'video game',
                      'video movie', 'tv movie', 'episode')
imdbIndex; string; the roman number for movies with the same title/year.
director; Person list; a list of director's name (e.g.: ['Brian De Palma'])
cast; Person list; list of actor/actress, with the currentRole instance
                   variable set to a Character object which describe his
                   role/duty.
cover url; string; the link to the image of the poster.
writer; Person list; list of writers ['Oscar Fraley (novel)']
plot; list; list of plots and authors of the plot.
rating; string; user rating on IMDb from 1 to 10 (e.g. '7.8')
votes; string; number of votes (e.g. '24,101')
runtimes; string list; in minutes ['119'] or something like ['USA:118',
          'UK:116']
number of episodes; int; number or episodes for a series.
color info; string list; ["Color (Technicolor)"]
countries; string list; production's country ['USA', 'Italy']
genres; string list; one or more in (Action, Adventure, Adult, Animation,
        Comedy, Crime, Documentary, Drama, Family, Fantasy, Film-Noir,
        Horror, Musical, Mystery, Romance, Sci-Fi, Short, Thriller,
        War, Western) and other genres defined by IMDb.
akas; string list; list of aka for this movie
languages; string list; list of languages
"""
    
def create_csv_movie_info(the_sheet_file, output_file):
    import sys
    import codecs
    encode =sys.stdin.encoding

    todos   = read_sheet(the_sheet_file)
    title   = ['id_movie', 'rating_imdb', 'number_of_votes', 'year', 'gender', 'country', 'language', 'directors']
    content = []
    
    for todo in todos:
        id_movie             = todo['id_move']
        exists = False
        for row in content:
            if id_movie in row:
                exists = True        
        if not exists:
            info = get_movie_info(id_movie)
            rating_imdb = info['rating']
            movie_votes = info['votes']
            movie_year = info['ano']
            movie_genre = info['genero']
            movie_country = info['pais']
            movie_lang = info['idioma']
            
            row = [id_movie, rating_imdb, movie_votes, movie_year, movie_genre, movie_country, movie_lang]
            
            for director in info['directors']:
                row.append(director['name'].encode(encode))
                
            content.append(row)
            print row
            save_sheet(file_name = output_file, content = content, title = title)
