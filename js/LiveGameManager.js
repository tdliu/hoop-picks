
// cousin of card injector
function LiveGameManager(apiConnector, section, sports) {
	this._apiConnector = apiConnector;
	this._games = {};
	this._section = section;
	this._sports = sports;

}

//checks to see if each game is 'live', and if it is, adds it
LiveGameManager.prototype.maybeRegisterGames = function(games) {
	for (var i = 0; i < games.length; i++) {
		var game = games[i];
		if (game.status == 'live') {
			this.registerGame(game);
		}
	}
}

LiveGameManager.prototype.registerGame = function(game) {
	this._games[game.game_id] = game;
	this._section.append(game.elem);
}

LiveGameManager.prototype.poll = function(callback) {
	var that = this;
	this._apiConnector.livegame(function(data) {

		for (var i = 0; i < data.length; i++) {
			var id = "nba" + data[i].gameId;
			if (that._games[id]) {
				that._games[id].liveUpdate(data[i])
			}
		}

		if (callback) {
			callback(data);
		}
	});
	
}
