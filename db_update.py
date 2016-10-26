from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import datetime
import json

from data_classes import Option, Outcome, Event, Pick

def insert_curr_nba_games(curr_date):
    print json.loads

    url =  "http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json".format(curr_date)
    #import json
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    events = []
    for game in games:
    	hteam = Option.get_or_insert("nba{}".format(game['hTeam']['triCode']), tri_code = game['hTeam']['triCode'])
    	vteam = Option.get_or_insert("nba{}".format(game['vTeam']['triCode']), tri_code = game['vTeam']['triCode'])
    	#events.append(Event(id = "nba{}".format(game['gameId']), season = int(game['seasonYear']), options = [ndb.Key(Option, game['hTeam']['triCode']), ndb.Key(Option, game['vTeam']['triCode'])]))
    	events.append(Event(id = "nba{}".format(game['gameId']), season = int(game['seasonYear']), date =curr_date, options = [hteam.key, vteam.key], start_time = datetime.datetime.strptime( game['startTimeUTC'], "%Y-%m-%dT%H:%M:%S.000Z")))
    ndb.put_multi(events)

def update_nba_games(date):
    url = 'http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json'.format(date)
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    for game in games:
    	game_key = ndb.Key("Event", "nba{}".format(game['gameId']))
    	game_event = game_key.get()
    	game_event.outcome.scores = [int(game['hTeam']['score']), int(game['vTeam']['score'])]
        if int(game['hTeam']['score']) > int(game['vTeam']['score']):
            game_event.outcome.correct = ndb.Key("Option", game['hTeam']['triCode'])
        else:
            game_event.outcome.correct = ndb.Key("Option", game['vTeam']['triCode'])
    	game_event.put()



'''
Event(id = "11600021", season = 2016, date = 20161006, options = [ndb.Key(Option, "PHI"), ndb.Key(Option, "WAS")], outcome = Outcome(scores = [119, 125], correct = ndb.Key(Option, "WAS")))
'''
