import React, {Component} from 'react';
//components
import CreateGroup from './CreateGroup.jsx'

//material ui components
import {List, ListItem} from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import RaisedButton from 'material-ui/RaisedButton';
import LinearProgress from 'material-ui/LinearProgress';
import Paper from 'material-ui/Paper';

//icons
import AddIcon from 'material-ui/svg-icons/content/add-circle-outline';
import Warning from 'material-ui/svg-icons/alert/error-outline';

import axios from 'axios';

const styles = {
	paper: {
		marginTop: 8,
	},
	create_group_button: {
		
	}
}

const VIEW_LOADING = 0;
const VIEW_NOT_SIGNED_IN = 1;
const VIEW_GROUPS_LIST = 2;
const VIEW_CREATE_GROUP = 3;

class Groups extends Component {
	constructor(props) {
		super(props);
		var view = VIEW_GROUPS_LIST;
		
		if (this.props.currentUser) {

		}
		else {
			view = VIEW_NOT_SIGNED_IN;
		}

		this.state = {
			view : view,
		}

	}

	renderCreateGroupButton() {
		return(
			<RaisedButton
				buttonStyle={styles.create_group_button}
				label="Create A Group"
				secondary={true}
				icon={<AddIcon />}
				fullWidth={true}
				onClick={ () => { this.setState({view : VIEW_CREATE_GROUP}) }}
			/>
		);
	}

	renderGroup(group, i) {
		return (
			<ListItem primaryText={group.name} key={i}/>
		);
		
	}

	renderNotSignedIn() {
		return (
			<Paper style={styles.paper}>
				<List>
	      			<ListItem 
	      				primaryText="You must sign in to view your groups." 
	      				leftIcon={<Warning />}
	      				disabled={true} />
	      		</List>
      		</Paper>

		);
	}

	renderGroupsList() {
		var groups = [];
		for (var i = 0; i < this.props.groups.length; i++) {
			
			groups.push(
				this.renderGroup(this.props.groups[i], i)
			);
		}

		return (
			<Paper style={styles.paper}>
				<List>
					{ this.renderCreateGroupButton() }
					<Subheader>Your Groups</Subheader>
					{ groups }
				</List>
			</Paper>
		);
	}

	renderCreateGroup() {
		return (
			<CreateGroup 
				currentUser={this.props.currentUser}
			/>
		);
	}

	render() {
		if (this.state.view == VIEW_LOADING) {
			return <LinearProgress mode="indeterminate" />;
		}
		else if (this.state.view == VIEW_NOT_SIGNED_IN) {
			return this.renderNotSignedIn();
		}
		else if (this.state.view == VIEW_GROUPS_LIST) {
			return this.renderGroupsList();
		}
		else if (this.state.view == VIEW_CREATE_GROUP) {
			return this.renderCreateGroup();
		}
	}
}

export default Groups;