WATSAN.MapOverlayView = Backbone.View.extend({
	events: {
		'click #show-coords.clickable'	: 'showGPSPane',
		'click #show-coords.secondary'	: 'hideGps',
		'click #gps .close'				: 'hideGps',
		'click #search-pane.closed'		: 'showResults',
		'click #search-pane .close'		: 'hideResults',
		'click #enter-coords'			: 'checkCoords'
	},

	showGPSPane: function() {
		$('#coords-pane').slideDown();
		$("#show-coords").addClass('secondary').removeClass('clickable');
	},

	hideGps: function() {
		$('#coords-pane').slideUp();
		$("#show-coords").removeClass('secondary').addClass('clickable');
	},

	hideResults: function() {
		$('#search-list').slideUp();
		$("#search-pane").removeClass('open').addClass('closed');
	},

	showResults: function() {
		$('#search-list').slideDown();
		$("#search-pane").removeClass('closed').addClass('open');
	},

	collapseAllSiteCards: function() {
		var length = WATSAN.sites.length;
		for (s = 0; s < length; s++)
			WATSAN.sites.at(s).get('card').collapse();
	},

	checkCoords: function() {
		var lat = $('#lat-input').val();
		var lng = $('#lng-input').val();
		var regex = /^[\-+]?[0-9]?[0-9]?[0-9]?\.[0-9]*$/;

		if (lat == '' || lng == '')
			alert("You must enter coordinates for both Latitude and Longitude");
		else if (regex.test(lat) && regex.test(lng))
			WATSAN.MapView.attemptSiteCreation(lat, lng);
		else
			alert("The coordinates you entered are not formated properly. Please use decimal form with a - sign for south.")
	}
});