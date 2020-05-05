function qualification(dato) {

    event.preventDefault();

    $('#subject').val(dato[0]);
    $('#id').val(dato[1]);
};


function editSubjects(dato) {

    event.preventDefault();

    $('#subject').val(dato[0]);
    $('#id').val(dato[1]);
}

function assignTeacher(dato) {

	$('.subjects').val(dato[0]);
	$('.d-none').val(dato[1]);
}

function editTeachers(dato) {

	$('.d-none').val(dato[0]); // get the id
	$('.teacher').val(dato[1]); // get the teacher  name
	$('.email').val(dato[2]); // get the email.
	$('.phone').val(dato[3]); // get the phone number

	$('#editTeachers').on('shown.bs.modal', function(){
		$('.teacher').trigger('focus');
	});
}