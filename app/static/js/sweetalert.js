function sendResponse(data) {
    $.ajax({
        url: "taskbook.com:5555/register-plan",
        method: "POST",
        data: $('#stady-plan').serialize(),
        dataType: "json",
        success: function(response) {

        }
    });
}

$(document).ready(function() {
    $('#btn-delete').on('click', function() {

        var valores = '';

        $('#btn-delete').parents("tr").find("#valor").each(function() {
            valores += $(this).html() + "\n";
            Swal.fire({
                title: valores,
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!'
            }).then((result) => {
                if (result.value) {
                    Swal.fire({
                        text: valores
                    });
                };
            });
        });
    });
});

function studyPlan() {
    Swal.mixin({
        input: 'text',
        confirmButtonText: 'Next &rarr;',
        showCancelButton: true,
        progressSteps: ['1', '2', '3', '4']
    }).queue([{
            title: 'Nombra tu Plan de estudio',
            text: ''
        },
        'Question 2',
        'Question 3'
    ]).then((result) => {
        if (result.value) {
            const answers = JSON.stringify(result.value)
            Swal.fire({
                title: 'All done!',
                html: `
              Your answers:
              <pre><code>${answers}</code></pre>
            `,
                confirmButtonText: 'Lovely!'
            })
        }
    })
}

function btnDelete() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
    }).then((result) => {
        if (result.value) {
            swalWithBootstrapButtons.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            )
        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            swalWithBootstrapButtons.fire(
                'Cancelled',
                'Your imaginary file is safe :)',
                'error'
            )
        }
    })
}