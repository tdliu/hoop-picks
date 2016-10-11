from google.appengine.api import urlfetch
import json

class GameInfo:
    def __init__(self, game_id, home, away, date):
        self.id = game_id
        self.home = home
        self.away = away
        self.date = date
        
        

def get_nba_daily_games(date):
    '''
    INPUT: date in YMD format
    OUTPUT: list of GameInfo objects
    '''
    #url = 'http://data.nba.net/data/10s/prod/v1/20161001/scoreboard.json'
    url = 'http://data.nba.net/data/10s/prod/v1/{}/scoreboard.json'.format(date)
    r = urlfetch.fetch(url)
    games = json.loads(r.content)['games']
    game_info = []
    for game in games:
        game_info.append(GameInfo(game['gameId'], game['hTeam']['triCode'], game['vTeam']['triCode'], date))
    return game_info
