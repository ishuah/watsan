WATSAN.SewerLine = Backbone.Model.extend({
	defaults: {
		"visible": true
	},
},{
	create: function(name, line) {
		var sewerline = new WATSAN.SewerLine({ name: name, line: line });
	   	WATSAN.sewerList.add(sewerline);
	},

	createPolyLine: function(latlngArray) {
		return L.polyline(latlngArray, {color: 'brown', clickable: false});
	}
});

WATSAN.SewerList = Backbone.Collection.extend({
	model: WATSAN.SewerLine,
});

WATSAN.sewerList = new WATSAN.SewerList();