/**
 * Created by Qiu Yu on 6/30/2015.
 */

$(document).ready(function () {
	//When radio button checked/unchecked, toggle background color
	$(".radio-group").on('click', 'input[type=radio]', function () {
		$(this).closest('.radio-group').find('.radio-inline, .solution-radio, .radio').removeClass('checked');
		$(this).closest('.radio-inline, .solution-radio, .radio').addClass('checked');
	});

	//Show additional info when relavent radio button checked
	$('input[type=radio]').click(function () {
		$(this).closest('.chart-panel').find('.additional-info').addClass('hide');
		if($(this).closest('.additional-info-button').length>0) {
			$(this).closest('.chart-panel').find('.additional-info').removeClass('hide');
		}
	})
});