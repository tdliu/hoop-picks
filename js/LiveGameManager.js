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
		console.log(data);
		if (callback) {
			callback(data);
		}
	});
	
}
