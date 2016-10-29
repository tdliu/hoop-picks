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

function jsDatetoDatestring(date) {
	return "" + date.getFullYear() + (date.getMonth() + 1) + date.getDate();
}

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
	console.log("string: " + jsDatetoDatestring(tomorrow_jsDate));
	var tomorrow = new GoatDate(jsDatetoDatestring(tomorrow_jsDate));

	return tomorrow;
}