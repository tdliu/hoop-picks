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

function pick(pickID, callback) {
	$.ajax({
      type: "POST",
      url: "/pick/",
      dataType: 'json',
      data: JSON.stringify({ message: " BACON " })
    })
    .done(function( data ) {
        alert( "Pick has been recorded: " + data['message']);
    });
}