$('docuemnt').ready(function () {

	var today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());

 //    $(function() {
	//   $('input[id="startDate"]').daterangepicker({
	//   		timePicker: true,
	//   		startDate: moment().startOf('hour'),
 //    		endDate: moment().startOf('hour').add(32, 'hour'),
	// 	    singleDatePicker: true,
	// 	    showDropdowns: true,
	// 	    minYear: today,
	// 	    maxYear: parseInt(moment().format('YYYY'),10)
	// 	});
	// });

	// $(function() {
	//   $('input[id="startDate"]').daterangepicker({
	//     timePicker: true,
	//     startDate: today,
	//     endDate: moment().startOf('hour').add(32, 'hour'),
	//     locale: {
	//       format: 'M/DD hh:mm A'
	//     }
	//   });
	// });

	$(function () {
        $('#startDate').datetimepicker({
            locale: 'ru'
        });
    });
});