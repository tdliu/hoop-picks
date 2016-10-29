var apiConnector = {};
apiConnector.pick = function(game_id, team, callback) {
	$.ajax({
      type: "POST",
      url: "/pick/",
      dataType: 'json',
      data: JSON.stringify({ game_id: game_id, team: team})
    })
    .done(function( data ) {
        if (callback) {
        	callback(data);	
        }
    });
}

apiConnector.game = function(date, sport, callback) {
	$.ajax({
      type: "GET",
      url: "/game/?date=" + date,
      dataType: 'json'
    })
    .done(function( data ) {
    	callback(data);
    });
}