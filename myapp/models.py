from google.appengine.ext import ndb
import math

class Group(ndb.Model):
    # Set group name as key.
    sport = ndb.StringProperty()
    creator = ndb.StringProperty()
    password = ndb.StringProperty()
    password_required = ndb.BooleanProperty(default = False)
    users = ndb.StringProperty(repeated = True)
    public = ndb.BooleanProperty(default = True)


class User(ndb.Model):
    # Set user_id as key.
    #user_id = ndb.StringProperty()
    groups = ndb.KeyProperty(kind = Group, repeated = True)

class Option(ndb.Model):
    tri_code = ndb.StringProperty()
    sport = ndb.StringProperty()
    #abbrev = ndb.StringProperty()
    city = ndb.StringProperty()
    nickname = ndb.StringProperty()
    num_win = ndb.IntegerProperty(default = 0)
    num_loss = ndb.IntegerProperty(default = 0)
    num_draw = ndb.IntegerProperty(default = 0)

class Outcome(ndb.Model):
    scores = ndb.IntegerProperty(repeated = True)
    #home_score = ndb.IntegerProperty()
    #away_score = ndb.IntegerProperty()
    winner = ndb.KeyProperty(kind = Option)
    

class Event(ndb.Model):
    sport = ndb.StringProperty()
    #gameId = ndb.IntegerProperty()
    season = ndb.IntegerProperty()
    event_type = ndb.StringProperty()
    date = ndb.DateProperty()
    week = ndb.IntegerProperty() # NFL
    options = ndb.KeyProperty(kind = Option, repeated = True) # Use participant generated ID
    #away = ndb.KeyProperty(kind = Option)
    outcome = ndb.StructuredProperty(Outcome, default = Outcome())
    start_time = ndb.DateTimeProperty()
    #participants = ndb.KeyProperty(kind = Participant, repeated = True)
    

    
class Pick(ndb.Model):
    user_id = ndb.StringProperty()
    sport = ndb.StringProperty()
    last_updated = ndb.DateTimeProperty(auto_now = True)
    prev_picks = ndb.KeyProperty(kind = Option, repeated = True)
    event = ndb.KeyProperty(kind = Event)
    pick = ndb.KeyProperty(kind = Option)
    num_pick = ndb.IntegerProperty(default = 0)

class UserGoatIndex(ndb.Model):
    user_id = ndb.StringProperty()
    sport = ndb.StringProperty()
    num_pick = ndb.IntegerProperty()
    num_point = ndb.IntegerProperty()
    num_correct = ndb.IntegerProperty()
    accuracy = ndb.ComputedProperty(lambda self: self._accuracy())
    rank = ndb.IntegerProperty()
    #goat_index = ndb.ComputedProperty(lambda self: self._goat_index())
    def _accuracy(self):
        if self.num_pick > 0:
            return float(self.num_correct)/float(self.num_pick)
        else:
            return 0

'''
    @property
    def _goat_index(self):
        P = .5
        Q = 20
        if self.num_pick == 0:
            return 0
        return P*(self.num_point/self.num_pick)*10 + 10*(1-P)*(1-math.exp(-self.num_pick/Q))
'''


'''

class League(ndb.Model):
    # content['data']['dates'][0]['fixtures'][1]['league']
    abbreviation = ndb.StringProperty()
    name = ndb.StringProperty()

class EventType(ndb.Model):
    event_id = ndb.StringProperty()
    name = ndb.StringProperty()

class State(ndb.Model):
    abbreviation = ndb.StringProperty()
    name = ndb.StringProperty()

class Country(ndb.Model):
    abbreviation = ndb.StringProperty()
    name = ndb.StringProperty()

class Venue(ndb.Model):
    # content['data']['dates'][0]['fixtures'][1]['venue']
    city = ndb.StringProperty()
    state = ndb.StructuredProperty(State)
    name = ndb.StringProperty()

class Team(ndb.Model):
    name = ndb.StringProperty()
    title = ndb.StringProperty()
    is_winner = ndb.BooleanProperty()
    abbreviation = ndb.StringProperty()
    score = ndb.IntegerProperty()
    team_id = ndb.IntegerProperty()

# content['data']['dates'][0]['fixtures'][1]['teams'][0]['logo']

class Record(ndb.Model):
    wins = ndb.IntegerProperty()
    losses = ndb.IntegerProperty()

class StartTime(ndb.Model):
    utc = ndb.DateTimeProperty()
    local = ndb.DateTimeProperty()

class Fixture(ndb.Model):
    league = ndb.StructuredProperty(League)
    event_type = ndb.StructuredProperty(EventType)
    teams = ndb.StructuredProperty(Team, repeated = True)
    # key content['data']['dates'][0]['fixtures'][1]['id']
'''


