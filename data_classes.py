from google.appengine.ext import ndb
import math


class Option(ndb.Model):
    tri_code = ndb.StringProperty()

class Outcome(ndb.Model):
    scores = ndb.IntegerProperty(repeated = True)
    #home_score = ndb.IntegerProperty()
    #away_score = ndb.IntegerProperty()
    winner = ndb.KeyProperty(kind = Option)
    

class Event(ndb.Model):
    sport = ndb.StringProperty()
    #gameId = ndb.IntegerProperty()
    season = ndb.IntegerProperty()
    date = ndb.DateProperty()
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
    num_change = ndb.IntegerProperty(default = 0)

class UserGoatIndex(ndb.Model):
    user_id = ndb.StringProperty()
    sport = ndb.StringProperty()
    num_pick = ndb.IntegerProperty()
    num_point = ndb.IntegerProperty()
    num_correct = ndb.IntegerProperty()
    accuracy = ndb.ComputedProperty(lambda self: self.__accuracy())
    #goat_index = ndb.ComputedProperty(lambda self: self._goat_index())

    @property
    def __accuracy(self):
        if self.num_picks > 0:
            return self.num_correct/self.num_pick
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


