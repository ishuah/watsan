WATSAN.ProjectsView = Backbone.View.extend({
	events: {
		"click #new-project": "createProject",
	},

	createProject: function() {
		var name = prompt("Please enter a name for your new project (e.g. Latrine Project 2)", "");
		if (name != '' && name != null) {
			var view = this;
			$.post('/project/save/', {'name': name})
				.success(function(response) {
					window.location = "/project/" + response.projectId;
				})
				.error(function() {	alert("Something went wrong, please try reloading the page"); });
		}
		else if (name != null) {
			alert('Your project must have a name.');
			this.createProject();
		}
	},
});