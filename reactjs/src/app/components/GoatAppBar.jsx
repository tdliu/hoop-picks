import React, {Component} from 'react';

import AppBar from 'material-ui/AppBar';
import Paper from 'material-ui/Paper';
import FlatButton from 'material-ui/FlatButton';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';

import IconButton from 'material-ui/IconButton';

import MenuIcon from 'material-ui/svg-icons/navigation/menu';
import NavigationClose from 'material-ui/svg-icons/navigation/close';
import AccountCircle from 'material-ui/svg-icons/action/account-circle';

import {pink800} from 'material-ui/styles/colors';

const styles = {
	title: {
		"fontFamily": "'Shrikhand', cursive",
		"fontSize" : "1.75rem",
		"color" : "white"
	},
	menuButton: {
		color: "white"
	},
	accountButton: {
		color: "white"
	},
	signIn: {
		color: "white"
	},
	goat: {
		marginBottom: '-10px',
		marginLeft: '10px',
		marginTop: '10px',
	},
	bar: {
		backgroundColor: pink800,
	}
};

class GoatAppBar extends Component {
	constructor(props) {
	    super(props);

	    this.state = {
	      rightDrawerOpen: false,
	    };
	}

	componentDidMount() {
			
	};

	closeRightDrawer() {
		this.setState({
			rightDrawerOpen: false,
		})
	}

	signOut() {
		console.log("IMPLEMENT SIGN OUT CALLBACK")
		this.props.onSignOut();
		this.setState( {
			rightDrawerOpen: false,
		})
	}

	handleSignInClick() {
		window.location.assign('/signin/');
	}

	handleAccountClick() {
		if (!this.state.dialogOpen) {
			this.setState( {
				rightDrawerOpen: true,
			})	
		}
		else {
			this.setState( {
				rightDrawerOpenOpen: false,
			})		
		}
	}

	renderRightButton() {
		if (this.props.currentUser) {
			return (
				<IconButton 
					onClick={ () => { this.handleAccountClick() }}
					iconStyle={styles.accountButton}>
					<AccountCircle />
				</IconButton>
			);
		}
		else {
			return <FlatButton label="Sign In" style={styles.signIn} onClick={ () => { this.handleSignInClick() }}/>
		}
	}

	renderDrawerMenu() {
		if (this.props.currentUser) {
			return (
				<MenuItem onTouchTap={() => {this.signOut() }}>Sign Out</MenuItem>
			)
		}
		else {
			return "";
		}
		
	}

	render() {
		return (
			<div>
				<Paper style={styles.bar} zDepth={2}>
					<div className="row bottom-xs between-lg">
						<div className="col-xs-9 col-lg-4">
							<div className="row bottom-xs">
								<div className="col-xs-4 col-lg-3">
									<img src="/img/goat_medium.png" height="100px" width="100px" style={styles.goat}/>
								</div>
								<div className="col-xs-8 col-lg-9">
									<span style={styles.title}> GOAT Index </span>
								</div>
							</div>
						</div>
						<div className="col-xs-2 col-lg-1">
							{ this.renderRightButton() }
						</div>
					</div>
				</Paper>

				<Drawer 
					width={300}
					docked={false}
					disableSwipeToOpen={true}
					openSecondary={true} 
					open={this.state.rightDrawerOpen} >

					<AppBar 
						title="Account"
						iconElementLeft={<IconButton onClick={() => {this.closeRightDrawer()} }><NavigationClose /></IconButton>}	
					/>

					{this.renderDrawerMenu()}

				</Drawer>
			
			</div>
		);
	}
}

export default GoatAppBar;