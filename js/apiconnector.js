//THIS ALSO SERVES AS THE GOAT FACTORY

function ApiConnector(today, team_records) {
  this.today = today;
  this.team_records = team_records;
  console.log(team_records)
}

ApiConnector.prototype.user_goat_index = function(sport, callback) {
  $.ajax({
      type: "GET",
      url: "/user_goat_index/" + "?sport=" + sport,
      dataType: 'json',
    })
    .done(function( data ) {
        if (callback) {
          callback(data);
        }
    });
}

ApiConnector.prototype.pick = function(game_id, team, sport, callback) {
  console.log("sending pick: ", game_id, team)
	$.ajax({
      type: "POST",
      url: "/pick/",
      dataType: 'json',
      data: JSON.stringify({ game_id: game_id, team: team, sport: sport})
    })
    .done(function( data ) {
        if (callback) {
        	callback(data);
        }
    });
}

ApiConnector.prototype.game = function(date, sport, callback) {
	$.ajax({
      type: "GET",
      url: "/game/?date=" + date + "&sport=" + sport,
      dataType: 'json'
    })
    .done(function( data ) {
    	if (callback)
        callback(data);
    });
}

ApiConnector.prototype.livegame = function(callback) {
  $.ajax({
      type: "GET",
      url: "/live_game/",
      dataType: 'json'
    })
    .done(function( data ) {
      console.log("livegame", data);
      if (callback)
        callback(data);
    });
}

ApiConnector.prototype.getNBAGames = function(game_date, callback) {
  var that = this;
  this.game(game_date.getDateString(), "nba", function(data) {
    var games = that.createNBAGames(game_date, data);
    
    if (callback) {
      callback(games);
    }
  });
}

ApiConnector.prototype.getNFLGames = function(game_date, callback) {
  console.log("getting nfl games")
  var that = this;
  this.game(game_date.getDateString(), "nfl", function(data) {
    var games = that.createNFLGames(game_date, data);
    if (callback) {
      callback(games);
    }
  });
}

// ------------------ GOAT GAME FACTORIES --------------//
ApiConnector.prototype.createNBAGames = function(game_date, games) {
  var goatGames = [];
  for (var i = 0; i < games.length; i ++) {
    var game = new GoatGame(this.today, game_date, games[i], this.team_records.nba);
    goatGames.push(game);
  }
  return goatGames;
}

ApiConnector.prototype.createNFLGames = function(game_date, games) {
  var goatGames = [];
  for (var i = 0; i < games.length; i ++) {
    var game = new GoatGame(this.today, game_date, games[i], this.team_records.nfl);
    goatGames.push(game);
  }
  return goatGames;

}