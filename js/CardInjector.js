// give this a section, a sport, and an apiconnector
// 

function CardInjector(section, sport, apiconnector) {
	this._section = section;
	this._sport = sport;
	this._apiconnector = apiconnector;
}

CardInjector.prototype.getGamesAndInjectCards = function(time_key, callback) {
	var that = this;
	if (this._sport == 'nba') {
		this._apiconnector.getNBAGames(time_key, function(games) {
			that.clearSection();
			that.addCardsToSection(games);
			if (callback) {
				callback(games);
			}

		})
	}
	else if (this._sport == 'nfl') {
		this._apiconnector.getNFLGames(time_key, function(games) {
			that.clearSection();
			that.addCardsToSection(games);
			if (callback) {
				callback(games);
			}
		})	
	}
}

CardInjector.prototype.clearSection = function() {
	this._section.html("");
}

CardInjector.prototype.addInjectData = function(data) {
	var games = this.constructGoatGames(data);
	this.addCardsToSection(games);
}

CardInjector.prototype.addCardsToSection = function(cards) {
	for (var i = 0; i < cards.length; i ++) {
		var goatGame = cards[i];
		if (goatGame.status != 'live') {
			this._section.append(goatGame.elem);
		}
	}

	this._section.animate(
		{'opacity': 1},
		1000)
}