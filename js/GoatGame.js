var pick_card_source = $("#pick-card-template").html();
var live_pick_card_source = $("#live-pick-card-template").html();

var pick_card_template = Handlebars.compile(pick_card_source);
var live_pick_card_template = Handlebars.compile(live_pick_card_source);

// ------------------ UTILS ------------------------//
function hasStarted(start_time) {
	var current_time_eastern = getCurrentTimeEastern();
	return start_time.getDifferenceHours(current_time_eastern) > 0;
}

// ------------------ CLASS GOAT GAME --------------//
function GoatGame(game) {
	for (var attr in game) {
        if (game.hasOwnProperty(attr)) this[attr] = game[attr];
    }

	this.start_time = new GoatTime(game.time);
	this.pretty_start_time = this.start_time.getPrettyTime();

	this.awayPicked = (game.current_pick == game.away);
    this.homePicked = (game.current_pick == game.home);

    //use live game data
    if (game.is_today) {
    	this.started = hasStarted(this.start_time);
    }
    else {
    	this.started = false;
    }

    if (this.started === true) {
		this.live_data.live_clock = this.formatLiveClock();
		this.elem = $(live_pick_card_template(this));
		liveGameManager.registerGame(this);  	
    }
    else {
    	this.elem = $(pick_card_template(this));	
    	this.setPickable(logged_in);
    }
}

GoatGame.prototype.hasStarted = function() {
	return this.started;
}

GoatGame.prototype.setPickable = function(logged) {
	if (logged) 
		this.addPickListeners();
	else
		this.addLoginListeners();
    this.getHomeElem().addClass('pickable')
    this.getAwayElem().addClass('pickable')
}

GoatGame.prototype.addLoginListeners = function() {
	var that = this;
	this.getHomeElem().click(function() {
		alert("Login!")
	})
	this.getAwayElem().click(function() {
		alert("Login!")
	})
}

GoatGame.prototype.addPickListeners = function() {
	var that = this;
	this.getHomeElem().click(function() {
	    $(this).addClass("picked")
	    $(this).parent().find(".away").removeClass("picked")
	    apiConnector.pick(that.game_id, that.home_id)
	})
  
	this.getAwayElem().click(function() {
		$(this).addClass("picked")
		$(this).parent().find(".home").removeClass("picked")
		apiConnector.pick(that.game_id, that.away_id)
	})
}

GoatGame.prototype.liveUpdate = function(the_live_data) {
	this.live_data = the_live_data;
	this.live_data.live_clock = this.formatLiveClock();

	var newelem = $(live_pick_card_template(this))
	this.elem.replaceWith(newelem);
	this.elem = newelem;
}

GoatGame.prototype.getAwayElem = function() {
	return this.elem.find('.away');
}

GoatGame.prototype.getHomeElem = function() {
	return this.elem.find('.home');
}

GoatGame.prototype.getPickElem = function() {
	return this.elem.find("#" + this.game_id );
}

GoatGame.prototype.formatLiveClock = function() {
	var live_clock = this.live_data.clock;
	live_clock += " - ";
	if (this.live_data.period.current == 1)
		live_clock += "1st";
	else if (this.live_data.period.current == 2)
		live_clock += "2nd";
	else if (this.live_data.period.current == 3)
		live_clock += "3rd";
	else if (this.live_data.period.current == 4)
		live_clock += "4th";

	return live_clock;
}