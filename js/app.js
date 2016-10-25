$(document).foundation()

var pick_card_source   = $("#pick-card-template").html();
var pick_card_template = Handlebars.compile(pick_card_source);

var card_test_context = {time: "10:00pm", team1: "Patriots", team2: "Falcons"};
var html = pick_card_template(card_test_context);

for (var i = 0; i < 5; i ++) {
	$('#top-row').append(html);
}

function pick(pickID) {
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