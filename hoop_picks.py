#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
import datetime
#import data_classes as dc
from data_classes import Option, Outcome, Event, Pick
import db_update
import logging
import json

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

'''
class Option(ndb.Model):
    tri_code = ndb.StringProperty()

class Outcome(ndb.Model):
    scores = ndb.IntegerProperty(repeated = True)
    #home_score = ndb.IntegerProperty()
    #away_score = ndb.IntegerProperty()
    correct = ndb.KeyProperty(kind = Option)
    

class Event(ndb.Model):
    event_type = ndb.StringProperty()
    gameId = ndb.IntegerProperty()
    season = ndb.IntegerProperty()
    date = ndb.IntegerProperty()
    options = ndb.KeyProperty(kind = Option, repeated = True) # Use participant generated ID
    #away = ndb.KeyProperty(kind = Option)
    outcome = ndb.StructuredProperty(Outcome)
    #participants = ndb.KeyProperty(kind = Participant, repeated = True)
    
    
class Pick(ndb.Model):
    user_id = ndb.StringProperty()
    last_updated = ndb.DateTimeProperty(auto_now = True)
    prev_picks = ndb.KeyProperty(kind = Option, repeated = True)
    event = ndb.KeyProperty(kind = Event)
    pick = ndb.KeyProperty(kind = Option)



def submit_sample_games():
    ndb.put_multi([Option(id = "PHI", tri_code = "PHI"), Option(id = "WAS", tri_code = "WAS"), Option(id = "IND", tri_code = "IND"), Option(id = "CHI", tri_code = "CHI"), Option(id = "BKN", tri_code = "BKN"), Option(id = "DET", tri_code = "DET"), Option(id = "CHA", tri_code = "CHA"), Option(id = "BOS", tri_code = "BOS"), Option(id = "MEM", tri_code = "MEM"), Option(id = "ATL", tri_code = "ATL"), Option(id = "GSW", tri_code = "GSW"), Option(id = "SAC", tri_code = "SAC"), Option(id = "POR", tri_code = "POR"), Option(id = "PHX", tri_code = "PHX"), Option(id = "LAL", tri_code = "LAL"), Option(id = "DEN", tri_code = "DEN"), Option(id = "BOS", tri_code = "BOS"), Option(id = "CHA", tri_code = "CHA"), Option(id = "NYK", tri_code = "NYK"), Option(id = "CLE", tri_code = "CLE"), Option(id = "MIA", tri_code = "MIA"), Option(id = "MIN", tri_code = "MIN"), Option(id = "MIL", tri_code = "MIL"), Option(id = "DAL", tri_code = "DAL"), Option(id = "SAS" ,tri_code = "SAS")])

    ndb.put_multi([
    Event(id = "11600021", season = 2016, date = 20161006, options = [ndb.Key(Option, "PHI"), ndb.Key(Option, "WAS")], outcome = Outcome(scores = [119, 125], correct = ndb.Key(Option, "WAS"))),
    Event(id = "11600022", season = 2016, date = 20161006, options = [ndb.Key(Option, "IND"), ndb.Key(Option, "CHI")], outcome = Outcome(scores = [115, 108], correct = ndb.Key(Option, "IND"))),
    Event(id = "11600024", season = 2016, date = 20161006, options = [ndb.Key(Option, "BKN"), ndb.Key(Option, "DET")], outcome = Outcome(scores = [101, 94], correct = ndb.Key(Option, "DET"))),
    Event(id = "11600025", season = 2016, date = 20161006, options = [ndb.Key(Option, "CHA"), ndb.Key(Option, "BOS")], outcome = Outcome(scores = [92, 107], correct = ndb.Key(Option, "CHA"))),
    Event(id = "11600026", season = 2016, date = 20161006, options = [ndb.Key(Option, "GSW"), ndb.Key(Option, "SAC")], outcome = Outcome(scores = [105, 96], correct = ndb.Key(Option, "GSW"))),
    Event(id = "11600027", season = 2016, date = 20161007, options = [ndb.Key(Option, "POR"), ndb.Key(Option, "PHX")], outcome = Outcome(scores = [115, 110], correct = ndb.Key(Option, "POR"))),
    Event(id = "11600028", season = 2016, date = 20161007, options = [ndb.Key(Option, "LAL"), ndb.Key(Option, "DEN")], outcome = Outcome(scores = [97, 101], correct = ndb.Key(Option, "DEN"))),
    Event(id = "11600029", season = 2016, date = 20161008, options = [ndb.Key(Option, "BOS"), ndb.Key(Option, "CHA")]),
    Event(id = "11600031", season = 2016, date = 20161008, options = [ndb.Key(Option, "NYK"), ndb.Key(Option, "BKN")]),
    Event(id = "11600033", season = 2016, date = 20161008, options = [ndb.Key(Option, "CLE"), ndb.Key(Option, "PHI")]),
    Event(id = "11600030", season = 2016, date = 20161008, options = [ndb.Key(Option, "CHI"), ndb.Key(Option, "IND")]),
    Event(id = "11600032", season = 2016, date = 20161008, options = [ndb.Key(Option, "MIA"), ndb.Key(Option, "MIN")]),
    Event(id = "11600034", season = 2016, date = 20161008, options = [ndb.Key(Option, "MIL"), ndb.Key(Option, "DAL")]),
    Event(id = "11600035", season = 2016, date = 20161008, options = [ndb.Key(Option, "SAS"), ndb.Key(Option, "ATL")]),
    ])
    return
'''
# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        #now = datetime.datetime.now()
        #now = datetime.date.today()
        #curr_date = "{}{}{}".format(now.year, now.month, now.day)
        #curr_date = int(curr_date)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        curr_date = 20161007
        curr_games_qry = Event.query().filter(Event.date == curr_date)
        curr_games_raw = curr_games_qry.fetch()
        curr_games = []
        prev_games = []
        # Get picks by user
        #curr_picks_qry
            
        for curr_game in curr_games_raw:
            #curr_pick = Pick.query().filter(Pick.event.id() == curr_game.key.id())
            if user:
                curr_pick_qry = Pick.query().filter(Pick.user_id == user.user_id())
                curr_pick_qry = curr_pick_qry.filter(Pick.event == curr_game.key)
                print curr_pick_qry
                curr_pick = curr_pick_qry.fetch()
                print curr_pick
                if len(curr_pick) > 0:
                    curr_games.append({'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'away': curr_game.options[1].get().tri_code, 'date': curr_game.date, 'pick': curr_pick[0].pick.get().tri_code})
                else:
                    curr_games.append({'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'away': curr_game.options[1].get().tri_code, 'date': curr_game.date})
            else:
                curr_games.append({'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'away': curr_game.options[1].get().tri_code, 'date': curr_game.date})
        prev_games_qry = Event.query().filter(Event.date < curr_date)
        prev_games_raw = prev_games_qry.fetch()
        #if len(prev_games_raw) > 0:
         #   for prev_game in prev_games_raw:
          #      prev_games.append({'game_id': prev_game.key.id(), 'home': prev_game.options[0].get().tri_code, 'away': prev_game.options[1].get().tri_code, 'home_score': prev_game.outcome.scores[0], 'away_score': prev_game.outcome.scores[1]})



        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'curr_games': curr_games,
            'prev_games': prev_games,
            'curr_date': curr_date,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))
# [END main_page]


class MakePickHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        user_id = user.user_id()
        game_id = self.request.get("game_id")
        picked_team = self.request.get("picked_team")
        curr_pick_qry = Pick.query().filter(Pick.user_id == user.user_id())
        curr_pick_qry = curr_pick_qry.filter(Pick.event == ndb.Key("Event", str(game_id)))
        curr_pick = curr_pick_qry.fetch()
        if len(curr_pick) > 0:
            # do this
            curr_pick[0].pick = ndb.Key("Option", picked_team)
            curr_pick[0].last_updated = datetime.datetime.now()
            curr_pick[0].put()
        else:
            pick = Pick(user_id = user_id, event = ndb.Key("Event", str(game_id)), pick = ndb.Key("Option", picked_team)) # use team_id as key in future
            pick.put()
        #self.response.out.write("<p>{}</p>".format(user_id))
        #db = MySQLdb.connect(db = "c9", user = "tdliu")

        #db = get_db()
        #c = db.cursor()
        #c.execute("INSERT INTO raw_user_picks VALUES (NOW(), %s, %s, %s);", (user.user_id(), game_id, team_pick))
        #db.commit()
        curr_pick_qry = Pick.query().filter(Pick.user_id == user.user_id())
        curr_pick_qry = curr_pick_qry.filter(Pick.event == ndb.Key("Event", str(game_id)))
        curr_pick = curr_pick_qry.fetch() 
        # print curr_pick       
        self.redirect('/')

class PickHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        user_id = data['user_id']
        game_id = data['game_id']
        team = data['team']

<<<<<<< HEAD
class CronDbUpdate(webapp2.RequestHandler):
    def post(self):
        # do stuff
        #now = datetime.datetime.now()
        now = datetime.date.today()
        curr_date = "{}{}{}".format(now.year, now.month, now.day)
        curr_date = int(curr_date)        
        insert_curr_nba_games(curr_date)
        #update_nba_games(date)
=======
        # MAGIC
        # validate:
            #game has not started yet
            #team is a valid choice
            # etc.

        responseData = { 'success' : True }
        self.response.out.write(json.dumps(responseData))


# --------------------- HANDLERS TO IMPLEMENT --------------------
class GameHandler(webapp2.RequestHandler):
    def get(self):
        date = self.request.get('date')
        sport = self.request.get('sport')
        # MAGIC

        responseData = [
            {
                'time': "7:00pm",
                'game_id': "1",
                'home': "Patriots",
                'away': "Falcons",
                'current_pick' : "Patriots"
            },
            {
                'time': "9:00pm",
                'game_id': "2",
                'home': "Saints",
                'away': "Rams",
                'current_pick' : "null"
            },
            {
                'time': "10:00pm",
                'game_id': "4",
                'home': "Chargers",
                'away': "Dolphins",
                'current_pick' : "Chargers"
            },
        ]
        self.response.out.write(json.dumps(responseData))
>>>>>>> 8e4ef88fd101013f9c417894578dda4ffb6b937f

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/make_pick', MakePickHandler),
    ('/pick/', PickHandler),
<<<<<<< HEAD
    ('/db_update', CronDbUpdate)
=======
    ('/game/', GameHandler)
>>>>>>> 8e4ef88fd101013f9c417894578dda4ffb6b937f
], debug=True)
