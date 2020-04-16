$(document).ready(function() {

    $('.btn-delete').on('click', function(e) {

        e.preventDefault();

        const btnDelete = document.querySelectorAll('.btn-delete');

        if (btnDelete) {
            const btnArray = jQuery.makeArray(btnDelete);

            btnArray.forEach((btn) => {
                btn.addEventListener('click', function() {
                    Swal.fire({
                        title: '¿Estas seguro de eliminarlo?',
                        text: "Ya no podras revertir los cambios!",
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Si, eliminarlo!'
                    }).then((result) => {

                        if (result.value) {
                            window.location = this.href;
                        }
                    });
                });
            });
        }
    });
});