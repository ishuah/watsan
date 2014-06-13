WATSAN.LandmarkView = Backbone.View.extend({
	events: {
		"click"	: "focus"
	},

	focus: function() {
		var basemap = WATSAN.map.get('basemap');
		var landmark = this.model;

		if (landmark.get('source') == 'google') {
			var searchresult = {"name": landmark.get('name'), "search_engine": landmark.get('source'), "shape": landmark.get('latlng')};	
			searchresult = JSON.stringify(searchresult);

			$.ajax({
				type: "POST",
				url: "/watsan/saveLandmark/",
				data: searchresult,
				dataType: "json",
				contentType: "application/json; charset=utf-8"
			});
			landmark.get('marker').addTo(basemap);
		}else if(!landmark.get('visible')){
			landmark.get('marker').addTo(basemap);
		}

		basemap.panTo(landmark.get('latlng')).setZoom(basemap.getMaxZoom());
	}
});