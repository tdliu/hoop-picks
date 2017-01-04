import React, {Component} from 'react';

import ApiConnector from '../ApiConnector.jsx';

import LiveEvent from './LiveEvent.jsx';

import LinearProgress from 'material-ui/LinearProgress';
import Paper from 'material-ui/Paper';

import Moment from 'moment-timezone';

const styles = {
	paper: {
		marginTop: 8
	},
	header: {
		fontSize: "1.2rem",
		margin: 16,
	},
	container: {
		paddingLeft: 16,
		paddingRight: 16,
		paddingBottom: 16,
	}
}

class LiveEventPanel extends Component {
	constructor(props) {
		super(props);

		this.state= {
			loading: true,
			events: [],
			poll: true,
		};
	}

	componentDidMount() {
		this.getLiveEvents();
		//setInterval(() => { this.getLiveEvents() }, 10000);
	}

	componentWillUnmount() {
		console.log("hey")
		this.setState({
			poll: false,
		})
	}

	getLiveEvents() {
		if (!this.state.poll) 
			return;
		ApiConnector.getLiveEvents( res => {
			if (res.status == 200) {
				console.log(res.data);
				this.setState({ 
					events: res.data,
					loading: false,
				 });
			}
		})
	}

	renderLoader() {
		if (this.state.loading) {
			return <LinearProgress mode="indeterminate" />
		}
	}

	renderLiveEvents() {
		var events= [];
		for (var i = 0; i < this.state.events.length; i++) {
			events.push(
				<LiveEvent
					key={ i }
					data={ this.state.events[i] }
				/>
			);
		}
		return events;
	}

	render() {
		return (
			<Paper style={styles.paper}>

				{ this.renderLoader() }

				<div className="row center-xs center-sm center-lg">
					<div className="col-xs-12">
						<h4 style={styles.header}> NBA </h4>
					</div>
				</div>
				<div className="row" style={ styles.container }>
					{ this.renderLiveEvents() }
				</div>

			</Paper>
		);
	}


}

export default LiveEventPanel;