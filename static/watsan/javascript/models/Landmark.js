WATSAN.Landmark = Backbone.Model.extend({
	defaults: {
		"visible": true,
		"static": true
	},

	initialize: function() {
		var landmark = this;
		this.on('change:static', this.updateMarker);
		WATSAN.map.get('basemap').on('viewreset', function() { landmark.trigger("change:static"); });
	},

	updateMarker: function() {
		var name = this.get('name');
		if (WATSAN.map.get('basemap').getZoom() < 18) {
			var newIcon = new L.divIcon({className: 'landmark ' + this.get('type') });
			if(this.has('marker')) {
			this.get('marker')
				.setIcon(newIcon)
				.on('mouseover', function(e) { this.bindPopup(name, { closeButton: false }).openPopup(); })
				.on('mouseout', function(e) { this.closePopup(); });
			}
		} else {
			var newIcon = new L.divIcon({className: 'landmark ' + this.get('type'), html: "<span class='title'>" + name + "</span>" });
			this.get('marker')
				.setIcon(newIcon)
				.off('mouseover')
				.off('mouseout');
		}
	}
},{
	create: function(name, type, lng, lat) {
		var latlng = new L.LatLng(lat, lng);
		var myIcon = new L.divIcon({className: 'landmark ' + type /*, html: "<span class='title'>" + name + "</span>" */});
		var marker = L.marker(latlng, { icon: myIcon })
			.on('click', function(e) { WATSAN.map.get('basemap').panTo(latlng).setZoom(WATSAN.map.get('basemap').getMaxZoom()); });
			
		var landmark = new WATSAN.Landmark({name: name, type: type, latlng: latlng, marker: marker});
	   	WATSAN.landmarkList.add(landmark);
	   	return landmark;
	}
});

WATSAN.LandmarkList = Backbone.Collection.extend({
	model: WATSAN.Landmark,
});

WATSAN.landmarkList = new WATSAN.LandmarkList();