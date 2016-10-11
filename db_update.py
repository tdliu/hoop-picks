#!/usr/bin/env python

import os

import MySQLdb
import json
from google.appengine.api import urlfetch


CLOUDSQL_PROJECT = '<hoopspredict>'
CLOUDSQL_INSTANCE = '<chris-bosh>'

db = MySQLdb.connect(db = "c9", user = "tdliu")

c = db.cursor()

def create_raw_user_picks_table():
    return """
    CREATE TABLE IF NOT EXISTS raw_user_picks (created_ts DATETIME, user_id VARCHAR(25), game_id INT, team_pick VARCHAR(10));
    """
    
def drop_raw_user_picks_table():
    return """
    DROP TABLE IF EXISTS raw_user_picks;
    """

"select * from user_picks join (select )"

# Table for processed user picks with results
# Last pick and whether or not it was correct

def drop_user_picks_table():
    return """
    DROP TABLE IF EXISTS user_picks;
    """

def create_user_picks_table():
    return """
    CREATE TABLE IF NOT EXISTS user_picks (created_ts DATETIME, user_id VARCHAR(25), game_id INT, correct_pick BOOLEAN);
    """
    
def insert_user_picks_table():
    return """
    INSERT INTO user_picks
    SELECT a.created_ts, a.user_id, a.game_id, CASE WHEN a.team_pick = c.winner THEN TRUE ELSE FALSE END AS correct_pick
    FROM raw_user_picks a
    JOIN 
    (SELECT user_id, game_id, max(created_ts) as created_ts FROM raw_user_picks GROUP BY user_id, game_id) b
    ON a.user_id = b.user_id AND a.game_id = b.game_id AND a.created_ts = b.created_ts
    JOIN
    (SELECT * from games) c
    ON a.game_id = c.game_id
    WHERE a.team_pick != "";
    """
    
def refresh_user_picks_table():
    c.execute(drop_user_picks_table())
    c.execute(create_user_picks_table())
    c.execute(insert_user_picks_table())
    return 0
    

"WITH (select user_id, game_id, max(created_ts) as created_ts from user_picks group by user_id, game_id)"

c.execute(create_user_picks_table())
c.execute("INSERT INTO user_picks VALUES (NOW(), 'tony_test', 123456, 'MIA')")
    
def create_games_table():
    return """
    CREATE TABLE IF NOT EXISTS games(seasonYear INT, game_id INT, date INT, home VARCHAR(10), away VARCHAR(10), home_score INT, away_score INT, winner VARCHAR(10));
    """
    
def drop_games_table():
    return """
    DROP TABLE IF EXISTS games;
    """

# Get today's games and get results from yesterday
# takes in today's date
def insert_games_table(curr_date):
    #curr_date = 20161007
    url = 'http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json'.format(curr_date)
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    for game in games:
        insert_str = """INSERT INTO games (seasonYear, game_id, date, home, away) 
        VALUES ({}, {}, {}, '{}', '{}');""".format(game['seasonYear'], game['gameId'], curr_date, game['hTeam']['triCode'], game['vTeam']['triCode'])
        c.execute(insert_str)
    return 0

    
def update_games_table(curr_date):
    prev_date = curr_date - 1
    url = 'http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json'.format(prev_date)
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    for game in games:
        if game['hTeam']['score'] > game['vTeam']['score']:
            winner = game['hTeam']['triCode']
        else:
            winner = game['vTeam']['triCode']
        c.execute("""UPDATE games 
        SET home_score = %s, away_score = %s, winner = %s
        WHERE game_id = %s;""", (game['hTeam']['score'], game['vTeam']['score'], winner, game['gameId']))
    return 0
    
c.execute(create_user_picks_table())
c.execute(drop_games_table())
c.execute(create_games_table())
curr_date = 20161006
insert_games_table(curr_date)
curr_date = 20161007
update_games_table(curr_date)
refresh_user_picks_table()
insert_games_table(curr_date)
curr_date = 20161008
update_games_table(curr_date)
insert_games_table(curr_date)



# table for most recent picks to be displayed
# joins games and users and gets today's and yesterday's games


# daily_update

#c.execute("INSERT INTO games (league, game_id, home, away, winner) values ('NBA', 123, 'TOR', 'MIA', 'MIA')")

'''
def get_nba_daily_games(date):

    #url = 'http://data.nba.net/data/10s/prod/v1/20161001/scoreboard.json'
    url = 'http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json'.format(date)
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    game_info = []
    for game in games:
        game_info.append(GameInfo(game['gameId'], game['hTeam']['triCode'], game['vTeam']['triCode'], date))
    return game_info
    
class GameInfo:
    def __init__(self, game_id, home, away, date):
        self.id = game_id
        self.home = home
        self.away = away
        self.date = date
        
        
'''



'''
db = MySQLdb.connect(
                unix_socket='/cloudsql/{}:{}'.format(
                    CLOUDSQL_PROJECT,
                    CLOUDSQL_INSTANCE),
                user='root')
'''
