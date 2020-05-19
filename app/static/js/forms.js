$(document).ready(function () {

	// function to validate form of create new teachers
	$('#submitTeacher').on('click', function() {

		var name = $('#teacher-name');
		var email = $('#teacher-email');
		var phone = $('#teacher-phone');

		if (name.val() == null || name.val().length == 0 || /^\s+$/.test(name.val())) {

			name.addClass('is-invalid');
			name.attr('placeholder', 'El nombre es obligatorio!');
			return false;
		} else if ( name.hasClass('is-invalid')) {

			name.removeClass('is-invalid');
			name.addClass('is-valid');
		}

		if ( email.val().length > 0 ) {

			if (!(/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)/.test(email.val())) ) {

				email.addClass('is-invalid');
				email.attr('placeholder', 'Correo no valido!');
				return false
			} else if ( email.hasClass('is-invalid')) {

				email.removeClass('is-invalid');
				email.addClass('is-valid');
			}
		}

		if ( phone.val().length > 0 && !(/^\d{9}$/.test(phone.val())) ) {

			phone.addClass('is-invalid');
			phone.attr('placeholder', 'Numero no valido!');
			return false;

		} else if ( phone.hasClass('is-invalid')) {

			phone.removeClass('is-invalid');
			phone.addClass('is-valid');
		}

		return true
	})

    // function to validate form of edit teachers
	$('#submitEdirTeacher').on('click', function() {

		var id = $('#token');
		var phone = $('.phone');
		var name = $('.teacher');
		var email = $('.email');

		if ( id.val() == null || id.val().length == 0 || /^\s+$/.test(id.val()) ) {

			alert('Es imposible enviar el formulario sin un id' + '' + id.val());
		  	return false;
		}

		if ( name.val() == null || name.val().length == 0 || /^\s+$/.test(name.val()) ) {

			name.addClass('is-invalid');
			name.attr('placeholder', 'El nombre es obligatorio!');
		  	return false;

		} else if ( name.hasClass('is-invalid')) {

			name.removeClass('is-invalid');
			name.addClass('is-valid');
		}

		if (email.val().length > 0){

			if (!(/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)/.test(email.val())) ) {

				email.addClass('is-invalid');
				email.attr('placeholder', 'Correo no valido!');
				return false
			}
		} else if ( email.hasClass('is-invalid') || email.val() == null ) {

			email.removeClass('is-invalid');
			email.attr('placeholder', '');
		}

		if ( phone.val().length > 0 ) {

			if ( !(/^\d{9}$/.test(phone.val())) ) {
				phone.addClass('is-invalid');
				phone.attr('placeholder', 'Numero no valido!');
				return false;
			} 
		} else if ( phone.hasClass('is-invalid') || phone.val() == null ) {

			phone.removeClass('is-invalid');
		}

		return true;
	})
	
})