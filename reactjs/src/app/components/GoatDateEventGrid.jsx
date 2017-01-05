import React, {Component} from 'react';

import GoatEvent from './GoatEvent.jsx'
import LiveEvent from './LiveEvent.jsx';

import ApiConnector from '../ApiConnector.jsx'

import NavigationChevronLeft from 'material-ui/svg-icons/navigation/chevron-left';
import NavigationChevronRight from 'material-ui/svg-icons/navigation/chevron-right';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import IconButton from 'material-ui/IconButton';
import LinearProgress from 'material-ui/LinearProgress';
import Paper from 'material-ui/Paper';

import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar';

import axios from 'axios';
import Moment from 'moment-timezone';

const styles = {
	h4: {
		fontFamily: "Roboto",
		fontSize: "1.2rem",
		marginBottom: 4,
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
	},
	navButton: {
		margin: 8,
	}
};

class GoatDateEventGrid extends Component {
	constructor(props) {
		super(props);
		var moment = Moment();

		if (moment.hours() < 6) {
			moment = moment.add(-1, 'd')
		}

		this.state = {
			scheduledEvents: [],
			liveEvents: [],
			poll: true,
			todays_datestring: moment.format("YYYYMMDD"),
			todays_moment: Moment(moment),
			cursor_moment: moment,
			cursor_datestring: moment.format("YYYYMMDD"),
			date_cursor_label: moment.format("MMM Do"),
			loading: true,
		};
	}

	navigateToToday() {
		var newMoment = this.state.todays_moment;
		
		this.setState({ loading: true});
		ApiConnector.getEvents(null, 'nba', newMoment.format("YYYYMMDD"), res => {
			this.setState({
					scheduledEvents: res.data,
					cursor_moment: Moment(newMoment),
					cursor_datestring: newMoment.format("YYYYMMDD"),
					date_cursor_label: newMoment.format("MMM Do"),
					loading: false
				})
		})
	}

	navigate(negative_one_or_positive_one) {
		var newMoment = this.state.cursor_moment.add(negative_one_or_positive_one, 'd')
		
		this.setState({ loading: true});
		ApiConnector.getEvents(null, 'nba', newMoment.format("YYYYMMDD"), res => {
			this.setState({
					scheduledEvents: res.data,
					cursor_moment: newMoment,
					cursor_datestring: newMoment.format("YYYYMMDD"),
					date_cursor_label: newMoment.format("MMM Do"),
					loading: false
				})
		})
	}

	getLiveEvents() {
		if (!this.state.poll) 
			return;
		ApiConnector.getLiveEvents( res => {
			if (res.status == 200) {
				console.log(res.data);
				this.setState({ 
					liveEvents: res.data,
					loading: false,
				 });
			}
		})
	}	

	componentDidMount() {
		this.getLiveEvents();
		setInterval(() => { this.getLiveEvents() }, 10000);

		ApiConnector.getEvents(null, 'nba', this.state.todays_datestring, res => {
			this.setState( {
					scheduledEvents: res.data,
					loading: false
				});
		});
	}

	componentWillReceiveProps(nextProps) {
		if (nextProps.currentUser != this.props.currentUser) {
			console.log("USER HAS CHANGED, NEW REQUEST");
			this.navigate(0);
		}
	}

	componentWillUnmount() {
		this.setState({
			poll: false,
		})
	}

	hasScheduledEventStarted(event, moment) {
		var scheduled_moment = Moment.tz(event.time, "HH:mm:ss", "America/New_York")
		//NOT the scheduled time is before now aka the scheduled time is after now
		return (!scheduled_moment.isBefore(moment)) 

	}

	getLiveEventFromScheduledEvent(scheduled_event) {
		var id = scheduled_event.game_id;
		for (var i = 0; i < this.state.liveEvents.length; i++) {
			if (("nba" + this.state.liveEvents[i].gameId) == id) {
				return this.state.liveEvents[i];
			}
		}
		console.log("not found", id);
		return null;
	}

	renderEvents() {
		var today_is_today = (this.state.cursor_datestring === this.state.todays_datestring)
		var now_eastern = Moment().tz('America/New_York');

		var events = [];
		for (var i = 0; i < this.state.scheduledEvents.length; i++) {
			var curr_event = this.state.scheduledEvents[i];
			var rendered_event = null;

			if (today_is_today && this.hasScheduledEventStarted(curr_event)) {
				var live_event_data = this.getLiveEventFromScheduledEvent(curr_event);
				if (!live_event_data) {
					rendered_event = (
						<GoatEvent 
							key={ i } 
							data={ this.state.scheduledEvents[i] } 
							currentUser={ this.props.currentUser }
							snackbarAlert= {this.props.snackbarAlert}
							enabled= {false}
						/> 
					);
				}
				else {
					rendered_event = (
						<LiveEvent
							key={ i }
							data={ live_event_data }
						/>
						)
				}
				
			}
			else {
				rendered_event = (
					<GoatEvent 
						key={ i } 
						data={ this.state.scheduledEvents[i] } 
						currentUser={ this.props.currentUser }
						snackbarAlert= {this.props.snackbarAlert}
						enabled= {true}
					/> 
				);
			}
			events.push(rendered_event);
			
		}
		return events;
	}

	renderLoader() {
		if (this.state.loading) {
			return <LinearProgress mode="indeterminate" />
		}
	}

	renderTodayButton() {
		var today_is_today = (this.state.cursor_datestring === this.state.todays_datestring)
		return (
			<RaisedButton 
				label="Today" 
				style={ styles.navButton }
				onClick={ () => { this.navigateToToday() }}
				disabled={ today_is_today } />
		);
	}

	render() {
		return (
			<Paper style={styles.containerContainer}>
				{ this.renderLoader() }
				<div className="row center-xs center-sm center-lg">
					<div className="col-xs-12">
						<h4 style={styles.h4}> NBA </h4>
					</div>
				</div>
				<div className="row center-xs center-sm center-lg">
					<div className="col-xs col-sm col-lg-2"> 
						<FlatButton label={this.state.date_cursor_label} disabled={true} labelStyle={styles.label} />
					</div>
				</div>
				<div className="row center-xs ">
					<div className="col-xs-3 col-sm col-lg-1"> 
						{ this.renderTodayButton() }
					</div>	
					<div className="col-xs-3 col-sm col-lg-1"> 
						<RaisedButton 
							style={ styles.navButton }
							icon={<NavigationChevronLeft />}
							onClick={ () => (this.navigate(-1)) } />
					</div>
					<div className="col-xs-3 col-sm col-lg-1"> 
						<RaisedButton 
							style={ styles.navButton }
							icon={<NavigationChevronRight />} 
							onClick={ () => (this.navigate(1)) } />
					</div>
				</div>
				
				<div className="row" style={ styles.container }>

					{ this.renderEvents() }

				</div>

			</Paper>

		)
	}
}

export default GoatDateEventGrid;