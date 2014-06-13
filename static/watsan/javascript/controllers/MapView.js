WATSAN.MapView = Backbone.View.extend({
	initialize: function(){
		WATSAN.map.get('basemap').on('click', this.mapClick);
	},

	events: {
		'focus .opt-input'			: 'clearPlaceholder',
		'blur .opt-input'			: 'setPlaceholder'
	},

	mapClick: function(e) {
		var latlong = new L.LatLng(e.latlng.lat, e.latlng.lng)
		WATSAN.MapView.attemptSiteCreation(latlong.lat, latlong.lng);
	},

	clearPlaceholder: function(ev) {
		var input = $(ev.target);
		var placeholderValue = input.attr('placeholder');
		input.attr('placeholder', '');
		input.attr('data-placeholder', placeholderValue);
	},

	setPlaceholder: function(ev) {
		var input = $(ev.target);
		var placeholderValue = input.attr('data-placeholder');
		input.attr('placeholder', placeholderValue);
	},
},{
	attemptSiteCreation: function(lat, lng) {
		$.post('check_site/', { 'point': 'POINT('+ lng +' '+ lat +')'})
			.done(function(data) {
				if (data.iswithin == "true") {
					var nearby = data['landmarks'];
					var pilot_area =  data['pilot_area'];
					var sewer_status = data['sewer_status'];
					var water_status = data['water_status'];
					var name = 'Site-' + WATSAN.sitesCount;
					var color = WATSAN.MapView.getColor();
					WATSAN.Site.create((new L.LatLng(lat, lng)), nearby, pilot_area, sewer_status, water_status, name, null, color);
	    		} else {
					alert('Point is not within the pilot areas');
				}
			})
			.error(function(data) { alert('An error occured, please try again'); });
	},

	getColor: function(){
		var count = WATSAN.sitesCount;
		if(count > WATSAN.site_colors.length-1)
			while(count > WATSAN.site_colors.length - 1) { count = count - (WATSAN.site_colors.length - 1); }
		return WATSAN.site_colors[count];
	}
})
