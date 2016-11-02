from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.runtime import DeadlineExceededError

import datetime
import json

from data_classes import Option, Outcome, Event, Pick
import logging


def insert_nba_games(start_date):
    try:
        curr_date = start_date
        while True:
            curr_date_str = curr_date.strftime("%Y%m%d")
            print curr_date_str
            url =  "http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json".format(curr_date_str)
            r = urlfetch.fetch(url)
            if r.status_code == 404:
                break
            games = json.loads(r.content)['games']
            events = []
            for game in games:
                hteam = Option.get_or_insert("nba{}".format(game['hTeam']['teamId']), tri_code = game['hTeam']['triCode'])
                vteam = Option.get_or_insert("nba{}".format(game['vTeam']['teamId']), tri_code = game['vTeam']['triCode'])
                #events.append(Event(id = "nba{}".format(game['gameId']), season = int(game['seasonYear']), options = [ndb.Key(Option, game['hTeam']['triCode']), ndb.Key(Option, game['vTeam']['triCode'])]))
                events.append(Event(id = "nba{}".format(game['gameId']), sport = "nba", season = int(game['seasonYear']), date = curr_date, options = [hteam.key, vteam.key], start_time = datetime.datetime.strptime( game['startTimeUTC'], "%Y-%m-%dT%H:%M:%S.000Z")))
            ndb.put_multi(events)
            curr_date = curr_date + datetime.timedelta(days=1)
    except DeadlineExceededError:
        logging.exception("DeadlineExceededError")


def update_nba_games(date):
    date_str = date.strftime("%Y%m%d")
    url = 'http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json'.format(date_str)
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    for game in games:
    	game_key = ndb.Key("Event", "nba{}".format(game['gameId']))
    	game_event = game_key.get()
    	game_event.outcome.scores = [int(game['hTeam']['score']), int(game['vTeam']['score'])]
        if int(game['hTeam']['score']) > int(game['vTeam']['score']):
            game_event.outcome.winner = ndb.Key("Option", "nba{}".format(game['hTeam']['teamId']))
        else:
            game_event.outcome.winner = ndb.Key("Option", "nba{}".format(game['vTeam']['teamId']))
    	game_event.put()

def recalculate_goat_index(sport):
    q = Picks.query().filter()
    return

def update_goat_index(sport):
    # do stuff

    return

def update_schema_task():
    q = Pick.query()
    picks = q.fetch()
    for pick in picks:
        pick.sport = "nba"
        pick.put()




