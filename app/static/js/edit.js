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

function editStudyPlan (datos) {

	var date = $('#goals_date');

	var current_date = new Date();

	date.min = current_date.getDate() + "-0" + (current_date.getMonth() +1) + "-" + current_date.getFullYear()

	console.log(date.man)

	$('#editStudyPlanModal').on('shown.bs.modal', function(){
		$('#goals_name').trigger('focus');
		$('#goals_name').val(datos.result['0']);
		$('.d-none').val(datos.result['1'])
	});
}

$('document').ready(function() {
})