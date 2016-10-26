$(document).foundation()

//-------------- TEMPLATES -------------------//
var pick_card_source = $("#pick-card-template").html();
var pick_card_template = Handlebars.compile(pick_card_source);

//-------------- INITIAL REQUESTS ------------//

function addGames(games) {
  for (var i = 0; i < games.length; i ++) {
    var context = games[i];
    if (i == games.length - 1) {
      context.isLast = true;
    }

    context.awayPicked = (context.current_pick == context.away);
    context.homePicked = (context.current_pick == context.home);

    var game = $(pick_card_template(context));
    addPickListeners(context, game);

    var added = $('#live-games-section').append(game);

  }
}

//-------------- LISTENERS -------------------//

function addPickListeners(context, game) {
  game.find(".home").click(function() {
    console.log(".home!!")
    $(this).addClass("picked")
    $(this).parent().find(".away").removeClass("picked")
    sendPick(context.game_id, context['home'])
  })
  
  game.find(".away").click(function() {
    console.log(".away!!")
    $(this).addClass("picked")
    $(this).parent().find(".home").removeClass("picked")
    sendPick(context.game_id, context['away'])
  })
}

function init() {
  //load games
  game("data", "nba", function(data) {
    addGames(data);
  })
}

init();