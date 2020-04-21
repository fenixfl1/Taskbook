$(document).ready(function() {

	$('.checked').on('click', function() {

		if( $('.badgebox').prop('checked') === true ) {
			$('#label').removeClass('d-none');
	    	$('#calificacion').removeClass('d-none');
	    	$('#calificacion').prop('required', 'required');
		} else{
			$('#label').addClass('d-none');
	    	$('#calificacion').addClass('d-none');
	    	$('#calificacion').removeAttr('required')
		}
	});
})