import React, {Component} from 'react';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import axios from 'axios';

class FeedCard extends Component {
	constructor(props) {
		super(props);


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

	}

	awayClicked() {

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
		return(
			<div className="col-xs-12 col-sm-12">

				<Card style="styles.card">
					



				</Card>


			</div>
		);

	}

}

export default FeedCard;