from . import auth_view
from flask import render_template, flash, request, redirect, jsonify, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .forms import LoadForm, TaskForm, EventForm, \
    SubjectsForm, ProfeForm, AssingForm, PlanForm
from app.database import db, engne
from app.database.models import ProfilePicture, Tarea, \
    DetalleTarea, Materias, Profesor, Eventos
from config.default import IMAGE_SET_EXT, UPLOAD_FOLDER_DEST
import os


def allowed_image(filename):

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in IMAGE_SET_EXT


# function to upload profile image
@auth_view.route('/uploads', methods=['GET', 'POST'])
@login_required
def Uploads():

    form = LoadForm()

    if form.validate_on_submit():

        picture = request.files['picture']

        if 'picture' not in request.files:
            messages = 'Ninguna imagen seleccionada!'
            category = 'error'

            return redirect(request.url)

        if picture.filename == '':
            messages = 'Ninguna imagen selecionada!'
            category = 'error'

            return redirect(request.url)

        if picture and allowed_image(picture.filename):
            filename = secure_filename(picture.filename)

            try:

                picture_url = (UPLOAD_FOLDER_DEST)
                _picture = ProfilePicture(picture_url=picture_url,
                                          user_id=current_user.id,
                                          name=filename)

                picture.save(os.path.join(UPLOAD_FOLDER_DEST, filename))

                db.add(_picture)
                db.commit()

                messages = 'Imagen guardada con exito!'
                category = 'success'

            except Exception as e:
                messages = 'Ha ocurrido un error.'
                category = 'error'
                raise e

        else:
            messages = 'Formato de imagen no permintida!'
            category = 'error'

    flash(messages, category)

    return redirect(url_for('users.profile'))


# function for register subjects
@auth_view.route('/register-subjects', methods=['POST'])
def register_subjects():

    form = SubjectsForm()

    messages = 'No agrego ninguna calificacion!'
    category = 'error'

    if form.validate_on_submit():

        estado = True
        name = form.name.data

        if form.estado.data:
            estado = False

        user = Materias(name=name, estado=estado,
                        user_id=current_user.id)

        try:
            db.add(user)
            db.commit()

            messages = 'Asignatura registrada con exito!'
            category = 'success'

        except ValueError as e:

            messages = 'No fue posible registrada la asignatura!'
            category = 'error'

            raise e

    flash(messages, category)
    return redirect(url_for('users.subjects'))


@auth_view.route('/subjects/completed/<id>')
def subject_completed(id):

    try:
        engne.execute(
            """UPDATE materias SET estado=0
                WHERE id=%s""", (id))

        messages = 'Nueva asignatura marcada como cursada!'
        category = 'success'

    except ValueError as e:

        raise e

        messages = 'No fue posible completar la operacion!'
        category = 'error'

    flash(messages, category)
    return redirect(url_for('users.subjects_finished'))


@auth_view.route('/delete/subject/<id>')
def delete_subjects(id):

    dato = db.query(Materias).filter(Materias.user_id == current_user.id).\
        filter(Materias.id == id).one()

    try:
        db.delete(dato)
        db.commit()

        messages = 'Registro eliminado con exito!'
        category = 'success'
    except ValueError as e:

        messages = 'No fue posible eliminar el registro!'
        category = 'error'
        raise e

    flash(messages, category)
    return redirect(url_for('users.subjects'))


# endpoint rest to get schedules
@auth_view.route('/schedule-list')
def schedule_list():

    resp = jsonify({'success': 1, 'result': 'It is Ok!'})

    return resp


# function to assing teacher to subjects
@auth_view.route('/assing-teacher/<id>', methods=['POST'])
def assing_teacher(id):

    form = AssingForm()

    if form.validate_on_submit():

        name = form.profe.data

        try:

            update = db.query(Materias).filter(Materias.id == id)
            new_teacher = update.one()
            new_teacher.profesor = [name]
            db.commit()

            messages = 'La operacion se realizo con exito!'
            category = 'success'

        except ValueError as e:
            raise e

            messages = 'Ocurrio un error!'
            category = 'error'

    flash(messages, category)
    return redirect(url_for('users.subjects'))


# this function is to register new teacher for the current user
@auth_view.route('/register-profesor', methods=['POST'])
def register_profesor():

    form = ProfeForm()

    if form.validate_on_submit():

        user = Profesor(name=form.name.data,
                        materia=form.subjects.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        phone_number=form.phone.data,
                        user_id=current_user.id)
        try:
            db.add(user)
            db.commit()

            messages = 'Registro guardado con exito!'
            category = 'success'

        except ValueError as e:
            messages = '{0} ya esta en tu lista de Profesores!'.format(
                form.name.data)
            category = 'error'

            raise e

    flash(messages, category)
    return redirect(url_for('users.subjects'))


@auth_view.route('/delete/teachers/<id>')
def delete_teachers(id):

    dato = db.query(Profesor).filter(Profesor.user_id == current_user.id).\
        filter(Profesor.id == id).one()

    try:
        db.delete(dato)
        db.commit()

        messages = 'Registro eliminado con exito!'
        category = 'success'
    except ValueError as e:

        messages = 'No fue posible eliminar el registro!'
        category = 'error'
        raise e

    flash(messages, category)
    return redirect(url_for('users.teachers'))


