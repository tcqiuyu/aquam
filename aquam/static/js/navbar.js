jQuery(document).ready(function ($) {
	//set some variables
	var isAnimating = false,
		firstLoad = false,
		newScaleValue = 1;

	//cache DOM elements
	var dashboard = $('.cd-side-navigation'),
		mainContent = $('.cd-main'),
		loadingBar = $('#cd-loading-bar');

	if ($('.cd-side-navigation .selected').length == 0) {
		var pathname = window.location.pathname; // Returns path only
		dashboard.find('*[data-menu="' + pathname.split("/")[1]
			+ '"]').addClass('selected').parent('li').siblings('li').children('.selected').removeClass('selected');
	}

	// select a new section
	dashboard.on('click', 'li a', function (event) {
		event.preventDefault();
		var target = $(this),
		//detect which section user has chosen
			sectionTarget = target.data("menu");
		if (!isAnimating) {
			//if user has selected a section different from the one already visible - load the new content
			triggerAnimation(sectionTarget, true);
		}
		firstLoad = true;

	});

	//scroll to content if user clicks the .cd-scroll icon
	mainContent.on('click', '.cd-scroll', function (event) {
		event.preventDefault();
		var scrollId = $(this.hash);
		//console.log(scrollId);
		$(scrollId).velocity('scroll', {container: $(".cd-section")}, 200);
	});

	//detect the 'popstate' event - e.g. user clicking the back button
	$(window).on('popstate', function () {
		if (firstLoad) {
			/*
			 Safari emits a popstate event on page load - check if firstLoad is true before animating
			 if it's false - the page has just been loaded
			 */
			var newPageArray = location.pathname.split('/'),
			//this is the url of the page to be loaded
				newPage = newPageArray[newPageArray.length - 1].replace('.html', '');
			if (!isAnimating) triggerAnimation(newPage, false);
		}
		firstLoad = true;
	});

	//start animation
	function triggerAnimation(newSection, bool) {
		isAnimating = true;
		newSection = ( newSection == '' ) ? 'index' : newSection;
		//update dashboard
		dashboard.find('*[data-menu="' + newSection + '"]').addClass('selected').parent('li').siblings('li').children('.selected').removeClass('selected');
		//trigger loading bar animation
		initializeLoadingBar(newSection);
		//load new content
		loadNewContent(newSection, bool);
	}

	function initializeLoadingBar(section) {
		var selectedItem = dashboard.find('.selected'),
			barHeight = selectedItem.outerHeight(),
			barTop = selectedItem.offset().top,
			windowHeight = $(window).height(),
			maxOffset = ( barTop + barHeight / 2 > windowHeight / 2 ) ? barTop : windowHeight - barTop - barHeight,
			scaleValue = ((2 * maxOffset + barHeight) / barHeight).toFixed(3) / 1 + 0.001;

		//place the loading bar next to the selected dashboard element
		loadingBar.data('scale', scaleValue).css({
			height: barHeight,
			top: barTop
		}).attr('class', '').addClass('loading ' + section);
	}

	function loadNewContent(newSection, bool) {
		var new_scripts_src = [];

		setTimeout(function () {
			//animate loading bar
			loadingBarAnimation();

			//var script = document.getElementsByTagName('script');
			//var old_scripts = $.extend(true, {}, script);
			//var old_scripts_src = [];
			//for (i = 0; i < old_scripts.length; i++) {
			//    old_scripts_src.push(old_scripts[i].src);
			//}
			//create a new section element and insert it into the DOM
			var section = $('<section class="cd-section overflow-hidden ' + newSection + '"></section>').appendTo(mainContent);
			//load the new content from the proper html file
			section.load("http://localhost:8000/" + newSection, function (event) {
				//var new_scripts = document.getElementsByTagName('script');
				//console.log(new_scripts);
				//for (i = 0; i < new_scripts.length; i++) {
				//    tmp = new_scripts[i].src;
				//    new_scripts_src.push(tmp);
				//}

				//console.log(tmp);
				//if(old_scripts_src.indexOf(tmp)==-1) {
				//$("head *").addClass("new_added");
				//}
				//console.log(new_scripts_src);

				//var added_scripts =
				//finish up the animation and then make the new section visible
				//console.log($(this).find(".js"));
				//$(this).find(".js").each(function (i) {
				//    console.log($(this).context.src);
				//
				//    scripts.push($(this).context.src);
				//});

				//section.load(newSection + ' .cd-section > *', function (event) {

				//var len = scripts.length;
				//for (var i = 0; i < len; i++) {
				//    $.getScript("http://localhost:8000/static/js/init_contact_map.js");
				//}

				section.html(section.find('.cd-section').html());
				//section.find()
				var scaleMax = loadingBar.data('scale');
				loadingBar.velocity('stop').velocity({
					scaleY: scaleMax
				}, 400, function () {
					//add the .visible class to the new section element -> it will cover the old one
					section.prev('.visible').removeClass('visible').end().addClass('visible').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function () {
						resetAfterAnimation(section);
					});

					//if browser doesn't support transition
					if ($('.no-csstransitions').length > 0) {
						resetAfterAnimation(section);
					}

					var url = "http://localhost:8000/" + newSection;
					if (url != window.location && bool) {
						//add the new page to the window.history
						//if the new page was triggered by a 'popstate' event, don't add it
						window.history.pushState({path: url}, '', url);
					}
					//var pathname = window.location.pathname; // Returns path only
					//console.log(pathname.split("/")[1]);
					dashboard.find('*[data-menu="' + newSection
						+ '"]').addClass('selected').parent('li').siblings('li').children('.selected').removeClass('selected');

					$.getScript("http://localhost:8000/static/js/" + newSection + ".js");

					$("head [src]:not(.new_added):not(img)").remove();
					$("head [type='text/css']:not(.new_added)").remove();
				});

				//});
			});

		}, 50);
		//console.log(new_scripts_src);
	}

	function loadingBarAnimation() {
		var scaleMax = loadingBar.data('scale');
		if (newScaleValue + 1 < scaleMax) {
			newScaleValue = newScaleValue + 1;
		} else if (newScaleValue + 0.5 < scaleMax) {
			newScaleValue = newScaleValue + 0.5;
		}
		loadingBar.velocity({
			scaleY: newScaleValue
		}, 100, loadingBarAnimation);
	}

	function resetAfterAnimation(newSection) {
		//once the new section animation is over, remove the old section and make the new one scrollable
		newSection.removeClass('overflow-hidden').prev('.cd-section').remove();
		isAnimating = false;
		//reset your loading bar
		resetLoadingBar();
	}

	function resetLoadingBar() {
		loadingBar.removeClass('loading').velocity({
			scaleY: 1
		}, 1);
	}

});