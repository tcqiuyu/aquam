/**
 * Created by Qiu on 9/9/15.
 */
function loadScript(src, callback) {

	var script = document.createElement("script");
	script.type = "text/javascript";
	if (callback)script.onload = callback;
	document.getElementsByTagName("head")[0].appendChild(script);
	//$.getScript(script)
	script.src = src;
}

loadScript('http://maps.googleapis.com/maps/api/js?v=3&sensor=false&callback=initialize',
	function () {
	});

function initialize() {
	var location = new google.maps.LatLng(40.577635, -105.087074);
	var scott = {
		zoom: 17,
		scrollwheel: false,
		center: location
	};
	var location_map = new google.maps.Map(document.getElementById('location-map'), scott);

	var csuMarker = new google.maps.Marker({
		position: location,
		map: location_map,
		title: "Center for Energy Water Sustainability Laurel St, Fort Collins, CO 80523"
	});
}
//google.maps.event.addDomListener(window, 'load', initialize);