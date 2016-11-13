#!/usr/bin/env python
from db_update import *
from google.appengine.api import users
import datetime
import logging
import webapp2


class InsertNBAGames(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                self.response.write('You are an administrator.')
                insert_nba_games(datetime.date(2016,10,29))
                #insert_nba_games(datetime.date.today())
                logging.info("Inserting NBA games.")
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')
        
        
class InsertNFLGames(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			if users.is_current_user_admin():
				self.response.write('You are an administrator.\nInserting NFL games.')
				insert_nfl_games()
			else:
				self.response.write('You are not an administrator.')
		else:
			self.response.write('You are not logged in.')

class UpdateNBAGames(webapp2.RequestHandler):
    def get(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        logging.info("HELLO")
        logging.info(date)
        #curr_date = datetime.date(2016,10,29)
        update_nba_games(date)
        logging.info("Updating NBA games for {}".format(date))

class RecalculateGoatIndex(webapp2.RequestHandler):
    def get(self):
        recalculate_goat_index("nba")
  