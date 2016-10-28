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
import db_update as db
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


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        #now = datetime.datetime.now()
        #now = datetime.date.today()
        #curr_date = "{}{}{}".format(now.year, now.month, now.day)
        #curr_date = int(curr_date)
        curr_date = datetime.date(2016,10,25)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        '''
        curr_date = datetime.date(2016,10,25)
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

        '''

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'curr_date': curr_date,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))
# [END main_page]

'''
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
'''

class PickHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        user_id = user.user_id()
        data = json.loads(self.request.body)
        game_id = data['game_id']
        team = data['team']
        print "hi" + team
        # MAGIC
        # validate:
            #game has not started yet
            #team is a valid choice
            # etc.
        # use get_or_insert instead
        curr_pick_qry = Pick.query().filter(Pick.user_id == user.user_id())
        curr_pick_qry = curr_pick_qry.filter(Pick.event == ndb.Key("Event", game_id))
        curr_pick = curr_pick_qry.fetch()
        if len(curr_pick) > 0:
            # do this
            curr_pick[0].pick = ndb.Key("Option", team)
            curr_pick[0].last_updated = datetime.datetime.now()
            curr_pick[0].put()
        else:
            pick = Pick(user_id = user_id, event = ndb.Key("Event", game_id), pick = ndb.Key("Option", team)) # use team_id as key in future
            pick.put()

        responseData = { 'success' : True }
        logging.info(team);
        self.response.out.write(json.dumps(responseData))

class CronDbUpdate(webapp2.RequestHandler):
    def post(self):
        # do stuff
        #now = datetime.datetime.now()
        now = datetime.date.today()
        curr_date = "{}{}{}".format(now.year, now.month, now.day)
        curr_date = int(curr_date)        
        insert_curr_nba_games(curr_date)
        #update_nba_games(date)



# --------------------- HANDLERS TO IMPLEMENT --------------------
class GameHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        curr_date = self.request.get('date')
        curr_date = datetime.date(2016,10,30)
        sport = self.request.get('sport')
        curr_games_qry = Event.query().filter(Event.date == curr_date)
        curr_games_raw = curr_games_qry.fetch()
        responseData = []
        for curr_game in curr_games_raw:
            #curr_pick = Pick.query().filter(Pick.event.id() == curr_game.key.id())
            start_time = curr_game.start_time.strftime("%H:%M:%S")
            if user:
                curr_pick_qry = Pick.query().filter(Pick.user_id == user.user_id())
                curr_pick_qry = curr_pick_qry.filter(Pick.event == curr_game.key)
                #print curr_pick_qry
                curr_pick = curr_pick_qry.fetch()
                print curr_pick
                if len(curr_pick) > 0:
                    responseData.append({'time': start_time, 'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'home_id': curr_game.options[0].id(), 'away': curr_game.options[1].get().tri_code, 'away_id': curr_game.options[1].id(), 'current_pick': curr_pick[0].pick.get().tri_code})
                else:
                    responseData.append({'time': start_time, 'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'home_id': curr_game.options[0].id(), 'away': curr_game.options[1].get().tri_code, 'away_id': curr_game.options[1].id()})
            else:
                responseData.append({'time': start_time, 'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().tri_code, 'home_id': curr_game.options[0].id(), 'away': curr_game.options[1].get().tri_code, 'away_id': curr_game.options[1].id()})
        # MAGIC
        '''
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
        '''
        self.response.out.write(json.dumps(responseData))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    #('/make_pick', MakePickHandler),
    ('/pick/', PickHandler),
    ('/db_update', CronDbUpdate),
    ('/game/', GameHandler)
], debug=True)
