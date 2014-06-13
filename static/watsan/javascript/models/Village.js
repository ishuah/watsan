WATSAN.Village = Backbone.Model.extend({
	defaults: {
		"visible": true
	},
},{
	create: function(name, pointArray) {
		if (name == 'Kibera') {
			return WATSAN.Village.createKibera(pointArray, name);
		} else {
			var poly = WATSAN.Village.createPolygon(pointArray, name);
			var village = new WATSAN.Village({ name: name, polygon: poly });
		   	WATSAN.villageList.add(village);
	   		return poly;
	   	}
	},

	createPolygon: function(latlngArray, name) {
		return L.polyline(latlngArray, {color: '#ffe900', opacity: 1, clickable: true, stroke: true, fillColor: 'rgba(0,0,0,0)', smoothFactor: 5})
			.setText('          ' + name + '          ', {repeat: true, attributes: {fill: '#ffe900', 'font-size': 25, dy: -10}})
			.on('click', function(e) { WATSAN.map.get('basemap').click(); });
	},

	createKibera: function(latlngArray, name) {
		var kibera = L.polyline(latlngArray, {color: 'white', opacity: 1, clickable: false, stroke: true, fillColor: 'rgba(0,0,0,0)', smoothFactor: 5})
			.setText('          ' + name + '          ', {repeat: true, attributes: {fill: 'white', 'font-size': 25, dy: -10}});
		kibera.addTo(WATSAN.map.get('basemap'));
		return kibera;
	}
});

WATSAN.VillageList = Backbone.Collection.extend({
	model: WATSAN.Village,
});

WATSAN.villageList = new WATSAN.VillageList();