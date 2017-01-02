var authUi = new firebaseui.auth.AuthUI(firebase.auth());
var userIdToken;

var uiConfig = {
	callbacks: {
      signInSuccess: function(currentUser, credential, redirectUrl) {
        console.log("CURRENT USER: ", currentUser);
        return true;
      }
    },
    'signInSuccessUrl' : '/',
	'signInOptions': [
		firebase.auth.GoogleAuthProvider.PROVIDER_ID,
		firebase.auth.TwitterAuthProvider.PROVIDER_ID,
		firebase.auth.EmailAuthProvider.PROVIDER_ID,
		firebase.auth.FacebookAuthProvider.PROVIDER_ID,
	],
	tosUrl: 'http://www.google.com'
};

function handleAuthStateChanged(user) {
	console.log('auth state changed on signin page');
}

authUi.start('#firebaseui-auth', uiConfig);
firebase.auth().onAuthStateChanged( function(user) {
	handleAuthStateChanged(user);
});;