import React, {Component} from 'react';

import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';

import ApiConnector from '../ApiConnector.jsx';

class DebugPanel extends Component {
	constructor(props) {
		super(props);

		this.state = {
			get_url: "",
			post_url: "",
			which_token: "debugToken",
			post_args: "",
			firebase_token: props.firebaseToken,
		}
	}

	componentWillReceiveProps(props) {
		this.setState( {firebase_token: props.firebaseToken} );
	}

	submitGet() {
		if (this.state.which_token == "debugToken") {
			var config = ApiConnector.createAuthConfig("", true);
		}
		else {
			var config = ApiConnector.createAuthConfig(this.state.firebase_token, false)
		}
		ApiConnector.sendGetRequest(this.state.get_url, config, function(res) {console.log("DEBUG", res) });
	}

	submitPost() {
		if (this.state.which_token == "debugToken") {
			var config = ApiConnector.createAuthConfig("", true);
		}
		else {
			var config = ApiConnector.createAuthConfig(this.state.firebase_token, false)
		}
		var args = JSON.parse(this.state.post_args)
		ApiConnector.sendPostRequest(this.state.get_url, args, config, function(res) {console.log("DEBUG", res) });
		
	}

	render() {
		return (
			
			<Paper>
				<h4 style={{padding:8}}> DEBUG </h4>
				<RaisedButton
					label="Log current options"
					onClick={ () => { console.log(this.state) } }
					style={{marginBottom: 16, margin: 16}}
				/>
				<RadioButtonGroup 
					name="which_token" 
					defaultSelected="debugToken"
					onChange= { (event, value) => { this.setState({which_token: value}) } }
					>

					<RadioButton
						value="debugToken"
						label="Use Debug Token (12345)"
						style={ {paddingLeft: 16} }
					/>
					<RadioButton
						value="firebaseToken"
						label="Use Firebase Auth Token"
						style={ {paddingLeft: 16} }
					/>
				</RadioButtonGroup>


				<TextField 
					hintText="get url" 
					onChange={ e => { this.setState({get_url: e.target.value}) } }
					style={ {margin: 8, paddingTop: 16} }
					errorText="example: /game/?sport=nba&date=20150404"
					errorStyle={ {color: 'black' }}
				/>
				<RaisedButton
					label="Submit GET Request"
					onClick={ () => {  this.submitGet() } }
					style={{margin: 16}}
				/>

				<TextField 
					hintText="POST url"
					onChange={ e => { this.setState({post_url: e.target.value}) } }
					style={ {margin: 8} }
					errorText="example: /group/create/"
					errorStyle={ {color: 'black' }}
				/>
				<TextField 
					hintText="POST args"
					onChange={ e => { this.setState({post_args: e.target.value}) } }
					style={ {margin: 8} }
					errorText="{ sport: 'nba', date: '20161414'}"
					errorStyle={ {color: 'black' }}
				/>
				<RaisedButton
					label="Submit POST Request"
					onClick={ () => { this.submitPost() } }
					style={{margin: 16}}
				/>
			</Paper>
			
		);
	}
}

export default DebugPanel;
