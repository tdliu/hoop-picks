$(document).foundation()

//-------------- GLOBALS ---------------------//
var today;

//-------------- TEMPLATES -------------------//
var pick_card_source = $("#pick-card-template").html();
var pick_card_template = Handlebars.compile(pick_card_source);

//-------------- INITIAL REQUESTS ------------//

function addGames(games) {
  console.log(games);
  for (var i = 0; i < games.length; i ++) {
    var context = games[i];
    if (i == games.length - 1) {
      context.isLast = true;
    }

    context.awayPicked = (context.current_pick == context.away);
    context.homePicked = (context.current_pick == context.home);
    context.time = (getPrettyTime(context.time))

    var game = $(pick_card_template(context));
    addPickListeners(context, game);

    var added = $('#live-games-section').append(game);
  }

  $('#live-games-section').animate(
    {'opacity': 1},
    1000)
}
//-------------- LISTENERS -------------------//

function addPickListeners(context, game) {
  game.find(".home").click(function() {
    console.log(".home!!")
    $(this).addClass("picked")
    $(this).parent().find(".away").removeClass("picked")
    apiConnector.pick(context.game_id, context['home_id'])
  })
  
  game.find(".away").click(function() {
    console.log(".away!!")
    $(this).addClass("picked")
    $(this).parent().find(".home").removeClass("picked")
    apiConnector.pick(context.game_id, context['away_id'])
  })
}

function init(datestring) {
  today = new GoatDate(datestring);
  console.log(today.getMonthDateAbbrev());

  $('#today-label').html("Today " + today.getMonthDateAbbrev());

  //load games
  apiConnector.game(today.getDateString(), "nba", function(data) {
    $('#games-loader').hide();
    addGames(data);
  })
}