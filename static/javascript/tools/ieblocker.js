var IE = (navigator.userAgent.indexOf("MSIE") >= 0) ? true : false;
if (IE) {
	$(function() {
		$("<div>").css({
			'position': 'absolute',
			'top': '0px',
			'left': '0px',
			backgroundColor: 'black',
			'opacity': '0.75',
			'width': '100%',
			'height': $(window).height(),
			zIndex: 5000
		}).appendTo("body");
			
		$("<div><img src='/static/images/no-ie.png' alt='' style='float: left;'/><p><br /><strong>Sorry! We use state of the art javascript which is not supported by Internet Explorer.</strong><br /><br />If you'd like to use our app please download <a href='http://getfirefox.org'>Firefox</a> or <a href='http://google.com/chrome'>Chrome</a>.</p>")
			.css({
				backgroundColor: '#e3e4d8',
				'top': '50%',
				'left': '50%',
				marginLeft: -260,
				marginTop: -100,
				width: 510,
				paddingRight: 10,
				height: 200,
				'position': 'absolute',
				zIndex: 6000,
				borderRadius: '5px'
			}).appendTo("body");
	});		
}