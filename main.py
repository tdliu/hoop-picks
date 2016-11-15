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
from db.db_update import insert_nba_games
from db.db_update import update_nba_games
from db.db_update import recalculate_goat_index
from db.db_update import insert_nfl_games
from myapp.views import *
from db.urls import *




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
            'nba_team_records': nba_team_records,
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
        #sport = data['sport']
        sport = game_id[:3] # temporary solution
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
            pick = Pick(user_id = user_id, sport = sport, event = ndb.Key("Event", game_id), pick = ndb.Key("Option", team)) # use team_id as key in future
            pick.put()

        responseData = { 'success' : True }
        logging.info(team);
        self.response.out.write(json.dumps(responseData))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/pick/', PickHandler),
    #('/db_update', CronDbUpdate),
    ('/live_game/', LiveGameHandler),
    ('/game/', GameHandler),
    ('/admin/insert_nba_games/', InsertNBAGames),
    ('/admin/insert_nfl_games/', InsertNFLGames),
    ('/cron/recalculate_goat_index/', RecalculateGoatIndex),
    ('/user_goat_index/', UserGoatIndexHandler),
    #('/update_schema/', UpdateSchemaHandler),
    ('/admin/update_all_nba_games/', UpdateAllNBAGames),
    ('/cron/update_nfl_games/', UpdateNFLGames),
    ('/cron/update_nba_games/', UpdateNBAGames),
    ('/cron/update_nba_team_records/', UpdateNBATeamRecords),
    ('/cron/update_nfl_team_records/', UpdateNFLTeamRecords),
    ('/admin/update_all_nfl_games/', UpdateAllNFLGames)
    #('/admin/temp_update_option_sport/', TempUpdateOptionSport)
], debug=True)
