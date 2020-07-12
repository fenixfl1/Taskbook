$('docuemnt').ready(function () {

	$(function () {

		$('#datetime1').datepicker({
			format: "dd/mm/yyyy",
		});

		$('#datetime2').datepicker({
			format: "dd/mm/yyyy",
		});

        $('#datetime1').datetimepicker();
        $('#datetime2').datetimepicker();
    });
});