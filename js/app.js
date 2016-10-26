$(document).foundation()

var fake_games = [{time: "10:00pm", home: "Patriots", away: "Falcons", game_id: "1"},
                  {time: "8:00pm", home: "Colts", away: "Saints", game_id: "2"},
                  {time: "5:00pm", home: "49ers", away: "Panthers", game_id: "3"},
                  {time: "10:00pm", home: "Redskins", away: "Seahawks", game_id: "4"},
                  {time: "10:00pm", home: "Cowboys", away: "Rams", game_id: "5"}
                ];

//-------------- TEMPLATES -------------------//
var pick_card_source = $("#pick-card-template").html();
var pick_card_template = Handlebars.compile(pick_card_source);


//-------------- INITIAL REQUESTS ------------//

function addGames(games) {
  for (var i = 0; i < games.length; i ++) {
    var html = pick_card_template(games[i]);
    $('#live-games-section').append(html);
  }
  addPickCardListeners();
}

//-------------- LISTENERS -------------------//

function addPickCardListeners() {
  $('.pick-card-option').click(function() {
    //make a pick
    console.log($(this).children("input[name='game_id']").val());
  });  
}



addGames(fake_games);