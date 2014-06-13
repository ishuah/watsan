steal("/static/watsan/css/tuktuk.css")
.then(
	'/static/css/extras/typicons.css',
	'/static/watsan/css/colorbrewer.css',
	'/static/watsan/css/map/map.css',
	'/static/watsan/css/map/overlays.css',
	'/static/watsan/css/main.css',
	"/static/watsan/css/header.css")
.then('/static/javascript/loaders/necessities.js')
.then(
	'/static/watsan/javascript/Google.js',
	'/static/watsan/javascript/leaflet.textpath.js')
.then('/static/watsan/javascript/templates/templates.js')
.then(
	'/static/watsan/javascript/models/Map.js',
	'/static/watsan/javascript/models/MapOverlay.js',
	'/static/watsan/javascript/controllers/MapOverlayView.js',
	'/static/watsan/javascript/controllers/MapView.js',
	'/static/watsan/javascript/controllers/SiteView.js',
	'/static/watsan/javascript/controllers/LandmarkView.js',
	'/static/watsan/javascript/controllers/SearchView.js',
	'/static/watsan/javascript/controllers/SiteCardView.js',
	'/static/watsan/javascript/models/Site.js',
	'/static/watsan/javascript/models/Landmark.js',
	'/static/watsan/javascript/models/Road.js',
	'/static/watsan/javascript/models/SewerLine.js',
	'/static/watsan/javascript/models/WaterLine.js',
	'/static/watsan/javascript/models/Village.js')
.then(function(){
	_.mixin(_.str.exports());
	WATSAN.map = new WATSAN.Map();
	WATSAN.overlay = new WATSAN.MapOverlay();
	WATSAN.sitesCount = 1;
	addBaseFeatures();
	addProjectSites();
	$('#loading-overlay').remove();
	WATSAN.sitesCount = WATSAN.sites.length+1;
})
