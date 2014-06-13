WATSAN.ConfirmedSite = _.template(""+
	"<div>"+
	"<p>Your possible site! </p>"+
	"<p>GPS Coordinates <br> Lat: <%= latlong.lat %> <br> Lng: <%= latlong.lng %></p>"+
	"<footer style='margin: 5px 0; text-align:center;'>"+
	"<button class='btn alert wrong'>Remove</button>"+
	"</footer>"+
	"</div>")