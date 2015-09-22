/**
 * Created by Qiu on 9/19/15.
 */
	//$('a[href^="#"]').on('click', function (event) {
	//    console.log("Here");
	//    var target = $(this.href);
	//
	//});
jQuery(document).ready(function ($) {
	$.getScript("https://cdnjs.cloudflare.com/ajax/libs/velocity/1.2.2/velocity.min.js");

	$('#flowchart').on('click', '[href]', function (event) {
		event.preventDefault();
		var scrollId = $($(this).attr('href'));
		//console.log(scrollId);
		$(scrollId).velocity('scroll', {container: $(".cd-section")}, 200);
	});

	//$('#flowchart').on('click', '[href]', function () {
	//    var target = $($(this).attr("href"));
	//    //console.log(target);
	//    if (target.length) {
	//        event.preventDefault();
	//        //console.log($(window).offset());
	//
	//        $('.cd-section').animate({
	//            scrollTop: target.offset().top + 2 * $('header').height() - ($('html').offset().top)
	//        }, 1000);
	//        console.log(target.offset());
	//    }
	//});
});