# this function is to authenticate task and task-details
@auth_view.route('/register_task', methods=['POST'])
def register_task():

    messages = ''
    category = ''

    form = TaskForm()

    if form.validate_on_submit():

        task = form.name.data
        materia = form.materia.data
        asignada_en = form.asignada_en.data
        dia_entrega = form.dia_entrega.data
        comentario = form.nota.data

        task = Tarea(name=task, user_id=current_user.id)
        db.add(task)
        db.commit()

        try:

            task_detail = DetalleTarea(
                tarea=task,
                materia=materia,
                asignada_en=asignada_en,
                dia_endrega=dia_entrega,
                comentario=comentario
            )

            db.add(task_detail)
            messages = 'Tarea guardada con exito!'
            category = 'success'

        except ValueError as e:

            db.delete(task)
            messages = 'No fue posible guardar los cambios!'
            category = 'error'

            raise e

        finally:
            db.commit()

        flash(messages, category)
        return redirect(url_for('users.tasks'))


# this function is to authenticate events and events-details
@auth_view.route('/register-event', methods=['POST'])
def register_event():

    form = EventForm()

    if form.validate_on_submit():

        title = form.name.data
        lugar = form.lugar.data
        url = form.url.data
        start = form.start_date.data
        end = form.end_date.data
        comment = form.nota.data

        try:
            event = Eventos(
                user_id=current_user.id,
                title=title,
                lugar=lugar,
                url=url,
                start_date=start,
                end_date=end,
                comentario=comment
            )

            db.add(event)
            db.commit()

            messages = 'Evento creado exitosamente!'
            category = 'success'

        except ValueError as e:

            messages = 'No fue posible crear el evento!'
            category = 'error'
            raise e

        finally:
            flash(messages, category)

    return redirect(url_for('users.eventos'))


# endpoint rest to send events to the client
@auth_view.route('/calendar-events')
@login_required
def calendar_events():

    try:
        result = engne.execute('SELECT id, title, color, UNIX_TIMESTAMP(start_date)*1000 as start,\
            UNIX_TIMESTAMP(end_date)*1000 as end FROM event')

        resp = jsonify({
            'success': 1,
            'result': [dict(row) for row in result]
        }
        )

        resp.status_code = 200

        return resp
    except Exception as e:
        raise e

    finally:
        result.close()


# function to register studies plan
@auth_view.route('/register-study-plan', methods=['POST'])
def register_study_plan():

    form = PlanForm()

    if form.validate_on_submit():

        pass

    return redirect(url_for('users.plan_de_estudio'))

# this function is to delete records in any antity


@auth_view.route('/delete/tasks/<string:id>')
def delete_tasks(id):

    task = db.query(Tarea).filter(Tarea.user_id == current_user.id).\
        filter(Tarea.id == id).one()

    try:

        db.delete(task)
        db.commit()

        messages = 'Registro eliminado con exito!'
        category = 'success'

    except ValueError as e:
        messages = 'No fue posible eliminar el registro!'
        category = 'error'

        raise e

    flash(messages, category)

    return redirect(url_for('users.tasks'))


@auth_view.route('/update-subjects/<id>', methods=['POST'])
def update_subjects(id):

    try:
        engne.execute("""UPDATE materias SET name=%s 
            WHERE id=%s""",
                      (request.form["name"], id))

        messages = 'Registro actualizado con exito!'
        category = 'success'

    except ValueError as e:
        messages = 'No fue posible editar el registro!'
        category = 'error'

        raise e

    flash(messages, category)
    return redirect(url_for('users.subjects'))


@auth_view.route('/add_qualification/<id>', methods=['POST'])
def add_qualification(id):

    try:
        qualification = db.query(Materias).filter(Materias.id == id)

        new = qualification.one()
        new.qualification = request.form['calificacion']

        db.commit()

        messages = 'La operacion se realizo con exito!'
        category = 'success'

    except ValueError as e:

        messages = 'No fue posible completar la operacion!'
        category = 'error'

        raise e

    flash(messages, category)
    return redirect(url_for('users.subjects_finished'))


@auth_view.route('/update-teacher/<id>', methods=['POST'])
def update_teacher(id):

    messages = ''
    category = ''

    form = ProfeForm()

    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data

        try:
            data = engne.execute("""
                    UPDATE profesor SET name=%s,
                    last_name=%s,
                    email=%s,
                    phone_number=%s
                    WHERE id=%s""",
                                 (name, last_name,
                                  email, phone, id)
                                 )

            messages = 'Registro actualizado con exito!'
            category = 'success'

        except ValueError as e:

            messages = 'No fue posible editar el registro!'
            category = 'error'
            raise e

    flash(messages, category)
    return redirect(url_for('users.teachers'))

# this function is to obtain the datas of the entity you want edit


@auth_view.route('/edit/<string:id>')
def get_edit(id):

    return render_template(
        'auth/edit.html.j2',
        title='edit-{}'.format(id)
    )


# this function edit any entity selected in the previus function
@auth_view.route('/edit/task/<string:id>')
def edit_tasks(id):

    try:
        task = db.query(Tarea).filter(Tarea.user_id == current_user.id).\
            filter(Tarea.id == id)

        task.id = id
        db.commit()

        flash('Registro modificado con exito!', category='success')

    except:

        flash('No fue posible modificar los datos!', category='danger')

    return redirect(url_for('users.tasks'))
