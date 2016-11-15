#!/usr/bin/env python

import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
import json
import webapp2
from google.appengine.api import urlfetch
import logging
from models import Option, Outcome, Event, Pick, UserGoatIndex
#from google.appengine.api import memcache
#import urllib2
#from xml.etree import ElementTree



class GameHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
        curr_date = datetime.datetime.strptime(self.request.get('date'), "%Y%m%d")
        #logging.info("HELLO")
        #logging.info(curr_date)
        #if curr_date is None:
        sport = self.request.get('sport')
        if sport == "nfl":
            qry = Event.query().filter(Event.sport == "nfl", Event.date > curr_date).order(Event.date)
            week = qry.fetch(1)[0].week
            curr_games_qry = Event.query().filter(Event.week == week)
        else:
            curr_games_qry = Event.query().filter(Event.date == curr_date, Event.sport == 'nba')
        curr_games_raw = curr_games_qry.fetch()
        responseData = []
        for curr_game in curr_games_raw:
            #curr_pick = Pick.query().filter(Pick.event.id() == curr_game.key.id())
            start_time = curr_game.start_time - datetime.timedelta(hours = 5) # to ET
            start_time = start_time.strftime("%H:%M:%S")
            winner = curr_game.outcome.winner
            if winner is not None:
                winner = winner.id()
            game_data = {
                            'time': start_time,
                            'sport': sport,
                            'game_id': curr_game.key.id(), 
                            'home': curr_game.options[0].get().tri_code, 
                            'home_id': curr_game.options[0].id(), 
                            'away': curr_game.options[1].get().tri_code, 
                            'away_id': curr_game.options[1].id(), 
                            'winner': winner}
            if sport == "nfl":
                game_data['week'] = week
                game_data['date'] = curr_game.date.strftime("%Y%m%d")
            if len(curr_game.outcome.scores) > 0:
                game_data['scores'] = curr_game.outcome.scores
            #start_time = curr_game.start_time.strftime("%H:%M:%S") 
            if user:
                curr_pick_qry = Pick.query().filter(Pick.user_id == user.user_id())
                curr_pick_qry = curr_pick_qry.filter(Pick.event == curr_game.key)
                #print curr_pick_qry
                curr_pick = curr_pick_qry.fetch()
                if len(curr_pick) > 0:
                    game_data['current_pick'] = curr_pick[0].pick.get().tri_code
                    responseData.append(game_data)
                    #responseData.append({'time': start_time, 'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'home_id': curr_game.options[0].id(), 'away': curr_game.options[1].get().tri_code, 'away_id': curr_game.options[1].id(), 'current_pick': curr_pick[0].pick.get().tri_code, 'winner': curr_game.outcome.winner.id()})
                else:
                    responseData.append(game_data)
                    #responseData.append({'time': start_time, 'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'home_id': curr_game.options[0].id(), 'away': curr_game.options[1].get().tri_code, 'away_id': curr_game.options[1].id(), 'winner': curr_game.outcome.winner.id()})
            else:
                responseData.append(game_data)
        # MAGIC
        self.response.out.write(json.dumps(responseData))

current_live_data = None
last_polled_ts = datetime.datetime.utcnow()

class LiveGameHandler(webapp2.RequestHandler):
    def get(self):
        global current_live_data
        global last_polled_ts
        #logging.info("HELLO")
        curr_ts = datetime.datetime.utcnow()
        if (curr_ts - last_polled_ts).total_seconds() > 10 or current_live_data is None:
            # poll new
            curr_date_str = datetime.datetime.strftime((curr_ts - datetime.timedelta(hours = 5)), "%Y%m%d")
            url =  "http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json".format(curr_date_str)
            #import json
            r = urlfetch.fetch(url)
            current_live_data = json.loads(r.content)['games']
            last_polled_ts = curr_ts
            logging.info("new nba poll")
            self.response.out.write(json.dumps(current_live_data))

        else:
            logging.info("using cached nba poll")
            self.response.out.write(json.dumps(current_live_data))

class UserGoatIndexHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        sport = self.request.get('sport')
        q = UserGoatIndex.query().filter(UserGoatIndex.sport == sport)
        results = q.fetch()
        user_goat_index = results[0]
        responseData = {
                            'num_pick': user_goat_index.num_pick,
                            'num_correct': user_goat_index.num_correct,
                            'accuracy': user_goat_index.accuracy

        }
        self.response.out.write(json.dumps(responseData))

