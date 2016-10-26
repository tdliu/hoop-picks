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

function pick() {
	$.ajax({
      type: "POST",
      url: "/pick/",
      dataType: 'json',
      data: JSON.stringify({ user_id: " the user id ", game_id: " the game id", team: " the team" })
    })
    .done(function( data ) {
        //alert( "Pick has been recorded: " + data['message']);
    });
}


function game() {
	$.ajax({
      type: "GET",
      url: "/game/?date=sometimestamp",
      dataType: 'json'
    })
    .done(function( data ) {
    	console.log(data);
    });
}