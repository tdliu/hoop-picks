$(document).foundation()

//-------------- GLOBALS ---------------------//
var today;

var liveGameManager;
var logged_in;
var gameInjector;
var dateNav;
var apiConnector;


//-------------- SEMAPHORE -------------------//

var num_finished = 0
var TOTAL = 2;
var nba_games;
var nfl_games;


function work_finished() {
  num_finished += 1;
  if (num_finished >= TOTAL) {
    finished();
  }
}

function finished() {
  nbaDateNav.initialGames(nba_games);
  nflDateNav.initialGames(nfl_games);
  liveGameManager.poll();
}

//-------------- INITIALIZE -------------------//

function init(datestring, logged, team_records) {
  logged_in = logged;

  today = new GoatDate(datestring);
  var starting_date;
  if (isEarlyMorning()) {
    starting_date = today.getYesterday();
  }
  else {
    starting_date = today;
  }

  apiConnector = new ApiConnector(today, team_records);
  liveGameManager = new LiveGameManager(apiConnector, $('#live-games-section'), ['nba', ,'nfl']);
  nbaDateNav = new GoatDateNavigator("nba", $('#nba-games-section'), $('#nba-date'), $('#nba-prev-date'), $('#nba-next-date'), starting_date, apiConnector, 1);
  nflDateNav = new GoatDateNavigator("nfl", $('#nfl-games-section'), $('#nfl-date'), $('#nfl-prev-date'), $('#nfl-next-date'), starting_date, apiConnector, 7);

  //initial loader: load games
  apiConnector.getNBAGames(starting_date, function(data) {
    nba_games = data;
    liveGameManager.maybeRegisterGames(nba_games);
    work_finished();
  })

  apiConnector.getNFLGames(starting_date, function(data) {
    nfl_games = data;
    liveGameManager.maybeRegisterGames(nfl_games);
    work_finished();
  })

  apiConnector.user_goat_index('nba', function(data) {
    console.log(data);
    $('#percentage').html(Math.round(data.accuracy * 100) + "%");
    $('#correct').html(data.num_correct);
    $('#total').html(data.num_pick);
    //$('#user-goat-index').

  })

  setInterval(function() {
    liveGameManager.poll();
  }, 10000)

}