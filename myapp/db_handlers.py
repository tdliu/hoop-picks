#!/usr/bin/env python
from db.db_update import *
from google.appengine.api import users
import datetime
import logging
import webapp2
from constants import admin_users


'''
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
'''

class InsertNBAGames(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id', default_value = None)
        if user_id:
            if user_id in admin_users:
                self.response.write('You are an administrator. Inserting NBA games')
                insert_nba_games(datetime.date(2016,10,29))
                logging.info("Inserted NBA games.")
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')

class InsertNFLGames(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id', default_value = None)
        if user_id:
            if user_id in admin_users:
                self.response.write('You are an administrator. Inserting NFL games.')
                insert_nfl_games()
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')

        
'''        
class InsertNFLGames(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			if users.is_current_user_admin():
				self.response.write('You are an administrator. Inserting NFL games.')
				insert_nfl_games()
			else:
				self.response.write('You are not an administrator.')
		else:
			self.response.write('You are not logged in.')
'''


class UpdateNBAGames(webapp2.RequestHandler):
    def get(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        #logging.info("HELLO")
        #logging.info(date)
        #curr_date = datetime.date(2016,10,29)
        update_nba_games(date)
        logging.info("Updating NBA games for {}.".format(date))

class UpdateAllNBAGames(webapp2.RequestHandler):
    def get(self):
        start_date = datetime.date(2016,11,03)
        curr_date = start_date
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        while curr_date <= end_date:
            update_nba_games(curr_date)
            curr_date = curr_date + datetime.timedelta(days=1)
        logging.info("Updating NBA games from {} to {}.".format(start_date, end_date))

class UpdateNFLGames(webapp2.RequestHandler):
    def get(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        update_nfl_games(date)
        logging.info("Updating NFL games for {}".format(date))

class UpdateAllNFLGames(webapp2.RequestHandler):
    def get(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        update_all_nfl_games(date)
        logging.info("Updating all NFL games up to {}".format(date))

class RecalculateGoatIndex(webapp2.RequestHandler):
    def get(self):
        recalculate_goat_index("nba")
        recalculate_goat_index("nfl")
        update_goat_index_rankings("nba")
        update_goat_index_rankings("nfl")

class UpdateNBATeamRecords(webapp2.RequestHandler):
    def get(self):
        update_nba_team_records()
        logging.info("Updating NBA team records.")

class UpdateNFLTeamRecords(webapp2.RequestHandler):
    def get(self):
        update_nfl_team_records()
        logging.info("Updating NFL team records.")

class TempUpdateOptionSport(webapp2.RequestHandler):
    def get(self):
        update_option_sport_attrib()
  