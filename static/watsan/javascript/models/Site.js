WATSAN.Site = Backbone.Model.extend({
	defaults: {
		"saved"		: false
	},

	remove: function() {
		var map = WATSAN.map.get('basemap');
		map.removeLayer(this.get('marker'));
		map.removeLayer(this.get('popup'));
		WATSAN.sites.remove(this);
		this.destroy();
	},

	toJSON: function() {
		var json = Backbone.Model.prototype.toJSON.apply(this, arguments);
		json.cid = this.cid;
		return json;
	},

	save: function() {
		if (this.get('name') != '' && this.get('name') != null) {
			var site = this;
			var data = 'POINT(' + site.get('latlong').lng + ' ' + site.get('latlong').lat + ')';
			$.ajax({
				type: "POST",
				url: "site/save/",
				data: 
					{	"coords": data, 
						"name": site.get('name'), 
						"projectId": WATSAN.projectId,
						"color": site.get('color') },
					dataType: "json",
					success: function(response) {
						site.set('id', response.siteId);
					},
					error: function(response) {
						alert("Something went wrong, please try refreshing the page.");
					}
			});
			WATSAN.sitesCount++;
			WATSAN.sites.add(site);
		}
	},

	editName: function(name) {

	}
},{
	create: function(latlong, nearby, pilot_area, sewer_status, water_status, name, id, color) {
		var map = WATSAN.map.get('basemap');
		var site = WATSAN.Site.addSiteToMap(latlong, nearby, pilot_area, sewer_status, water_status, name, id, color);
		site.set('popup', L.popup({ closeButton: false, offset: L.point(0, -40), minWidth: 300 }).setLatLng(latlong));
		site.view = new WATSAN.SiteView({ model: site });

		site.set('layer', map.addLayer(site.get('popup')));
	    map.panTo(latlong);

	   	WATSAN.map.get('basemap').off('click');
		WATSAN.map.get('basemap').on('click', function() { WATSAN.map.get('basemap').openPopup(site.get('popup')) });

	   	return site;
	},

	addSiteToMap: function(latlong, nearby, pilot_area, sewer_status, water_status, name, id, color) {
		var map = WATSAN.map.get('basemap');
		var icon = new L.divIcon({
	 		className: 'svg-marker',
		    html: "<svg class='Blues' width='100%' height='100%'><g>" +
		    		"<path class='stroke " + color + "' d='M6.457474289761293,0A6.457474289761293,6.457474289761293 0 1,1 -6.457474289761293,0C-6.457474289761293,-6.457474289761293 0,-6.457474289761293 0,-19.372422869283877C0,-6.457474289761293 6.457474289761293,-6.457474289761293 6.457474289761293,0Z' transform='translate(20,20)rotate(180)scale(2)'></path>" +
		    		"<path class='" + color + "' d='M6.457474289761293,0A6.457474289761293,6.457474289761293 0 1,1 -6.457474289761293,0C-6.457474289761293,-6.457474289761293 0,-6.457474289761293 0,-19.372422869283877C0,-6.457474289761293 6.457474289761293,-6.457474289761293 6.457474289761293,0Z' transform='translate(20,20)rotate(180)scale(1.6)'></path>" +
		    	"</g></svg>",
		    iconSize: [50, 50],
		    iconAnchor: [20, 50]
	 	});
	 	var marker = L.marker(latlong, { icon: icon }).addTo(map);
		var site = new WATSAN.Site({
			latlong: latlong,
			marker: marker,
			nearby: nearby,
			pilot_area: pilot_area,
			sewer_status: sewer_status,
			water_status: water_status,
			name: name,
			id: id,
			icon: icon,
			color: color });
		return site;
	},

});

WATSAN.SiteList = Backbone.Collection.extend({
	model: WATSAN.Site,
});

WATSAN.sites = new WATSAN.SiteList();
