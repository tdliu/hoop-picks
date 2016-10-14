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
#import schedule

from google.appengine.api import users
import MySQLdb

import jinja2
import webapp2

CLOUDSQL_PROJECT = 'hoop-picks'
CLOUDSQL_INSTANCE = 'chris-bosh'

def get_db():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        db = MySQLdb.connect(
            unix_socket='/cloudsql/{}:{}'.format(
                CLOUDSQL_PROJECT,
                CLOUDSQL_INSTANCE),
            user='root')
    else:
        print "hi"
        db = MySQLdb.connect(db = "c9", user = "tdliu")
    return db
    
db = MySQLdb.connect(db = "c9", user = "tdliu")
c = db.cursor()
'''
class GameInfo:
    def __init__(self, game_id, home, away, date, home_score, away_score):
        self.id = game_id
        self.home = home
        self.away = away
        self.date = date
        self.home_score = home_score
        self.away_score = away_score
'''

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

#db = MySQLdb.connect(db = "c9", user = "tdliu")

#c = db.cursor()



# We want to construct a Datastore key for a user?


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        curr_date = 20161008
        #nba_games = schedule.get_nba_daily_games(curr_date)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        db = get_db()
        #db = MySQLdb.connect(db = "c9", user = "tdliu")
        c = db.cursor()
        curr_games = []
        prev_games = []
        curr_picks = [] 
        if user:
            user_id = user.user_id()
            c.execute("""
                SELECT a.game_id, home, away, date, team_pick, home_score, away_score, winner FROM 
                (SELECT * FROM games WHERE date > %s) a
                LEFT JOIN 
                (SELECT x.* FROM raw_user_picks x
                JOIN
                (SELECT user_id, game_id, max(created_ts) as created_ts FROM raw_user_picks GROUP BY user_id, game_id) y
                ON x.user_id = y.user_id AND x.game_id = y.game_id AND x.created_ts = y.created_ts
                WHERE x.user_id = %s and x.team_pick != '') b
                ON a.game_id = b.game_id
                ORDER BY a.game_id DESC;
            """, (curr_date - 3, user_id))
            for (game_id, home, away, date, team_pick, home_score, away_score, winner) in c.fetchall():
                if date < curr_date:
                    prev_games.append({'game_id': game_id, 'home': home, 'away': away, 'date': date, 'team_pick': team_pick, 'home_score': home_score, 'away_score': away_score, 'winner': winner})
                else:
                    curr_games.append({'game_id': game_id, 'home': home, 'away': away, 'date': date, 'team_pick': team_pick})
            
        template_values = {
            'user': user,
            #'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'curr_games': curr_games,
            'prev_games': prev_games,
            'curr_date': curr_date,
            'curr_picks': curr_picks
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        

# [END main_page]

class MakePickHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        user_id = user.user_id()
        game_id = self.request.get("game_id")
        team_pick = self.request.get("picked_team")
        #self.response.out.write("<p>{}</p>".format(user_id))
        #db = MySQLdb.connect(db = "c9", user = "tdliu")

        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO raw_user_picks VALUES (NOW(), %s, %s, %s);", (user.user_id(), game_id, team_pick))
        db.commit()
        self.redirect('/')


# have a get_db() function


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/make_pick', MakePickHandler)
    
    #('/sign', Guestbook),
], debug=True)
# [END app]

# Equivalent of guestbook is all nba games