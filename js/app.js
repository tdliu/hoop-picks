$(document).foundation()

//-------------- GLOBALS ---------------------//

var today;

var liveGameManager;
var logged_in;
var gameInjector;
var dateNav;

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
  $('#date').html("" + today.getMonthDateAbbrev());
  //$('#next-btn').html("" + next.getMonthDateAbbrev() + " >>");
}

function loadUpcomingGames() {
  $('#date-games-section').html("")
  $('#game-loader').show();

  apiConnector.game(today.getDateString(), "nba", function(data) {
    $('#game-loader').hide();
    $('#date-games-section').html("")
    gameInjector.upcomingGameData(data);//addGamesToSection($('#upcoming-games-section'), data, false);
  })
}

function selectPrev() {
  today = today.getYesterday();
  updateDateSelector();
  loadUpcomingGames();
}

function selectNext() {
  today = today.getTomorrow();
  updateDateSelector();
  loadUpcomingGames();
}

function init(datestring, logged) {
  logged_in = logged;

  today = new GoatDate(datestring);
  updateDateSelector();

  liveGameManager = new LiveGameManager(apiConnector);
  gameInjector = new GoatGameInjector($('#started-games-section'), $('#date-games-section'));

  //load games
  apiConnector.game(today.getDateString(), "nba", function(data) {
    $('#game-loader').hide();
    gameInjector.todayGameInfo(data);
  })

  liveGameManager.poll(function(data) {
    gameInjector.todayLiveGameData(data);
  });

  $('#prev-date').click(function() {
    selectPrev();
  })

  $('#next-date').click(function() {
    selectNext();
  })
  

  setInterval(function() {
    console.log("interval");
    liveGameManager.poll();
  }, 10000)

}