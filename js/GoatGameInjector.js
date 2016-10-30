// TODAY SECTIONS
//		Started: today_started_section
//		Upcoming: today_upcoming_section
// UPCOMING SECTIOn
//		Upcoming: upcoming_section


function GoatGameInjector(today_started_section, today_upcoming_section, upcoming_section) {
	this._today_started_section = today_started_section;
	this._today_upcoming_section = today_upcoming_section;
	this._upcoming_section = upcoming_section;

	this._today_game_info_received = false;
	this._today_live_game_data_received = false;
}

GoatGameInjector.prototype.todayGameInfo = function(today_games) {
	this._today_games = today_games;
	this._today_game_info_received = true;
	if (this._today_live_game_data_received) {
		this.joinTodayGamesAndInject();
	}
}

GoatGameInjector.prototype.todayLiveGameData = function(live_game_data) {
	this._today_live_game_data = live_game_data;
	this._today_live_game_data_received = true;
	if (this._today_game_info_received) {
		this.joinTodayGamesAndInject();
	}
}

GoatGameInjector.prototype.upcomingGameData = function(future_games_data) {
	var goatGames = this.goatGameFactory(future_games_data, false);
	this.addGamesToSection(this._upcoming_section, goatGames['upcoming']);
}

GoatGameInjector.prototype.joinTodayGamesAndInject = function() {
	var joined = this._today_games; // TODO
	for (var i = 0; i < this._today_live_game_data.length; i++) {
		live_datum = this._today_live_game_data[i];
		game_id = "nba" + live_datum['gameId'];

		for (var j = 0; j < joined.length; j++) {
			if (joined[j].game_id == game_id) {
				joined[j].live_data = live_datum;
				joined[j].has_live_data = true;
			}
		}
	}

	var goatGames = this.goatGameFactory(joined, true);
	this.addGamesToSection(this._today_started_section, goatGames['started'])
	this.addGamesToSection(this._today_upcoming_section, goatGames['upcoming'])
}

GoatGameInjector.prototype.goatGameFactory = function(games, is_today) {
	var goatGames = { 'started' : [], 'upcoming' : []};
	for (var i = 0; i < games.length; i ++) {
		games[i].is_today = is_today;
		if (i == games.length - 1) {
		  games[i].isLast = true;
		}

		var game = new GoatGame(games[i]);
		if (game.hasStarted()) {
			goatGames['started'].push(game);
		}
		else {
			goatGames['upcoming'].push(game);	
		}
	}
	if (goatGames['started'].length > 0) goatGames['started'][goatGames['started'].length - 1].setLast();
	if (goatGames['upcoming'].length > 0) goatGames['upcoming'][goatGames['upcoming'].length - 1].setLast();
	return goatGames;
}

GoatGameInjector.prototype.addGamesToSection = function(section, goatGames) {
	for (var i = 0; i < goatGames.length; i ++) {
		var goatGame = goatGames[i];
		section.append(goatGame.elem);
	}

	section.animate(
		{'opacity': 1},
		1000)
}