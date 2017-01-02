import React, {Component} from 'react';

import {List, ListItem} from 'material-ui/List';
import Subheader from 'material-ui/Subheader';

class Group extends Component {
	constructor(props) {
		super(props);

		

	}

	renderMemebers() {


		return (


		);
	}

	render() {
		return (
			<List>
				<Subheader>Group Members</Subheader>
				{ this.renderMembers() }
			</List>

		);
	}
}

export default Group;