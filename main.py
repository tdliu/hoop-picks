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
#from google.appengine.api import urlfetch

#import data_classes as dc
from myapp.models import Option, Outcome, Event, Pick, UserGoatIndex
#import db_update as db
import logging
import json
#from google.appengine.api import memcache

import jinja2
import webapp2
#from db.db_update import insert_nba_games
#from db.db_update import update_nba_games
#from db.db_update import recalculate_goat_index
#from db.db_update import insert_nfl_games
from myapp.views import *
#from db.urls import *
from myapp.db_handlers import *




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
        nba_team_query = Option.query().filter(Option.sport == "nba")
        nba_teams = nba_team_query.fetch()
        nba_team_records = {}
        for team in nba_teams:
            nba_team_records[team.key.id()] = [team.num_win, team.num_loss]
        nfl_team_query = Option.query().filter(Option.sport == "nfl")
        nfl_teams = nfl_team_query.fetch()
        nfl_team_records = {}
        for team in nfl_teams:
            nfl_team_records[team.key.id()] = [team.num_win, team.num_loss, team.num_draw]
        throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
        now = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).date()
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
            'nba_team_records': json.dumps(nba_team_records),
            'nfl_team_records': json.dumps(nfl_team_records),
            'logged_in' : logged_in
        }
        logging.info("HEY")
        logging.info(nfl_team_records)
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))
# [END main_page]

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/signin.html')
        self.response.write(template.render());

class PickHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        user_id = data['user_id']
        game_id = data['game_id']
        #sport = data['sport']
        sport = game_id[:3] # temporary solution
        team_id = data['team_id']
        #logging.info(user_id)
        # Check if game has started
        if (datetime.datetime.utcnow() > ndb.Key("Event", game_id).get().start_time): # we don't want the user to see the change
            responseData = { 'success' : False, 'message': "Pick submitted after start time." }
            self.response.out.write(json.dumps(responseData))
            return
        pick_id = user_id + game_id
        pick = Pick.get_or_insert(
            pick_id,
            sport = sport,
            user_id = user_id,
            event = ndb.Key("Event", game_id)
        )
        responseData = {
            'user_id': user_id,
            'game_id': game_id,
            'success' : True}
        # Is user making or removing pick.
        if team_id:
            pick.pick = ndb.Key("Option", team_id)
            pick.num_pick = pick.num_pick + 1
            responseData['team_id'] = team_id
        else:
            pick.pick = None
        #pick.score = []
        pick.put()
        self.response.out.write(json.dumps(responseData))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signin/', SignInHandler),
    ('/pick/', PickHandler),
    #('/db_update', CronDbUpdate),
    ('/live_game/', LiveGameHandler),
    ('/game/', GameHandler),
    ('/insert_nba_games/', InsertNBAGames),
    ('/insert_nfl_games/', InsertNFLGames),
    ('/cron/recalculate_goat_index/', RecalculateGoatIndex),
    ('/user_goat_index/', UserGoatIndexHandler),
    #('/update_schema/', UpdateSchemaHandler),
    ('/admin/update_all_nba_games/', UpdateAllNBAGames),
    ('/cron/update_nfl_games/', UpdateNFLGames),
    ('/cron/update_nba_games/', UpdateNBAGames),
    ('/cron/update_nba_team_records/', UpdateNBATeamRecords),
    ('/cron/update_nfl_team_records/', UpdateNFLTeamRecords),
    ('/admin/update_all_nfl_games/', UpdateAllNFLGames),
    ('/user/', UserHandler),
    ('/group/create/', GroupCreateHandler)
    #('/admin/temp_update_option_sport/', TempUpdateOptionSport)
], debug=True)
