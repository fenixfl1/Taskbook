from . import user_view as app
from flask import render_template


@app.errorhandler(500)
def base_error_handler(e):

    return render_template(
        'errors/500.html',
        title=e.name,
        e=e.description
    ), 500


@app.errorhandler(404)
def error_404_handler(e):

    return render_template(
        'errors/404.html',
        title=e.name,
        e=e.description
    ), 404


@app.errorhandler(403)
def error_403_handler(e):

    head = e.name
    body = e.description

    return render_template(
        'errors/403.html',
        title=head,
        e=body
    ), 403
