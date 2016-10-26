from google.appengine.ext import ndb


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
    outcome = ndb.StructuredProperty(Outcome, default = Outcome())
    #participants = ndb.KeyProperty(kind = Participant, repeated = True)
    
    
class Pick(ndb.Model):
    user_id = ndb.StringProperty()
    last_updated = ndb.DateTimeProperty(auto_now = True)
    prev_picks = ndb.KeyProperty(kind = Option, repeated = True)
    event = ndb.KeyProperty(kind = Event)