var pick_card_source = $("#pick-card-template").html();
var live_pick_card_source = $("#live-pick-card-template").html();
var completed_card_source = $("#completed-card-template").html();


var pick_card_template = Handlebars.compile(pick_card_source);
var live_pick_card_template = Handlebars.compile(live_pick_card_source);
var completed_card_template = Handlebars.compile(completed_card_source);

// ------------------ UTILS ------------------------//
function hasStarted(start_time) {
	var current_time_eastern = getCurrentTimeEastern();
	return start_time.isAfter(current_time_eastern);
}

// ------------------ CLASS GOAT GAME --------------//
function GoatGame(today, game_date, game, team_records) {
	//copy all the attributes
	for (var attr in game) {
        if (game.hasOwnProperty(attr)) this[attr] = game[attr];
    }

    if (game.date) {
    	this.date = new GoatDate(game.date);
    }
    else {
    	this.date = game_date;
    }

	this.start_time = new GoatTime(game.time);
	this.pretty_start_time = this.start_time.getPrettyTime();

	this.awayPicked = (game.current_pick == game.away);
    this.homePicked = (game.current_pick == game.home);

    if (team_records) {
    	this.homeRecord = team_records[this.home_id];
    	this.awayRecord = team_records[this.away_id];
    }

    var difference_days = this.date.differenceInDays(today);

    if (difference_days === 0) { // this game is today
    	this.started = hasStarted(this.start_time);
    	if (this.started) {
    		this.constructLiveGame();
    	}
    	else {	//this game is today but hasn't started
			this.constructUpcomingGame();
    	}
    }
    else if (difference_days == -1 && isEarlyMorning()) {
    	this.constructLiveGame();
    }
    else if (difference_days < 0) { //this game is in the past
    	this.constructCompletedGame();
    }
    else if (difference_days > 0) { //this game is in the future
    	this.constructUpcomingGame();
    }

    console.log("status: ", this.status)
}

GoatGame.prototype.constructCompletedGame = function() {
	this.status = 'completed';
	if (this.scores) {
		this.homeWon = (this.scores[0] - this.scores[1] > 0);
		this.awayWon = !this.homeWon;
		this.correct = (this.homeWon && this.homePicked) || (this.awayWon && this.awayPicked);	
	}
	
	if (!this.current_pick) {
		this.correctness = ""
	}
	else if (this.correct) {
		this.correctness = "correct";
	}
	else {
		this.correctness = "incorrect";
	}
	console.log(this.correctness)
    this.elem = $(completed_card_template(this));
}

GoatGame.prototype.constructLiveGame = function() {
	this.status = 'live';
	this.elem = $(live_pick_card_template(this));
}

GoatGame.prototype.constructUpcomingGame = function() {
	this.status = 'upcoming';
    this.elem = $(pick_card_template(this));	
    this.setPickable(logged_in);
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
	    $(this).find(".pick-checkbox").addClass("picked")
	    $(this).parent().find(".away").find(".pick-checkbox").removeClass("picked")
	    apiConnector.pick(that.game_id, that.home_id, that.sport);
	})
  
	this.getAwayElem().click(function() {
		$(this).find(".pick-checkbox").addClass("picked")
		$(this).parent().find(".home").find(".pick-checkbox").removeClass("picked")
		apiConnector.pick(that.game_id, that.away_id, that.sport);
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
	if (!this.live_data.isGameActivated) {
		return "final";
	}
	else if (this.live_data.period.isHalftime) {
		return "halftime";
	}
	var live_clock = this.live_data.clock;

	if (!live_clock) {
		return this.pretty_start_time;
	}
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