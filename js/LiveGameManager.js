function LiveGameManager(apiConnector) {
	this._apiConnector = apiConnector;
	this._games = {};
}

LiveGameManager.prototype.registerGame = function(game) {
	this._games[game.game_id] = game;
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
