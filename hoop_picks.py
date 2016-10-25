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

class Option(ndb.Model):
    abbrev_name = ndb.StringProperty()

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
    ndb.put_multi([Option(id = "PHI", abbrev_name = "PHI"), Option(id = "WAS", abbrev_name = "WAS"), Option(id = "IND", abbrev_name = "IND"), Option(id = "CHI", abbrev_name = "CHI"), Option(id = "BKN", abbrev_name = "BKN"), Option(id = "DET", abbrev_name = "DET"), Option(id = "CHA", abbrev_name = "CHA"), Option(id = "BOS", abbrev_name = "BOS"), Option(id = "MEM", abbrev_name = "MEM"), Option(id = "ATL", abbrev_name = "ATL"), Option(id = "GSW", abbrev_name = "GSW"), Option(id = "SAC", abbrev_name = "SAC"), Option(id = "POR", abbrev_name = "POR"), Option(id = "PHX", abbrev_name = "PHX"), Option(id = "LAL", abbrev_name = "LAL"), Option(id = "DEN", abbrev_name = "DEN"), Option(id = "BOS", abbrev_name = "BOS"), Option(id = "CHA", abbrev_name = "CHA"), Option(id = "NYK", abbrev_name = "NYK"), Option(id = "CLE", abbrev_name = "CLE"), Option(id = "MIA", abbrev_name = "MIA"), Option(id = "MIN", abbrev_name = "MIN"), Option(id = "MIL", abbrev_name = "MIL"), Option(id = "DAL", abbrev_name = "DAL"), Option(id = "SAS" ,abbrev_name = "SAS")])

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

        curr_date = 20161006
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
                    curr_games.append({'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().abbrev_name, 'away': curr_game.options[1].get().abbrev_name, 'date': curr_game.date, 'pick': curr_pick[0].pick.get().abbrev_name})
                else:
                    curr_games.append({'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().abbrev_name, 'away': curr_game.options[1].get().abbrev_name, 'date': curr_game.date})
            else:
                curr_games.append({'game_id': curr_game.key.id(), 'home': curr_game.options[0].get().abbrev_name, 'away': curr_game.options[1].get().abbrev_name, 'date': curr_game.date})
        prev_games_qry = Event.query().filter(Event.date < curr_date)
        prev_games_raw = prev_games_qry.fetch()
        for prev_game in prev_games_raw:
            prev_games.append({'game_id': prev_game.key.id(), 'home': prev_game.options[0].get().abbrev_name, 'away': prev_game.options[1].get().abbrev_name, 'date': curr_game.date, 'home_score': prev_game.outcome.scores[0], 'away_score': prev_game.outcome.scores[1]})
        #curr_game = curr_games[0]



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

'''
class Pick(ndb.Model):
    user_id = ndb.StringProperty()
    last_updated = ndb.DateTimeProperty(auto_now = True)
    event = ndb.KeyProperty(kind = Event)
    pick = ndb.KeyProperty(kind = Option)
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
# [START guestbook]
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]
'''

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/make_pick', MakePickHandler)
], debug=True)
# [END app]
