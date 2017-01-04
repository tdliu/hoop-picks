import React, {Component} from 'react';

import {BottomNavigation, BottomNavigationItem} from 'material-ui/BottomNavigation';
import CircularProgress from 'material-ui/CircularProgress';

import Index from 'material-ui/svg-icons/Action/trending-up';
import ViewComfy from 'material-ui/svg-icons/image/view-comfy';
import ViewCarousel from 'material-ui/svg-icons/action/view-carousel';
import GroupsIcon from 'material-ui/svg-icons/social/group';

import {pink800} from 'material-ui/styles/colors';

const NAV_INDEX_LIVE = 0;
const NAV_INDEX_GAMES = 1;
const NAV_INDEX_GROUPS = 2;
const NAV_INDEX_GOAT_INDEX = 3;

const styles = {
	navigation: {
		boxShadow: "inset 0 7px 9px -7px rgba(0,0,0,0.4)"
	},
	live :{
		color: 'grey',
		fontWeight: '700'
	},
	liveSelected: {
		color: pink800,
		fontWeight: '700'
	},
	index: {

	}
}

class GoatNavigation extends Component {
	constructor(props) {
		super(props);


	}

	renderYourGOATIndexIcon() {
		if (this.props.is_loading_user) {
			return <CircularProgress size={20} thickness={2} />
		}
		else if (this.props.goat_indeces) {
			var percent = this.props.goat_indeces.overall.correct / this.props.goat_indeces.overall.total;
			percent *= 100;
			if (this.props.navIndex == NAV_INDEX_GOAT_INDEX) {
				return <div style={ styles.liveSelected }>{ percent }%</div>;
			}
			else {
				return <div style={ styles.live }>{ percent }%</div>;
			}
		}
		else {
			return <Index />
		}
	}

	renderLiveIcon() {
		if (this.props.navIndex == NAV_INDEX_LIVE) {
			return <div style={ styles.liveSelected } >LIVE</div>
		}
		else {
			return <div style={ styles.live } >LIVE</div>
		}
	}

	render() {
		return (
			<BottomNavigation style={styles.navigation} selectedIndex={this.props.navIndex}>
					<BottomNavigationItem
						label="Scores"
						icon={ this.renderLiveIcon() }
						onTouchTap={() => this.props.nav(NAV_INDEX_LIVE)}
					/>
					<BottomNavigationItem
						label="Games"
						icon={<ViewComfy />}
						onTouchTap={() => this.props.nav(NAV_INDEX_GAMES)}
					/>
					<BottomNavigationItem
						label="Groups"
						icon={<GroupsIcon />}
						onTouchTap={() => this.props.nav(NAV_INDEX_GROUPS)}
					/>
					<BottomNavigationItem
						label="Your Index"
						icon={ this.renderYourGOATIndexIcon() }
						onTouchTap={() => this.props.nav(NAV_INDEX_GOAT_INDEX)}
					/>
				</BottomNavigation>	
		);
	}
}

export default GoatNavigation;