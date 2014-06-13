WATSAN.SiteCardView = Backbone.View.extend({
	initialize: function() {
		this.render();
		this.model.set('card', this);
		this.model.on('remove', function(){ this.remove(); }, this);
	},

	events: {
		'keyup .name_input' 	: 'changeName',
		'click .delete' 		: 'removeSite',
		'click .more.closed'	: 'expand',
		'click .more.open'		: 'collapse', 
	},

	render: function() {
		this.setElement(WATSAN.SiteCardTemplate(this.model.toJSON()));
		this.$el.hide().appendTo("#site-details").fadeIn();
	},

	expand: function() {
		this.$('.extra').slideDown().css('overflow', 'inherit');
		this.$el.removeClass('closed');
		this.$('.more').removeClass('closed').addClass('open').text("Less Detail");
	},

	collapse: function() {
		this.$('.extra').slideUp();
		this.$el.addClass('closed');
		this.$('.more').removeClass('open').addClass('closed').text("More Detail");
	},

	removeSite: function() {
		var view = this;
		if (confirm('Are you sure you want to delete this site?')) {
			if(this.model.get('id')){
				$.post('site/delete/', { "id": this.model.get('id') })
				.success(function(){
					view.$el.fadeOut(function() {
						view.remove();
						view.model.remove();
					});
				})
				.error(function(){
					alert("Something went wrong, please try reloading the page");
				});
			} else {
				view.remove();
				view.model.remove();
			}
		}
	},

	changeName: function(e){
		if (this.$('.name_input').val() != '') {
			this.model.set('name', this.$('.name_input').val());
			$.post("site/edit/", { "id": this.model.get('id'), "name": this.model.get('name')});
		}
	}
});