import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import Paper from 'material-ui/Paper';
import FlatButton from 'material-ui/FlatButton';
import AccountCircle from 'material-ui/svg-icons/action/account-circle';
import Close from 'material-ui/svg-icons/navigation/close';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import IconButton from 'material-ui/IconButton';
import NavigationClose from 'material-ui/svg-icons/navigation/close';

const styles = {
	title: {
		"fontFamily": "'Shrikhand', cursive",
	}
};

class GoatAppBar extends Component {
	constructor(props) {
	    super(props);

	    this.state = {
	      rightDrawerOpen: false,
	    };

	    console.log("app bar constructor current user: ", props.currentUser)
	    
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
			return <FlatButton icon={<AccountCircle />} onClick={ () => { this.handleAccountClick() }}/>
		}
		else {
			return <FlatButton label="Sign In" onClick={ () => { this.handleSignInClick() }}/>
		}
	}
	
	renderLoginOptions() {
		if (!this.props.currentUser) {
			return <Paper className="firebaseui-auth" />
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
				<AppBar title="GOAT Index"
				    titleStyle={styles.title}
				    iconElementRight={ this.renderRightButton() }
				  />
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
					{this.renderLoginOptions()}
					{this.renderDrawerMenu()}

				</Drawer>
				
			</div>
		);
	}
}

export default GoatAppBar;