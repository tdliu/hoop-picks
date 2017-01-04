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
			
			<Paper style={{ padding: 16, marginTop: 8 }}>
				<div className="row">
					<div className="col-xs-6 offset-xs-1">
						<h4> DEBUG </h4>
					</div>
					<div className="col-xs-12">
						<RaisedButton
							label="Log current options"
							onClick={ () => { console.log(this.state) } }
							style={{marginBottom: 16, margin: 16}}
						/>
					</div>
					<div className="col-xs-12">
						<RadioButtonGroup 
							name="which_token" 
							defaultSelected="debugToken"
							onChange= { (event, value) => { this.setState({which_token: value}) } }
							>

							<RadioButton
								value="debugToken"
								label="Use Debug Token (12345)"
								style={ {marginLeft: 16} }
							/>
							<RadioButton
								value="firebaseToken"
								label="Use Firebase Auth Token"
								style={ {marginLeft: 16} }
							/>
						</RadioButtonGroup>
					</div>
					<div className="col-xs-12">
						<TextField 
							hintText="get url" 
							onChange={ e => { this.setState({get_url: e.target.value}) } }
							errorText="example: /game/?sport=nba&date=20150404"
							errorStyle={ {color: 'black' }}
						/>
					</div>
					<div className="col-xs-12">
						<RaisedButton
							label="Submit GET Request"
							onClick={ () => {  this.submitGet() } }
						/>
					</div>
					<div className="col-xs-12">
						<TextField 
							hintText="POST url"
							onChange={ e => { this.setState({post_url: e.target.value}) } }
							errorText="example: /group/create/"
							errorStyle={ {color: 'black' }}
						/>
					</div>
					<div className="col-xs-12">
						<TextField 
							hintText="POST args"
							onChange={ e => { this.setState({post_args: e.target.value}) } }
							errorText="{ sport: 'nba', date: '20161414'}"
							errorStyle={ {color: 'black' }}
						/>
					
					</div>
					<div className="col-xs-12">
						<RaisedButton
							label="Submit POST Request"
							onClick={ () => { this.submitPost() } }
						/>
					
					</div>

					
			</div>
			</Paper>
			
		);
	}
}

export default DebugPanel;
