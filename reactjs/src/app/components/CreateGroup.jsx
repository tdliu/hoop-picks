import React, {Component} from 'react';

import ApiConnector from '../ApiConnector.jsx';

//material ui components
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import Toggle from 'material-ui/Toggle';

import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';

import CircularProgress from 'material-ui/CircularProgress';

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
			nameValue: null,
			sportValue: null,
			passwordValue: null,
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
						onChange={ e => { this.setState({passwordValue: e.target.value}) } }
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
		var params = {
			name:  this.state.nameValue,
			password_required: this.state.passwordRequired,
			password: this.state.passwordValue,
			sport: this.state.sportValue,
		}

		ApiConnector.createGroup(this.props.currentUserToken, params, res => {
			console.log(res);
			if (res.data.success) {
				
			}
			else {
				if (res.data.problem_param) {
					if (res.data.problem_param == 'name') {
						this.setState({
							nameError: res.data.message,
							loading: false
						})
					}
					else if (re.data.problem_parapm == 'password') {
						this.setState({
							nameError: res.data.message,
							loading: false
						})
					}

				}
				else {

				}
			}
		})
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
							onChange={ e => { this.setState({nameValue: e.target.value}) } }
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
						<DropDownMenu 
							value={this.state.sport} 
							onChange={ e => { this.setState({sportValue: e.target.value}) } }>
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