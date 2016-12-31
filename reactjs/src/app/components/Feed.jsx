import React, {Component} from 'react';

import FlatButton from 'material-ui/FlatButton';
import LinearProgress from 'material-ui/LinearProgress';
import Paper from 'material-ui/Paper';

import axios from 'axios';
import Moment from 'moment-timezone';

const styles = {
	h4: {
		fontFamily: "Roboto",
		fontSize: "1.2rem",
		margin: 16,
	},
	container: {
		paddingLeft: 16,
		paddingRight: 16,
		paddingBottom: 16,
	},
	containerContainer: {
		marginTop: 8,
	},
	label: {
		color: "black",
	}
};

class Feed extends Component {
	constructor(props) {
		super(props);

		var moment = Moment();

		this.state = {
			events: [],
			moment: moment,
			todays_date: moment.format("YYYYMMDD"),
			date_cursor_label: moment.format("MMM Do"),
			loading: true,
		};
	}

	componentDidMount() {
		axios.get('/game/?sport=nba&date=' + this.state.todays_date)
			.then(res => {
				this.setState( {
					events: res.data,
					loading: false
				});
				console.log(res);
			});
	}

	renderEvent(i) {
		
	}

	render() {
		return (




		);
	}

}

export default feed;