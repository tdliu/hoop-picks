import React, {Component} from 'react';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import GoatEventOption from './GoatEventOption.jsx'
import axios from 'axios';

const styles = {
	card: {
		marginTop: 16,
		paddingLeft: 16,
		paddingRight: 16,
		paddingBottom: 4,
	},
};

class GoatEvent extends Component {
	constructor(props) {
		super(props);
		this.state = {
			homePicked : false,
			awayPicked : true,
		};
	}

	formatTime() {
		if (this.props.data.time) {
			return this.props.data.time;
		}
		else {
			return "!time!";
		}
	}

	homeClicked() {
		if (!this.props.enabled)
			return
		if (this.state.homePicked) {
			this.setState({ homePicked: false});
			this.sendPick(null);
		}
		else {
			this.setState({ homePicked: true, awayPicked: false});
			this.sendPick(this.props.data.home_id);
		}
	}

	awayClicked() {
		if (!this.props.enabled)
			return
		if (this.state.awayPicked) {
			this.setState({ awayPicked: false});
			this.sendPick(null);
		}
		else {
			this.setState({ awayPicked: true, homePicked: false});
			this.sendPick(this.props.data.away_id);
		}
	}

	sendPick(team_id) {
		var params = {
			user_id: this.props.currentUser.uid,
			team_id: team_id,
			game_id: this.props.data.game_id,
		};
		console.log("Sending Pick", params);

		axios.post('/pick/', params)
			.then(response => {
				console.log(response);
				this.props.snackbarAlert("Pick Saved")
			})
			.catch(error => {
				this.props.snackbarAlert(error.message);
				console.log(error);
			}
		);
	}

	render() {
		return (
			<div className="col-xs-6 col-sm-6 col-lg-3">

				<Card style={styles.card}>
					<CardHeader
					  subtitle={ this.formatTime() }
					  actAsExpander={true}
					  showExpandableButton={true}
					/>

					<GoatEventOption 
						teamName= {this.props.data.away} 
						picked= { this.state.awayPicked } 
						onClick={() => { this.awayClicked(); }}
					/>

					<GoatEventOption 
						teamName= {this.props.data.home} 
						picked={ this.state.homePicked } 
						onClick={() => { this.homeClicked(); }} 
					/>

					<CardText expandable={true}>
					  Extra Info
					</CardText>

				</Card>

			</div>
		)
	}
}

export default GoatEvent;