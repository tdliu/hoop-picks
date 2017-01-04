import React, {Component} from 'react';

import Paper from 'material-ui/Paper';

const styles = {
	paper: {
		marginTop: 16,
		paddingLeft: 16,
		paddingRight: 16,
		paddingBottom: 4,
	},
	timeLive: {
		color: 'red',
		fontSize: '.8rem',
		fontWeight: '700',
	},
	timeFinal: {
		color: 'black',
		fontSize: '.8rem',
		fontWeight: '700',
	},
	timeRow: {
		paddingTop: 8,
		marginBottom: 8,
	},
	teamRow: {
		marginBottom: 8,
	}
}

class LiveEvent extends Component  {
	constructor(props) {
		super(props);
	}


	renderTimestamp() {
		var timestamp = "";
		var style = styles.timeLive;
		if (this.props.data.period.isHalftime) {
			timestamp = "halftime";
		}
		else if (this.props.data.period.current == 4 && !this.props.data.isGameActivated) {
			timestamp = "final";
			style = styles.timeFinal;
		}
		else {
			var period = this.props.data.period.current;
			var periodString = "";
			if (period == 1) periodString = "1st";
			if (period == 2) periodString = "2nd";
			if (period == 3) periodString = "3rd";
			if (period == 4) periodString = "4th";

			if (this.props.data.period.isEndOfPeriod) {
				timestamp = "End " + periodString;
			}
			else {
				var clock = this.props.data.clock;
				timestamp = clock + " - " + periodString;
			}
		}

		return <div style={ style }>{ timestamp } </div>
	}

	renderAwayTeam() {
		return (
			<div className="row" style={ styles.teamRow }>
				<div className="col-xs-2">
					
				</div>
				<div className="col-xs">
					{ this.props.data.vTeam.triCode }
				</div>
				<div className="col-xs-3">
					{ this.props.data.vTeam.score }
				</div>
			</div>
		);
	}

	renderHomeTeam() {
		return (
			<div className="row" style={ styles.teamRow }>
				<div className="col-xs-2">
					
				</div>
				<div className="col-xs">
					{ this.props.data.hTeam.triCode }
				</div>
				<div className="col-xs-3">
					{ this.props.data.hTeam.score }
				</div>
			</div>
		);
	}

	render() {
		return (
			<div className="col-xs-6 col-sm-6 col-lg-3">
				<Paper style={ styles.paper } rounded={ false }>
					<div className="row" style={ styles.timeRow } >
						<div className="col-xs-10 col-xs-offset-2">
							{ this.renderTimestamp() }
						</div>
					</div>

					{ this.renderAwayTeam() }

					{ this.renderHomeTeam() }

				</Paper>
			</div>
		);
	}
}

export default LiveEvent;