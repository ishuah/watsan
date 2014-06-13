WATSAN.MapOverlay = Backbone.Model.extend({
	defaults: {
		'runningSearchRequest': false
	},

	initialize: function() {
		this.view = new WATSAN.MapOverlayView({el: $('#overlay'), model: this});
		this.searchView = new WATSAN.SearchView({ el: $('#search-pane') });

		WATSAN.sites.on("add remove", this.togglePopup, this);
	},

	togglePopup: function() {
		if (WATSAN.sites.length > 0) {
			$("#instructions-popup").remove();
			if (!$("#back-popup").length > 0)
				$("#popup-space").append("<a href='/watsan/project/" + WATSAN.projectId + "' class='popup' id='back-popup'>Click to view the next steps</a>").hide().fadeIn();
		} else if (WATSAN.sites.length <= 0) {
			$("#back-popup").remove();
			if (!$("#instructions-popup").length > 0)
				$("#popup-space").append("<p class='popup' id='instructions-popup'>Click within the yellow borders to check availability and estimated cost of connections in those areas.</p>").hide().fadeIn();
		}
	},
});