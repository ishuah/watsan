WATSAN.Map = Backbone.Model.extend({
	initialize: function() {
		WATSAN.map = this;
		basemap = L.map('map_canvas', { 
			zoomControl: false,
			minZoom: 15,
			maxBounds: L.latLngBounds([[-1.32528, 36.77386], [-1.29889, 36.80873]])
		}).setView([-1.31206, 36.78873], 16);
		this.set('basemap', basemap);
		this.view = new WATSAN.MapView({ model: this });

		this.addLayers(basemap);
		this.addControls(basemap);

		var header_height = $('header').height() + 20;
		$("#map").css({ 'top': header_height });
	},

	addLayers: function(map) {
		var satellite = new L.Google('HYBRID');
		map.addLayer(satellite);
		this.set('satLayer', satellite);
		// var mapbox = L.mapbox.tileLayer('davkutalek.map-m44e15tr', {opacity: 0.5}).addTo(map).bringToFront();
		// this.set('mapboxLayer', mapbox);
	},

	addControls: function(map) {
		map.zoomControl = L.control.zoom({position: 'topleft'}).addTo(map);

		var CenterControl = L.Control.extend({
		    options: { position: 'topleft' },

		    onAdd: function (map) {
		        var container = L.DomUtil.create('a', 'typicn typcn-radar custom-control');
		        $(container)
		        	.css({ 'cursor': 'pointer'})
		        	.attr('title', "Click to center on Kibera")
		        	.on('click', function(e) {
			        	map.panTo([-1.31206, 36.78873]);
			        	e.stopImmediatePropagation();
			        });
		        return container;
		    }
		});
		map.addControl(new CenterControl());
	},
})