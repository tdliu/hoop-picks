function GoatDateNavigator(sport, section, date, prev, next, today, apiConnector, date_interval) {
	this._sport = sport;
	this._section_elem = section;
	this._date_elem = date;
	this._prev_button_elem = prev;
	this._next_button_elem = next;

	this._today = today;
	this._current_date = today;

	this._date_interval = date_interval;

	this._cardInjector = new CardInjector(this._section_elem, sport, apiConnector);

	var that = this;
	this._prev_button_elem.click(function() { that.previous(); })
  	this._next_button_elem.click(function() { that.next(); })

  	this.updateDateText([]);
}

GoatDateNavigator.prototype.initialGames = function(games) {
	this._cardInjector.addCardsToSection(games);
	this.updateDateText(games);
}

GoatDateNavigator.prototype.updateDateText = function(games) {
	if (this._sport == 'nba') {
		this._date_elem.html("" + this._current_date.getMonthDateAbbrev());	
	}
	else if (this._sport == 'nfl') {
		if (games.length > 0)
			this._date_elem.html("Week " + games[0].week);
		else this._date_elem.html("" + this._current_date.getMonthDateAbbrev());	
	}
	
}

GoatDateNavigator.prototype.next = function() {
	this._current_date = this._current_date.getOffset(this._date_interval);
	var that = this;
	this._cardInjector.getGamesAndInjectCards(this._current_date, function(games) {
		that.updateDateText(games);	
	});
	
}

GoatDateNavigator.prototype.previous = function() {
	this._current_date = this._current_date.getOffset(-1 * this._date_interval);
	var that = this;
	this._cardInjector.getGamesAndInjectCards(this._current_date, function(games) {
		that.updateDateText(games);
	});
	
}