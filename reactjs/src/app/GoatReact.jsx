import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

//---------- My Components ----------
import GoatAppBar from './components/GoatAppBar.jsx';
import GoatNavigation from './components/GoatNavigation.jsx';

//-------- Material UI Components ------
import Snackbar from 'material-ui/Snackbar';

//------------- SECTIONS ------------------
import Groups from './components/Groups.jsx';
import GoatDateEventGrid from './components/GoatDateEventGrid.jsx';
import DebugPanel from './components/DebugPanel.jsx'
import YourGOATIndex from './components/YourGOATIndex.jsx';

//-----------ICONS --------------
import AccountCircle from 'material-ui/svg-icons/action/account-circle';

import {pink800} from 'material-ui/styles/colors';

import firebase from 'firebase';
import firebaseui from 'firebaseui';

import ApiConnector from './ApiConnector.jsx';

import injectTapEventPlugin from 'react-tap-event-plugin';
injectTapEventPlugin();

// Initialize Firebase
var config = {
	apiKey: "AIzaSyCyC7WNpwar0SJr5XqxewMsYrISocl12lM",
	authDomain: "goatindex-e7638.firebaseapp.com",
	databaseURL: "https://goatindex-e7638.firebaseio.com",
	storageBucket: "goatindex-e7638.appspot.com",
	messagingSenderId: "1041806276577"
};
firebase.initializeApp(config);

const muiTheme = getMuiTheme({
  palette: {
  	primary1Color: pink800,
  },
  appBar: {
    height: 50,
  },
});

class App extends Component {
	constructor() {
		super();

		this.state = {
			currentUser: null,
			currentUserToken: null,
			snackbarOpen : false,
			snackbarAction : "",
			snackbarMessage : "",
			navIndex : 0,
			user_groups: [],
			debugUrl: null,
			is_loading_user: false,
		}	
	}

	snackbarAlert(message) {
		console.log("snackbaralert: ", message)
		this.setState({
			snackbarMessage : message, 
			snackbarOpen: true
		});
	}

	handleAuthStateChanged(user) {
		if (user) {
			console.log("changed: signed in", user)
			this.setState({
				currentUser: user,
			})

			user.getToken().then( iDToken => {
				console.log(iDToken)
				this.setState({
					currentUserToken : iDToken,
				})

				ApiConnector.getUser(iDToken, res => {
					console.log("USER: ", res)
					this.setState({
						user_groups : res.data.groups,
						user_goat_indeces : res.data.goat_indeces,
						is_loading_user: false,
					})
				})
				this.setState({ is_loading_user: true })
			})
			.catch(function(error) {
				console.log(error);
			});
		 } 
		 else {
			this.setState({
				currentUser: null,
				currentUserToken: null
			})
		  }
	}

	handleSignOut() {
		firebase.auth().signOut().then(
			() => {
				this.setState({
					currentUser: null,
				})
				window.location.reload(true);
			}, error => {
				console.log("error: ", error)
			}
		)
	}

	componentDidMount() {
		firebase.auth().onAuthStateChanged( user => { this.handleAuthStateChanged(user) });
	}

	componentWillUnmount() {
		
	}

	nav(index) {
		this.setState({navIndex: index})
	}

	renderMainContent() {
		if (this.state.navIndex == 0) {
			return this.renderLeaderboards()
		}
		else if (this.state.navIndex == 1) {
			return this.renderGames();
		}
		else if (this.state.navIndex == 2) {
			return this.renderGroups()
		}
		else if (this.state.navIndex == 3) {
			return this.renderYourGOATIndex()
		}
	}

	renderGames() {
		return (
			<div className="row center-lg">
				<div className="col-xs-12 col-sm-12 col-lg-8">
					<GoatDateEventGrid 
						currentUser= { this.state.currentUser } 
						currentUserToken = { this.state.currentUserToken }
						snackbarAlert={ message => {this.snackbarAlert(message) } } 
					/>
				</div>
			</div>
		);
	}

	renderLeaderboards() {

	}

	renderGroups() {
		return (
			<div className="row center-lg">
				<div className="col-xs-12 col-sm-12 col-lg-8">
					<Groups 
						currentUser={ this.state.currentUser }
						currentUserToken={ this.state.currentUserToken }
						groups={ this.state.user_groups }
					/>
				</div>
			</div>
		);
	}

	renderYourGOATIndex() {
		return (
			<YourGOATIndex 
				goat_indeces={ this.state.user_goat_indeces }
			/>

		);
	}

	renderFeed() {

	}

	render() {
		return (
			<MuiThemeProvider muiTheme={muiTheme}>
			<div>
				<GoatAppBar 
					currentUser={ this.state.currentUser } 
					currentUserToken={ this.state.currentUserToken }
					onSignOut={ () => { this.handleSignOut() }}
				/>
				<GoatNavigation 
					nav= { index => {this.nav(index) } }
					goat_indeces= { this.state.user_goat_indeces }
					is_loading_user= { this.state.is_loading_user }
					navIndex= { this.state.navIndex }
				/>

				{ this.renderMainContent() }

				{/*<DebugPanel firebaseToken={ this.state.currentUserToken } /> */}

				<Snackbar
					open= { this.state.snackbarOpen }
					message= { this.state.snackbarMessage }
					action= { this.state.snackBarAction }
					autoHideDuration= { 2000 }
					onRequestClose= {() => { console.log("closed"); this.setState({snackbarOpen : false}) }}
				/>

			</div>
			
		  </MuiThemeProvider>
		);
	};
}

function makeRequest(url) {
	console.log(url);
}

ReactDOM.render(
	<App />
  ,
  document.getElementById('app')
);

