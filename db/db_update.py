from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.runtime import DeadlineExceededError
import urllib2
from xml.etree import ElementTree
import datetime
import json

from myapp.models import Option, Outcome, Event, Pick, UserGoatIndex
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
                events.append(Event(
                    id = "nba{}".format(game['gameId']), 
                    sport = "nba", 
                    season = int(game['seasonYear']), 
                    date = curr_date, 
                    options = [hteam.key, vteam.key], 
                    start_time = datetime.datetime.strptime( game['startTimeUTC'], "%Y-%m-%dT%H:%M:%S.000Z")))
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


def insert_nfl_games():
    def schedule_url(year, stype, week):
        """
        Returns the NFL.com XML schedule URL. `year` should be an
        integer, `stype` should be one of the strings `PRE`, `REG` or
        `POST`, and `gsis_week` should be a value in the range
        `[0, 17]`.
        """
        xmlurl = 'http://www.nfl.com/ajax/scorestrip?'
        if stype == 'POST':
            week += 17
            if week == 21:  # NFL.com you so silly
                week += 1
        return '%sseason=%d&seasonType=%s&week=%d' % (xmlurl, year, stype, week)

    def get_nfl_matchup_info(game_id, game_state = "PRE"):
        url = "http://www.nfl.com/ajax/schedules/matchup?gameId={}&gameState={}".format(game_id, game_state)
        r = urlfetch.fetch(url)
        content = json.loads(r.content)
        return {
            "home_team": {"team_id": content['homeTeam']['teamId'], "abbr": content['homeTeam']['abbr'], "nickname": content['homeTeam']['nickName'], "city": content['homeTeam']['city']},
            "visitor_team": {"team_id": content['visitorTeam']['teamId'], "abbr": content['visitorTeam']['abbr'], "nickname": content['visitorTeam']['nickName'], "city": content['visitorTeam']['city']}
        }

    def get_game_meridiem(game, games):
        time_str = game['t']
        h = int(time_str.split(':')[0])
        m = int(time_str.split(':')[1])
        meridiem = None
        if 0 < h <= 5:
            meridiem = "PM"
        # test
        if meridiem is None:
            days_games = [g for g in games if g['d'] == game['d']]
            preceeding = [g for g in days_games if g['eid'] < game['eid']]
            proceeding = [g for g in days_games if g['eid'] > game['eid']]
            if any(h > t for t in [int(g['t'].split(':')[0]) for g in proceeding]):
                meridiem = 'AM'
            elif any(h < t for t in [int(g['t'].split(':')[0]) for g in preceeding]):
                meridiem = 'PM'
            # blah
            if meridiem is None:
                if game['d'] not in ['Sat', 'Sun']:
                    meridiem = 'PM'
                if game['gt'] == 'POST':
                    meridiem = 'PM'
        return meridiem 
    year = 2016
    stype = "REG"
    for i in xrange(1,18):
        week = i
        url = schedule_url(year, stype, week)
        # Insert all games. And then update
        result = urllib2.urlopen(url).read()
        root = ElementTree.fromstring(result)
        events = []
        games = [g.attrib for g in root.find('gms').findall('g')]
        for game in games:
            matchup_info = get_nfl_matchup_info(game['eid'])
            hteam = Option.get_or_insert(
                        "nfl{}".format(matchup_info["home_team"]["team_id"]), 
                        tri_code = matchup_info["home_team"]["abbr"],
                        nickname = matchup_info["home_team"]["nickname"],
                        city = matchup_info["home_team"]["city"]
                        )
            vteam = Option.get_or_insert(
                        "nfl{}".format(matchup_info["visitor_team"]["team_id"]), 
                        tri_code = matchup_info["visitor_team"]["abbr"],
                        nickname = matchup_info["visitor_team"]["nickname"],
                        city = matchup_info["visitor_team"]["city"])
            game_date = datetime.date(int(game['eid'][0:4]), int(game['eid'][4:6]), int(game['eid'][6:8]))
            meridiem = get_game_meridiem(game, games)
            h = int(game['t'].split(':')[0])
            m = int(game['t'].split(':')[1])
            if meridiem == "AM":
                start_time = datetime.time(h, m)
            else:
                start_time = datetime.time(h + 12, m)
            events.append(Event(
                id = "nfl{}".format(game['eid']),
                sport = "nfl", 
                season = int(game['eid'][0:4]), 
                event_type = stype,
                date = game_date,
                week = week,
                options = [hteam.key, vteam.key],
                start_time = datetime.datetime.combine(game_date, start_time)
                ))
        ndb.put_multi(events)
    return



def recalculate_goat_index(sport):
    ndb.delete_multi(
        UserGoatIndex.query().fetch(keys_only = True)
    )
    q = Pick.query().filter(Pick.sport == sport) # sport == "nba"
    picks = q.fetch()
    goat_indexes = []
    for pick in picks:
        #get_or_insert user goat index
        user_id = pick.user_id
        event = pick.event.get()
        if event.start_time < datetime.datetime.utcnow():
            goat_index = UserGoatIndex.get_or_insert("{}{}".format(sport, user_id), user_id = user_id, sport = sport, num_pick = 0, num_point = 0, num_correct = 0)
            outcome = event.outcome
            goat_index.num_pick = goat_index.num_pick + 1
            if outcome.winner == pick.pick:
                goat_index.num_correct = goat_index.num_correct + 1
            goat_indexes.append(goat_index)
    ndb.put_multi(goat_indexes)





'''
def insert_weekly_nfl_games():
    url = "http://www.nfl.com/liveupdate/scores/scores.json"
    r = urlfetch.fetch(url)
    if r.status_code == 404:
        break
    games = json.loads(r.content)
    for game_id in games:
        game_url = "http://www.nfl.com/feeds-rs/videos/byGameCenter/2016110605.json?gameState=PRE"
        r = urlfetch.fetch(url)
        if r.status_code == 404:
            break


    return
'''
'''
def update_schema_task():
    q = Pick.query()
    picks = q.fetch()
    for pick in picks:
        pick.sport = "nba"
        pick.put()
'''




