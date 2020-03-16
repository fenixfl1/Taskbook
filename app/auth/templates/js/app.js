function try_delete() {
    var opt = confirm('¿Seguro de que quieres eliminar el registro?');

    if (opt == true) {
        window.location.href = " {{ url_for('auth.delete') }} ";
    }
}