from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import datetime
import json

from data_classes import Option, Outcome, Event, Pick

#content['data']['dates'][0]['date']
#content['data']['dates'][0]['fixtures'][0]
# Takes date in YYYY-MM-DD string format
# leagues: nhl, mlb, nba, nfl, ncaaf, ncaab, soccer
'''
def get_game_ids(start_date, sports):
    url = "http://www.si.com/private/content-proxy/scoreboard?date={}".format(start_date)
    #url = "http://www.si.com/private/content-proxy/scoreboard?date=2016-10-26"
    response = requests.get(url)
    content = response.json()
    fixtures = []
    if isinstance(sports, list):
        for sport in sports:
            fixtures.extend(content['data'][sport])
    else:
        fixtures.extend(content['data'][sports])
    return fixtures

def insert_fixtures(start_date, num_days, sports):
    # do stuff
    game_ids = get_game_ids(start_date, sports)
    url = "http://www.si.com/private/stats-proxy/v1/all_sports/event_scoreboard?events%5B%5D=1677892&events%5B%5D=1673898"
    for game_id in game_ids:

'''

def insert_nba_games(num_day, start_date):
    # e.g. datetime.date(2016,10,25)
    date_list = [start_date + datetime.timedelta(days=x) for x in range(0, num_day)]
    #date_str_list = [x.strftime("%Y%m%d") for x in date_list]
    for curr_date in date_list:
        curr_date_str = curr_date.strftime("%Y%m%d")
        url =  "http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json".format(curr_date_str)
        #import json
        r = urlfetch.fetch(url)
        games = json.loads(r.content)['games']
        events = []
        for game in games:
        	hteam = Option.get_or_insert("nba{}".format(game['hTeam']['teamId']), tri_code = game['hTeam']['triCode'])
        	vteam = Option.get_or_insert("nba{}".format(game['vTeam']['teamId']), tri_code = game['vTeam']['triCode'])
        	#events.append(Event(id = "nba{}".format(game['gameId']), season = int(game['seasonYear']), options = [ndb.Key(Option, game['hTeam']['triCode']), ndb.Key(Option, game['vTeam']['triCode'])]))
        	events.append(Event(id = "nba{}".format(game['gameId']), season = int(game['seasonYear']), date = curr_date, options = [hteam.key, vteam.key], start_time = datetime.datetime.strptime( game['startTimeUTC'], "%Y-%m-%dT%H:%M:%S.000Z")))
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
