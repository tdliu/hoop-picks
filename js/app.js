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
  console.log("FINISHED!");
  $('#game-loader').hide();
  console.log("nba: ", nba_games);
  console.log("nfl: ", nfl_games);
  nbaDateNav.initialGames(nba_games);
  nflDateNav.initialGames(nfl_games);
}

//-------------- INITIALIZE -------------------//

function init(datestring, logged, team_records) {
  logged_in = logged;

  today = new GoatDate(datestring);
  //TODO: rewind if it is early morning

  apiConnector = new ApiConnector(today, team_records);
  liveGameManager = new LiveGameManager(apiConnector);
  nbaDateNav = new GoatDateNavigator("nba", $('#nba-games-section'), $('#nba-date'), $('#nba-prev-date'), $('#nba-next-date'), today, apiConnector, 1);
  nflDateNav = new GoatDateNavigator("nfl", $('#nfl-games-section'), $('#nfl-date'), $('#nfl-prev-date'), $('#nfl-next-date'), today, apiConnector, 7);

  //initial loader: load games
  apiConnector.getNBAGames(today, function(data) {
    nba_games = data;
    work_finished();
  })

  apiConnector.getNFLGames(today, function(data) {
    nfl_games = data;
    work_finished();
  })


  liveGameManager.poll(function(data) {
    //gameInjector.todayLiveGameData(data);
  }); 

  setInterval(function() {
    console.log("interval");
    liveGameManager.poll();
  }, 10000)

}