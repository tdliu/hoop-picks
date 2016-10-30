var MONTHS = ['Null', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec'];

// ------------------ UTILS -------------------//

function jsDatetoDatestring(date) {
	return "" + date.getFullYear() + (date.getMonth() + 1) + date.getDate();
}

function getCurrentTimeEastern() {
	var offset = -4;
	var d = new Date();
    var utc = d.getTime() + (d.getTimezoneOffset() * 60000);
    var nd = new Date(utc + (3600000*offset));
    var timestring12 = nd.toLocaleTimeString();
    var timestring24 = timestring12;
    if (timestring12.indexOf('PM') != -1) {
    	var firstColon = timestring12.indexOf(":");
    	var hour = parseInt(timestring12.substring(0, firstColon)) + 12;
    	timestring24 = "" + hour + ":" + timestring12.substring(firstColon + 1, firstColon + 3);
    }
	return new GoatTime(timestring24);
}

// ----------------- CLASS GOAT TIME --------------//
function GoatTime(timestring) {
	var firstColon = timestring.indexOf(':');
	this.timestring = timestring;
	this.hour = parseInt(timestring.substring(0, firstColon));
	this.minutes = parseInt(timestring.substring(firstColon + 1 , firstColon + 3));
}

GoatTime.prototype.getDifferenceHours = function(other) {
	return other.hour - this.hour + ((other.minutes - this.minutes) / 60);
}

GoatTime.prototype.getPrettyTime = function() {
	var prettytime = "";
	if (this.hour > 12)
		prettytime += (this.hour - 12);
	else 
		prettytime += this.hour;

	prettytime += ":" + this.timestring.substring(3,5);
	if (this.hour > 11)
		prettytime += "pm"
	else 
		prettytime += "am"

	return prettytime;
}


// ----------------- CLASS GOAT DATE --------------//
function GoatDate(datestring) {
	this._datestring = datestring;

	this._year = parseInt(datestring.substring(0,4));
	this._month = parseInt(datestring.substring(4,6));
	this._date = parseInt(datestring.substring(6,8));
	

	var d = new Date();
	d.setMonth(this._month - 1);
	d.setDate(this._date);
	this._jsDate = d;

	this._month_abbrev = MONTHS[this._month];
}

GoatDate.prototype.getMonthAbbrev = function() {
	return this._month_abbrev;
}

GoatDate.prototype.getDateSuffix = function() {
	var suffix = "th";
	if (this._date % 10 == 1) {
		suffix = 'st';
	}
	else if (this._date % 10 == 2) {
		suffix = 'nd';
	}
	else if (this._date % 10 == 3) {
		suffix = 'rd';
	}
	return suffix;
}

GoatDate.prototype.getMonthDateAbbrev = function() {
	return this.getMonthAbbrev() + " " + this._date + this.getDateSuffix();
}

GoatDate.prototype.getDateString = function() {
	return this._datestring;
}

GoatDate.prototype.getTomorrow = function() {
	var tomorrow_jsDate = new Date(this._jsDate);
	tomorrow_jsDate.setDate(tomorrow_jsDate.getDate() + 1);
	var tomorrow = new GoatDate(jsDatetoDatestring(tomorrow_jsDate));

	return tomorrow;
}