var pick_card_source = $("#pick-card-template").html();
var pick_card_template = Handlebars.compile(pick_card_source);

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

    this.elem = $(pick_card_template(this));

    if (this.started === false) {
    	this.setPickable(logged_in);
    }
    else if (this.started === true) {
    	this.getPickElem().addClass("live")
    }

    if (this.awayPicked) {
    	this.getAwayElem().addClass("picked");
    }
    else if (this.homePicked) {
    	this.getHomeElem().addClass("picked");	
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

GoatGame.prototype.getAwayElem = function() {
	return this.elem.find('.away');
}

GoatGame.prototype.getHomeElem = function() {
	return this.elem.find('.home');
}

GoatGame.prototype.getPickElem = function() {
	return this.elem.find("#" + this.game_id );
}