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
from google.appengine.api import urlfetch

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
        now = (datetime.datetime.utcnow() - datetime.timedelta(hours = 4)).date()
        curr_date = "{}{}{}".format(now.year, now.month, now.day)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            logged_in = True
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            logged_in = False

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'curr_date': curr_date,
            'logged_in' : logged_in
        }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))
# [END main_page]


class PickHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        user_id = user.user_id()
        data = json.loads(self.request.body)
        game_id = data['game_id']
        team = data['team']
        if (datetime.datetime.utcnow() > ndb.Key("Event", game_id).get().start_time): # we don't want the user to see the change
            responseData = { 'success' : False, 'message': "Pick submitted after start time." }
            self.response.out.write(json.dumps(responseData))
            return
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
            curr_pick[0].num_change = curr_pick[0].num_change + 1
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
        curr_date = datetime.datetime.strptime(self.request.get('date'), "%Y%m%d")
        #if curr_date is None:
        #curr_date = (datetime.datetime.utcnow() - datetime.timedelta(hours = 4)).date()
        sport = self.request.get('sport')
        curr_games_qry = Event.query().filter(Event.date == curr_date)
        curr_games_raw = curr_games_qry.fetch()
        responseData = []
        for curr_game in curr_games_raw:
            #curr_pick = Pick.query().filter(Pick.event.id() == curr_game.key.id())
            start_time = curr_game.start_time - datetime.timedelta(hours = 4) # to ET
            start_time = start_time.strftime("%H:%M:%S")
            winner = curr_game.outcome.winner
            if winner is not None:
                winner = winner.id()
            game_data = {
                            'time': start_time, 
                            'game_id': curr_game.key.id(), 
                            'home': curr_game.options[0].get().tri_code, 
                            'home_id': curr_game.options[0].id(), 
                            'away': curr_game.options[1].get().tri_code, 
                            'away_id': curr_game.options[1].id(), 
                            'winner': winner}
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
        logging.info("HELLO")
        curr_ts = datetime.datetime.utcnow()
        if (curr_ts - last_polled_ts).total_seconds() > 10 or current_live_data is None:
            # poll new
            curr_date_str = datetime.datetime.strftime((curr_ts - datetime.timedelta(hours = 4)), "%Y%m%d")
            url =  "http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json".format(curr_date_str)
            #import json
            r = urlfetch.fetch(url)
            current_live_data = json.loads(r.content)['games']
            self.response.out.write(json.dumps(current_live_data))
            last_polled_ts = curr_ts
        else:
            self.response.out.write(json.dumps(current_live_data))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/pick/', PickHandler),
    ('/db_update', CronDbUpdate),
    ('/live_game/', LiveGameHandler),
    ('/game/', GameHandler)
], debug=True)
