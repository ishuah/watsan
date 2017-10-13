steal('/static/javascript/tools/jquery.js')
	.then(
		'/static/javascript/tools/d3.v3.min.js',
		'/static/css/map/map.css')
	.then(function() {
		// var width = $( window ).width();
		// var height = $( window ).height();
		// var interval = 12000;
		// radius = 100;
		// radiusWidth = 20;

		// var arc = d3.svg.arc()
		// 	.startAngle(0)
		// 	.innerRadius(90)
		// 	.outerRadius(120);

		// var svg = d3.select("#spinner").insert("svg", ":first-child")
		// 		.attr("width", width)
		// 		.attr("height", height)
		// 	.append("g")
		// 		.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

		// var meter = svg.append("g")
		//     .attr("class", "progress-meter");

		// meter.append("path")
		//     .attr("class", "staticBack")
		//     .attr("d", arc.innerRadius(radius - radiusWidth - 10).outerRadius(radius + radiusWidth + 10).endAngle(2*Math.PI));

		// var background = meter.append("path")
		//     .attr("class", "background")
		//     .attr("d", arc.innerRadius(radius - radiusWidth).outerRadius(radius + radiusWidth).endAngle(2*Math.PI));

		// var foreground = meter.append("path")
		//     .attr("class", "foreground");

		// $("#spinner").fadeIn();

		// (function spin() {
		// 	var i = d3.interpolate(0, 6);
		//  	d3.transition().duration(interval).tween("progress", function() {
		//         return function(t) {
		//         	var p = i(t);
		// 			foreground
		// 				.attr("d", arc.startAngle(2*Math.PI * Math.floor(p)).endAngle(2*Math.PI * p))
		// 				.attr('class', function() {
		// 					if (Math.floor(p) % 2) return 'foreground dark';
		// 					else return 'foreground';
		// 				});
		// 			background.attr('class', function() {
		// 					if (Math.floor(p) % 2) return 'background';
		// 					else return 'background dark';
		// 				});
		//         };
		//     });
		//     setTimeout(spin, interval);
		// })();
	setTimeout(function() {
		$("#gif-spinner").append("<div class='text'>Still Working... This may take some time</div>");
		setTimeout(function() {
			$("#gif-spinner .text").text("Still Working... This may take some time");
		}, 12000);
	}, 12000);
}).then(
		'/static/javascript/loaders/apis.js',
		'/static/javascript/tools/underscore-min.js')
	.then('/static/javascript/tools/underscore.string.min.js')
	.then('/static/javascript/tools/backbone-min.js')