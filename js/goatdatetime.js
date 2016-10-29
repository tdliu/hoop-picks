var MONTHS = ['Null', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec'];

function getPrettyTime(time) {
	var prettytime = "";
	var hour = parseInt(time.substring(0,2));
	if (hour > 12)
		prettytime += (hour - 12);
	else 
		prettytime += hour;

	prettytime += time.substring(2, 5);
	if (hour > 11)
		prettytime += "pm"
	else 
		prettytime += "am"

	return prettytime
}

function GoatDate(datestring) {
	this._datestring = datestring;
	var year = datestring.substring(0,4);
	var month = datestring.substring(4,6);
	var date = datestring.substring(6,8);

	this._month = parseInt(month);
	this._date = parseInt(date);
	this._year = parseInt(year);

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