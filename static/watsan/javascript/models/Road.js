WATSAN.Road = Backbone.Model.extend({
	defaults: {
		"visible": true
	},
},{
	create: function(name, type, line) {
		if (name == 'Uganda Railway')
			line.setStyle({color: '#333'});
		var road = new WATSAN.Road({ name: name, type: type, line: line });
	   	WATSAN.roadList.add(road);
	},

	createPolyLine: function(latlngArray) {
		return L.polyline(latlngArray, {color: 'white', clickable: false});
	}
});

WATSAN.RoadList = Backbone.Collection.extend({
	model: WATSAN.Road,
});

WATSAN.roadList = new WATSAN.RoadList();