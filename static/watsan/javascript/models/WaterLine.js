WATSAN.WaterLine = Backbone.Model.extend({
	defaults: {
		"visible": true
	},
},{
	create: function(name, line) {
		var waterline = new WATSAN.WaterLine({ name: name, line: line });
	   	WATSAN.waterList.add(waterline);
	},

	createPolyLine: function(latlngArray) {
		return L.polyline(latlngArray, {color: 'blue', clickable: false});
	}
});

WATSAN.WaterList = Backbone.Collection.extend({
	model: WATSAN.WaterLine,
});

WATSAN.waterList = new WATSAN.WaterList();