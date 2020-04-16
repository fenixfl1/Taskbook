// $(document).ready(function() {

//     var answers;

//     $('#crear').on('click', function() {

//         var steps = [{
//                 //ask for and validate email here
//                 type: 'question',
//                 title: 'Titulo del plan de estudio',
//                 html: `<div class="form-group">
//                             <input type="text" required class="form-control-lg form-control" id=name>
//                         </div>`
//             },
//             {
//                 //ask for and validate text input here
//                 type: 'question',
//                 title: 'Seleciona los dias que vas a estudiar',
//                 html: `<div id="group" class="btn-group">
//                             <label for="sun" class="btn btn-sm btn-info">Sun
//                                 <input type="checkbox" id="sun" class="badgebox"><span class="badge">&check;</span>
//                             </label>

//                             <label for="mon" class="btn btn-info btn-sm">Mon
//                                 <input type="checkbox" id="mon" class="badgebox"><span class="badge">&check;</span>
//                             </label>

//                             <label for="tue" class="btn btn-info btn-sm">Tue
//                                 <input type="checkbox" id="tue" class="badgebox"><span class="badge">&check;</span>
//                             </label>

//                             <label for="wed" class="btn btn-info btn-sm">Wed
//                                 <input type="checkbox" id="wed" class="badgebox"><span class="badge">&check;</span>
//                             </label>

//                             <label for="thu" class="btn btn-info btn-sm">Thu
//                                 <input type="checkbox" id="thu" class="badgebox"><span class="badge">&check;</span>
//                             </label>

//                             <label for="fri" class="btn btn-info btn-sm">Fri
//                                 <input type="checkbox" id="fri" class="badgebox"><span class="badge">&check;</span>
//                             </label>

//                             <label for="sat" class="btn btn-info btn-sm">Sat
//                                 <input type="checkbox" id="sat" class="badgebox"><span class="badge">&check;</span>
//                             </label>
//                         </div>`
//             },
//             {
//                 type: 'question',
//                 title: 'Seleciona tu horario',
//                 html: `<div class="form-row text-center mx-auto">
//                             <div class="btn">
//                                 <input placeholder="Selected time" type="text" id="myTimePicker" class="form-control timepicker">
//                                 <label for="start">Inicio</label>
//                                 <input type="time" name="start" class="btn-lg btn" id="manual-operations-input">
//                             </div>

//                             <div class="btn">
//                                 <label for="end">fin</label>
//                                 <input type="time" name="end" class="btn-lg btn" id="manual-operations-input">
//                             </div>
//                         </div>`
//             }
//         ];
//         Swal.mixin({
//             confirmButtonText: 'Next',
//             showCancelButton: true,
//             progressSteps: ['1', '2', '3']

//         }).queue(steps).then((result) => {
//             // Swal({
//             //     type: 'success',
//             //     html: 'Email successfully sent to: '
//             // });
//             if (result.value) {
//                 var title = $('#name').serialize();

//                 answers = result.value;
//                 Swal.fire({
//                     title: 'All done!',
//                     html: `Your answers:
//                         <pre><code>${title}</code></pre>`,
//                     confirmButtonText: 'Ceptar!'
//                 });
//             };
//         }).finally(function() {
//             $.ajax({
//                 method: "POST",
//                 url: "taskbook.com:5555/register-study-plan",
//                 data: $(answers).serialize(),
//                 dataType: "json",
//                 success: function(response) {
//                     location.reload();
//                 },
//                 error: function(response) {
//                     alert('No fue posible guadar el plan de estudios');
//                 }
//             });
//         })
//     });
// });

$(document).ready(function() {

    $('#crear').on('click', function() {
        $('#studyPlan').modal('show');
    });

});