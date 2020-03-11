from . import auth_view
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from flask_security import user_registered
from flask_security.datastore import UserDatastore
from werkzeug.utils import secure_filename
from datetime import datetime
from .forms import LoadForm, TaskForm
from app.database import db
from app.database.queries import Queries
from app.database.models import ProfilePicture, Tarea, DetalleTarea, Materias
from config.default import IMAGE_SET_EXT, UPLOAD_FOLDER_DEST
import os


def allowed_image(filename):

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in IMAGE_SET_EXT


@auth_view.route('/uploads', methods=['GET', 'POST'])
@login_required
def Uploads():

    form = LoadForm()

    message = ''

    if form.validate_on_submit():

        picture = request.files['picture']

        if 'picture' not in request.files:
            message = 'Ninguna imagen seleccionada!'
            flash(message, category='error')
            return redirect(request.url)

        if picture.filename == '':
            message = 'Ninguna imagen selecionada!'
            flash(message, category='error')
            return redirect(request.url)

        if picture and allowed_image(picture.filename):
            filename = secure_filename(picture.filename)
            message = 'Imagen guardada con exito!'

            try:

                picture_url = (UPLOAD_FOLDER_DEST)
                _picture = ProfilePicture(picture_url=picture_url,
                                          user_id=current_user.id,
                                          name=filename)

                picture.save(os.path.join(UPLOAD_FOLDER_DEST, filename))

                db.add(_picture)
                db.commit()

            except Exception as e:
                message = 'Sea producido un error.'
                flash(message, category='error')
                raise e

            flash(message, category='success')

        else:
            message = 'Formato de imagen no permintida!'
            flash(message, category='error')

    return render_template(
        'auth/index.html',
        title='Uploads images',
        year=datetime.now().year,
        upload_form=form
    )


@auth_view.route('/register event', methods=['GET', 'POST'])
def register_event():

    return render_template(
        'auth/register_event.html',
        title='Register event'
    )


@auth_view.route('/register_task', methods=['GET', 'POST'])
def register_task():

    form = TaskForm()
    message = ''

    if form.validate_on_submit():

        task = form.name.data
        materia = form.materia.data
        asignada_en = form.asignada_en.data
        dia_entrega = form.dia_entrega.data
        comentario = form.nota.data

        try:
            # task = Tarea(
            #     name=task, user_id=current_user.id,
            #     detalle=DetalleTarea(
            #         materia=Materias(name=materia),
            #         asignada_en=asignada_en,
            #         dia_endrega=dia_entrega,
            #         comentario=comentario
            #     )
            # )
            task = Tarea(name=task, user_id=current_user.id)

            details_task = DetalleTarea(
                materia=Materias(name=materia),
                asignada_en=asignada_en,
                dia_endrega=dia_entrega,
                comentario=comentario
            )

            db.add(task)
            db.add(details_task)
            db.commit()
            message = 'Tarea guardada con exito!'
            flash(message, 'success')

        except ValueError as e:
            message = 'No fue posible guardar los cambios!'
            flash(message, 'error')
            print("este es el error")
            print(e)

        return redirect(url_for('users.tasks'))
