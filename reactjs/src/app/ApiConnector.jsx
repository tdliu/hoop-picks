import axios from 'axios';

class ApiConnector {

	//USERS
	getUser(user, userIdToken, callback) {
		var url = '/user/?user_id=' + user.uid;
		var config = {
			headers: {
				authorization: 'Bearer ' + userIdToken,
			}
		}
		axios.get(url, config)
			.then(res => {
				callback(res);
			})
			.catch(function(error) {
				console.log(error);
			});
	}

	//EVENTS
	getEvents() {
		console.log("FETCH EVENTS")
	}

	
}

export default new ApiConnector();