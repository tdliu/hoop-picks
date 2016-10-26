function getGamesByDate(date, user, callback) {
  $.ajax({
  	type: "POST",
  	url: "/game/",
  	dataType: 'json',
  	data: JSON.stringify({ "date" : date, "user": user})
  })
  .
  done(function(data) {
  	callback(data);
  });
}

function sendPick(game_id, team, callback) {
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


function game(date, sport, callback) {
	$.ajax({
      type: "GET",
      url: "/game/?date=sometimestamp",
      dataType: 'json'
    })
    .done(function( data ) {
    	callback(data);
    });
}