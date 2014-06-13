steal(
	'/static/javascript/tools/jquery.js',
	"/static/watsan/css/tuktuk.css",
	"/static/watsan/css/dash/projects.css",
	"/static/watsan/css/main.css",
	"/static/watsan/css/header.css")
.then('/static/css/extras/typicons.css')
.then('/static/javascript/tools/underscore-min.js')
.then('/static/javascript/tools/underscore.string.min.js')
.then('/static/javascript/tools/backbone-min.js')
.then(
	'/static/watsan/javascript/controllers/ProjectsView.js',
	'/static/watsan/javascript/models/Project.js',
	'/static/watsan/javascript/models/Site.js')
.then(function() {
	new WATSAN.ProjectsView({ el: $('#projects') });
});
