WATSAN.SearchView = Backbone.View.extend({
	initialize: function() {
		this.collection = new WATSAN.LandmarkList();
		this.collection.on('add', this.addLandmarkToList);
		this.collection.on('reset', this.resetLandmarkList);
	},
	
	events: {
		"keyup #search_box"		: "checkKey",
		"click a"				: "search",
		"click #clear-search"	: "clearBox"
	},

	checkKey: function(e) {
		if (e.keyCode == 13) this.search();
	},
	
	search: function() {
		var searchString = this.$("#search_box").val();
		if (searchString && searchString != '') {
			this.clear();
			$('#search-icon').removeClass('typicn').removeClass('typcn-zoom').addClass('loading');
			this.$('.close').show();

			var matches = WATSAN.landmarkList.filter(function(landmark) {
				return landmark.get('name').toLowerCase().indexOf(searchString.toLowerCase()) >= 0; 
			});
			if (matches.length < 3)
				var googleResults = this.searchGoogle(searchString, matches.length);
			else
				$('#search-icon').removeClass('loading').addClass('typicn').addClass('typcn-zoom');
			this.collection.add(matches);
			$.ajax({
				type: "POST",
				url: "/watsan/saveSearchString/",
				data: searchString,
				dataType: "text",
				contentType: "text; charset=utf-8"
			});
		} else {
			this.clear();
		}
	},

	searchGoogle: function(searchString, dbResultsLength) {
		var bounds = WATSAN.map.get('basemap').getBounds();
		var sw = new google.maps.LatLng(bounds.getSouth(), bounds.getWest());
		var ne = new google.maps.LatLng(bounds.getNorth(), bounds.getEast());

		var service = new google.maps.places.PlacesService(WATSAN.googleMap);
		var request = {
			bounds: new google.maps.LatLngBounds(sw, ne),
			keyword: searchString
		};
		service.nearbySearch(request, callback);

		var view = this;
		function callback(results, status) {
			if (status == google.maps.places.PlacesServiceStatus.OK) {
				for (var i = 0; i < results.length; i++)
					view.addGooglePlaceToList(results[i]);
			} else if (dbResultsLength == 0) {
				view.addNoMatches();
			}
			$('#search-icon').removeClass('loading').addClass('typicn').addClass('typcn-zoom');
		}
	},

	addLandmarkToList: function(landmark) {
		landmark.view = new WATSAN.LandmarkView({ el: "<li class='result'>" + landmark.get('name') + "</li>", model: landmark });
		$('#search-list').append(landmark.view.$el);
	},

	addGooglePlaceToList: function(place) {
		if (!this.collection.where({name: place.name}).length > 0) {
			var landmark = WATSAN.Landmark.create(place.name, 'x', place.geometry.location.kb, place.geometry.location.jb);
			landmark.set('source', 'google');
			landmark.view = new WATSAN.LandmarkView({ el: "<li class='result'>" + landmark.get('name') + "</li>", model: landmark });
			$('#search-list').append(landmark.view.$el);
		}
	},

	addNoMatches: function() {
		$('#search-list').append("<li id='no-matches'>Sorry, No Matches!</li>");
	},

	resetLandmarkList: function() {
		$('#search-list .result').remove();
	},

	clearBox: function() {
		this.$('#search_box').val('');
		this.clear();
	},

	clear: function() {
		this.collection.each(function(landmark) {
			landmark.view.remove();
		});
		this.collection.reset();
		$('#search-icon').removeClass('loading').addClass('typicn').addClass('typcn-zoom');
		this.$('#no-matches').remove();
		this.$('.close').hide();
		this.$('#search_box').focus();
	},
});