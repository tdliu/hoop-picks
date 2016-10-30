$(document).foundation()

//-------------- GLOBALS ---------------------//

var today;
var tomorrow;
var next;
var liveGameManager;
var logged_in;
var gameInjector;

//-------------- INITIAL REQUESTS ------------//

function addGamesToSection(section, games, is_today) {
  for (var i = 0; i < games.length; i ++) {
    games[i].is_today = is_today;
    if (i == games.length - 1) {
      games[i].isLast = true;
    }

    var game = new GoatGame(games[i]);

    section.append(game.elem);
  }

  section.animate(
    {'opacity': 1},
    1000)
}
//-------------- LISTENERS -------------------//

function updateDateSelector() {
  $('#upcoming-label').html("" + tomorrow.getMonthDateAbbrev());
  $('#next-btn').html("" + next.getMonthDateAbbrev() + " >>");
}

function loadUpcomingGames() {
  $('#upcoming-games-section').html("")
  $('#upcoming-loader').show();

  apiConnector.game(tomorrow.getDateString(), "nba", function(data) {
    $('#upcoming-loader').hide();
    gameInjector.upcomingGameData(data);//addGamesToSection($('#upcoming-games-section'), data, false);
  })
}

function selectPrev() {
  next = tomorrow;
  tomorrow = tomorrow.getYesterday();
  if (tomorrow._date == today._date) {
    tomorrow = tomorrow.getYesterday();

  }
  updateDateSelector();
  loadUpcomingGames();
}

function selectNext() {
  tomorrow = next;
  next = next.getTomorrow();
  if (next._date == today._date) {
    next = next.getTomorrow();
  }

  updateDateSelector();
  loadUpcomingGames();
}

function init(datestring, logged) {
  logged_in = logged;

  today = new GoatDate(datestring);
  tomorrow = today.getTomorrow();
  next = tomorrow.getTomorrow();
  updateDateSelector();

  liveGameManager = new LiveGameManager(apiConnector);
  gameInjector = new GoatGameInjector($('#started-games-section'), $('#today-upcoming-games-section'), $('#upcoming-games-section'));

  $('#today-label').html("Today " + today.getMonthDateAbbrev());
  

  //load games
  apiConnector.game(today.getDateString(), "nba", function(data) {
    $('#games-loader').hide();
    gameInjector.todayGameInfo(data);
  })

  apiConnector.game(tomorrow.getDateString(), "nba", function(data) {
    $('#upcoming-loader').hide();
    gameInjector.upcomingGameData(data);//addGamesToSection($('#upcoming-games-section'), data, false);
  })

  liveGameManager.poll(function(data) {
    gameInjector.todayLiveGameData(data);
  });

  $('#next-btn').click(function() {
    selectNext();
  })
  $('#upcoming-label').click(function() {
    selectPrev();
  })

  setInterval(function() {
    console.log("interval");
    liveGameManager.poll();
  }, 10000)

}