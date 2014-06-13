WATSAN.SiteView = Backbone.View.extend({
	initialize: function(){
		this.render();
	},

	events: {
		'click .save' : 'accept',
		'click .close' : 'removeSite'
	},

	render: function(){
		var view = this;
		this.setElement(WATSAN.UnconfirmedSite(this.model.toJSON()));
		this.model.get('popup').setContent(this.el);
	},

	accept: function() {
		this.model.save();
		new WATSAN.SiteCardView({ model: this.model });
		this.setElement(WATSAN.ConfirmedSite(this.model.toJSON()));
		this.changePopup();
	},

	changePopup: function() {
		var site = this.model;
		WATSAN.map.get('basemap').off('click');
		WATSAN.map.get('basemap').removeLayer(site.get('popup'));

		var popup = L.popup({ offset: L.point(0, -40), minWidth: 300 })
			.setLatLng(site.get('latlong'))
			.setContent(this.el);
		site.set('popup', popup);
		// site.get('marker').setPopup(popup);
		WATSAN.map.get('basemap').on('click', WATSAN.map.view.mapClick);
	},

	removeSite: function(){
		WATSAN.map.get('basemap').off('click');
		WATSAN.map.get('basemap').removeLayer(this.model.get('popup'));
		this.remove();
		this.model.remove();
		WATSAN.map.get('basemap').on('click', WATSAN.map.view.mapClick);
	}
})