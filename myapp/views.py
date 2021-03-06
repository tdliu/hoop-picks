#!/usr/bin/env python

import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
import json
import webapp2
from google.appengine.api import urlfetch
import logging
from models import Option, Outcome, Event, Pick, UserGoatIndex

import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine
#from google.appengine.api import memcache
#import urllib2
#from xml.etree import ElementTree

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()


class GameHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
        curr_date = datetime.datetime.strptime(self.request.get('date'), "%Y%m%d")

        #if curr_date is None:
        sport = self.request.get('sport')
        #sport = 'nfl'
        
        if sport == "nfl":
            qry = Event.query().filter(Event.sport == "nfl", Event.date > curr_date).order(Event.date)
            week = qry.fetch(1)[0].week
            #logging.info(week)
            curr_games_qry = Event.query().filter(Event.week == week)
        else:
            curr_games_qry = Event.query().filter(Event.date == curr_date, Event.sport == 'nba')
        curr_games_raw = curr_games_qry.fetch()
        #logging.info(curr_games_raw)
        #logging.info(curr_games_raw)
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
                #logging.info("HELLO")
                
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
            curr_ts_et = curr_ts - datetime.timedelta(hours = 5)
            if curr_ts_et.time() > datetime.time(0) and curr_ts_et.time() < datetime.time(6):
                curr_date_str = datetime.datetime.strftime(curr_ts_et - datetime.timedelta(hours = 6), "%Y%m%d")
            else:
                curr_date_str = datetime.datetime.strftime(curr_ts_et, "%Y%m%d")
            url =  "http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json".format(curr_date_str)
            #import json
            r = urlfetch.fetch(url)
            nba_current_live_data = json.loads(r.content)['games']
            last_polled_ts = curr_ts
            
            self.response.out.write(json.dumps(nba_current_live_data))

        else:
            #logging.info("using cached nba poll")
            self.response.out.write(json.dumps(nba_current_live_data))

class UserGoatIndexHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            sport = self.request.get('sport')
            if sport == "all":
                q = UserGoatIndex.query().filter(UserGoatIndex.user_id == user.user_id())
            else:
                q = UserGoatIndex.query().filter(UserGoatIndex.sport == sport).filter(UserGoatIndex.user_id == user.user_id())
            results = q.fetch()
            if len(results) == 0:
                responseData = None
            else:
                user_goat_indexes = results
                num_pick = 0
                num_correct = 0
                for ugi in user_goat_indexes:
                    num_pick = num_pick + ugi.num_pick
                    num_correct = num_correct + ugi.num_correct
                accuracy = float(num_correct)/num_pick
                responseData = {
                                    'num_pick': num_pick,
                                    'num_correct': num_correct,
                                    'accuracy': accuracy,
                                    'rank': rank

                }
        else:
            responseData = None
        self.response.out.write(json.dumps(responseData))


# THESE ARE THE NEW HANDLERS

class GroupCreateHandler(webapp2.RequestHandler):
    def post(self):
        id_token = self.request.headers['Authorization'].split(' ').pop()
        if not claims:
            logging.info("AUTHENTICATION FAILED")
            #not authenticated!!! bad!!

        user_id = claims['sub'];
        data = json.loads(self.request.body)
        name = data['name'];
        password_required = data['password_required'];
        password = data['password'] if password_required else None;
        sport = data['sport'];

        #DO MAGIC 
        responseData = {
            'group' : None,
            'success' : False,
            'problem_param' : 'name',
            'message' : "This team name has been taken" 
        }
        self.response.out.write(json.dumps(responseData))


class UserHandler(webapp2.RequestHandler):
    def get(self):
        #logging.info(self.request.headers);
        id_token = self.request.headers['Authorization'].split(' ').pop()
        claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST);
        if not claims:
            logging.info("AUTHENTICATION FAILED")
            #not authenticated!!! bad!!

        user_id = claims['sub'];
        #do magic with user_id
        
        groups = [
            {
                'group_id' : '12345',
                'sport' : 'NBA',
                'creator' : 'abcdef',
                'name' : "Stanford",
                'password' : 'password123',
                'password_required' : True,
                'user_ids' : ['ghijkl', 'mnopqr'],
                'public' : True
            }
        ]
        responseData = {
            'goat_indeces' : {
                "overall" : {
                    'total': 50,
                    'correct': 34
                },
                "NBA" : {
                    'total': 20,
                    'correct': 10
                }
            },
            'groups' : groups,
            'success' : True,
            'message' : "success",
        }
        self.response.out.write(json.dumps(responseData))
