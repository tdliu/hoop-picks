import axios from 'axios';

class ApiConnector {

	sendGetRequest(url, config, callback) {
		axios.get(url, config)
			.then(res => {
				if (callback)
					callback(res);
			})
			.catch(function(error) {
				console.log(error);
			});
	}

	sendPostRequest(url, params, config, callback) {
		axios.post(url, params, config)
			.then(res => {
				callback(res);
			});
	}
	

	createAuthorizationHeader(token) {
		return { 
			authorization: 'Bearer ' + token
		};
	}

	createDebugAuthorizationHeader() {
		return { 
			authorization: 'Bearer ' + '12345'
		};
	}

	createAuthConfig(token, debug) {
		if (debug) {
			return {
				headers: this.createDebugAuthorizationHeader()
			}
		}
		return {
			headers: this.createAuthorizationHeader(token)
		}
	}

	//USERS
	getUser(token, callback) {
		var url = '/user/';
		var config = this.createAuthConfig(token);
		this.sendGetRequest(url, config, callback);
	}

	//EVENTS
	getEvents() {
		console.log("FETCH EVENTS")
	}

	//GROUPS
	getGroupAsGroupOwner(token, group_id, callack) {
		var url ='/group/';
		var config = this.createAuthConfig(token);
		this.sendGetRequest(url, config, callback);
	}

	getGroupAsMember(group_id, callback) {
		var url ='/group/';
		this.sendGetRequest(url, {}, callback)
	}

	createGroup(token, params, callback) {
		var url = '/group/create/';
		var config = this.createAuthConfig(token);
		axios.post(url, params, config)
			.then(res => {
				callback(res);
			});
	}
}

export default new ApiConnector();