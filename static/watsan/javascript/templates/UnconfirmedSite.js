WATSAN.UnconfirmedSite = _.template(""+
	"<div class='Blues'>"+
		"<a class='color left close'>x</a>"+
		"<p>Save this location?</p>"+
		"<p>Closest Landmarks: <br>" +
			"<span><%= nearby %></span></p>" +
		"<div id='footer'>"+
			"<button class='left btn cancel close'>Cancel</button>"+
			"<button class='right btn save <%= color %>'>Save</button>"+
		"</footer>"+
	"</div>")