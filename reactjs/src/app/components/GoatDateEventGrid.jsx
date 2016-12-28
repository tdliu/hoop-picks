import React, {Component} from 'react';
import GoatEvent from './GoatEvent.jsx'

import NavigationChevronLeft from 'material-ui/svg-icons/navigation/chevron-left';
import NavigationChevronRight from 'material-ui/svg-icons/navigation/chevron-right';
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

class GoatDateEventGrid extends Component {
	constructor(props) {
		super(props);
		var moment = Moment();

		if (moment.hours() < 6) {
			moment = moment.add(-1, 'd')
		}

		this.state = {
			events: [],
			moment: moment,
			todays_date: moment.format("YYYYMMDD"),
			date_cursor_label: moment.format("MMM Do"),
			loading: true,
		};
	}

	navigate(negative_one_or_positive_one) {
		var newMoment = this.state.moment.add(negative_one_or_positive_one, 'd')
		
		this.setState({ loading: true});
		axios.get('/game/?sport=nba&date=' + newMoment.format("YYYYMMDD"))
			.then(res => {
				this.setState({
					events: res.data,
					moment: newMoment,
					todays_date: newMoment.format("YYYYMMDD"),
					date_cursor_label: newMoment.format("MMM Do"),
					loading: false
				})
			});
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

	componentWillReceiveProps(nextProps) {
		if (nextProps.currentUser != this.props.currentUser) {
			console.log("USER HAS CHANGED, NEW REQUEST");
			this.navigate(0);
		}
	}

	renderEvents() {
		var events = [];
		for (var i = 0; i < this.state.events.length; i++) {
			events.push( 
				<GoatEvent 
					key={i} 
					data={ this.state.events[i] } 
					currentUser={ this.props.currentUser }
					snackbarAlert= {this.props.snackbarAlert}
				/> 
			);
		}
		return events;
	}

	renderLoader() {
		if (this.state.loading) {
			return <LinearProgress mode="indeterminate" />
		}
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
				<div className="row center-xs center-sm center-lg" >
					<div className="col-xs col-sm col-lg-2">
						<FlatButton icon={<NavigationChevronLeft />} onClick={() => { this.navigate(-1) }} />
					</div>
					<div className="col-xs col-sm col-lg-2"> 
						<FlatButton label={this.state.date_cursor_label} disabled={true} labelStyle={styles.label} />
					</div>
					<div className="col-xs col-sm col-lg-2">
						<FlatButton icon={<NavigationChevronRight />} onClick={() => { this.navigate(1) }}/>
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