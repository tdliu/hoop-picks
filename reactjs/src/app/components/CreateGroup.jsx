import React, {Component} from 'react';

//material ui components
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import Toggle from 'material-ui/Toggle';

import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';

import CircularProgress from 'material-ui/CircularProgress';

//icons

import axios from 'axios';

const styles = {
	paper: {
		marginTop: 8,
	},
	form : {
		padding: 16,
	},
	formItem :{
		marginBottom: 16,
	}
	
}

class CreateGroup extends Component {
	constructor(props) {
		super(props);

		this.state= {
			passwordRequired: false,
			nameError : "",
			passwordError: "",
			sport: 1,
			loading: false,
		}

	}

	togglePasswordRequired() {
		this.setState(
			{ passwordRequired : !this.state.passwordRequired}
		);
	}

	renderPasswordField() {
		if (this.state.passwordRequired) {
			return (
				<div className="col-xs-12 col-sm-12" style={styles.formItem}>
					<TextField 
						hintText="Password" 
						errorText={ this.state.passwordError }
					/> 
				</div>
			);
		}
		else {
			return "";
		}
	}

	submit() {
		this.setState({loading : true});
	}

	renderSubmit() {
		if (!this.state.loading) {
			return (
				<div className="col-xs-12 col-sm-12" style={styles.formItem}>
					<RaisedButton
						label="Create Group"
						secondary={true}
						fullWidth={true}
						onClick={ () => { this.submit(); }}
					/>
				</div>
			);
		}
	}

	renderLoading() {
		if (this.state.loading) {
			return (
				<div className="col-xs col-sm" style={styles.formItem}>
					<CircularProgress />
				</div>
			);
		}
	}

	render() {
		return (
			<Paper style={styles.paper}>
				<div className="row" style={styles.form}>
					<div className="col-xs-12 col-sm-12">
						<h3> Create a Group </h3>
					</div>
					<div className="col-xs-12 col-sm-12" style={styles.formItem}>
						<TextField 
							hintText="Group Name" 
							errorText={ this.state.nameError }
						/>
					</div>
					<div className="col-xs-12 col-sm-12" style={styles.formItem}>
						<Toggle
						label="Require password to join?"
						onToggle= {() => { this.togglePasswordRequired() }}
					/>
					</div>
					
					{ this.renderPasswordField() }
					
					<div className="col-xs-12 col-sm-12" style={styles.formItem}>
						Sport
						<DropDownMenu value={this.state.sport} onChange={this.handleChange}>
				          <MenuItem value={1} primaryText="NBA" />
				        </DropDownMenu>

					</div>

					{ this.renderSubmit() }
				
				</div>
				<div className="row center-xs center-sm">
					{ this.renderLoading() }
				</div>

			</Paper>

		);
	}

}

export default CreateGroup;