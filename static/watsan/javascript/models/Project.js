WATSAN.Project = Backbone.Model.extend({
	defaults: {
		"step": 1
	},

	initialize: function() {
		this.get('sites').on('add', function(site) { this.addSite(site); }, this);

		this.get('sites').on('remove', function() {
			if (this.get('sites').length <= 0)
				this.removeSiteTable();
		}, this);

		this.on('change:step', this.stepChange, this);
	},

	addSite: function(site) {
		this.get('element').find('.no-sites').remove();
		if(site.get('sewerline_cost') == 'False'){
			var sewer_line_info = "<td>Not possible.</td>";
		}else{
			var sewer_line_info = "<td> Est. cost: "+ _.str.numberFormat(parseFloat(site.get('sewerline_cost'))) +" Ksh <br> Distance:"+ _.str.numberFormat(parseFloat(site.get('sewerline_distance'))) +"m</td>";
		}

		if(site.get('waterline_cost') == 'False'){
			var water_line_info = "<td>Not possible.</td>"
		}else{
			var water_line_info = "<td> Est cost:"+ _.str.numberFormat(parseFloat(site.get('waterline_cost'))) +" Ksh<br> Distance:"+ _.str.numberFormat(parseFloat(site.get('waterline_distance'))) +"m </td>";
		}
		
		
		this.get('element').find('.site-table table').append("<tr><td>" + site.get('name') + "</td><td>"+ site.get('village') +"</td>"+sewer_line_info+water_line_info+"<td>"+ site.get('landmarks') +"</td></tr>");
		if (this.get('step') < 3)
			this.set('step', 3);
	},

	removeSiteTable: function() {
		this.get('element').find('.site-table').content("<table><tr class='no-sites'><td>You haven't chosen any sites yet</td></tr></table>");
		if (this.get('step') >= 2)
			this.set('step', 1);
	},

	stepChange: function() {
		this.get('element').find('.step').addClass('incomplete');
		for (var i = 1; i <= this.get('step'); i++) {
			this.get('element').find('.step._' + i).removeClass('incomplete');
		}
	},
});