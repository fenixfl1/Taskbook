from . import auth_view
from app.tasks import notifications
from flask import flash, request, redirect, jsonify, url_for
from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename
from .forms import LoadForm, TaskForm, EventForm, \
    SubjectsForm, ProfeForm, AssignForm, PlanForm, \
    QualificationForm, PlanGoalsForm
from app.database import db, engne as engine
from app.database.models import Tasks, Courses, Teachers,\
    Events, StudyPlan, User, StudyPlanGoals
from config.default import IMAGE_SET_EXT
from datetime import datetime, timedelta
# from app.database.schemas import CoursesSchema
# import os


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
            # filename = secure_filename(picture.filename)

            try:

                # picture_url = (UPLOAD_FOLDER_DEST)
                # _picture = ProfilePicture(picture_url=picture_url,
                #                           user_id=current_user.id,
                #                           name=filename)

                # picture.save(os.path.join(UPLOAD_FOLDER_DEST, filename))

                # db.add(_picture)
                # db.commit()

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

    if form.validate_on_submit():

        name = form.name.data
        profe = form.profe.data
        finished = form.estado.data

        # check that there's no subject with that name
        check = db.query(Courses).\
            filter(Courses.user_id == current_user.id).\
            filter(Courses.state == 1).\
            filter(Courses.name == name).first()

        if not check:

            user = Courses(name=name, finished=finished,
                           user_id=current_user.id,
                           teacher=profe)

            try:
                db.add(user)
                db.commit()

                msg = '{} tu proxima clase empiezara pronto'.format(
                    current_user.first_name)

                delay = datetime.utcnow() + timedelta(minutes=3)

                notifications.apply_async(
                    (name,
                     msg,
                     datetime.now(),
                     current_user.id),
                    eta=delay
                )
                # result.wait()

                messages = 'Asignatura registrada con exito!'
                category = 'success'

            except ValueError as e:

                messages = 'No fue posible registrada la asignatura!'
                category = 'error'

                raise e

        else:
            messages = '{} ya esta registrada!'.format(name)
            category = 'error'

    flash(messages, category)
    return redirect(url_for('users.subjects'))


@auth_view.route('/subjects/completed/<int:id>')
def subject_completed(id):

    try:
        engine.execute(
            """UPDATE course SET finished=1
                WHERE id=%s""", (id))

        messages = 'Nueva asignatura marcada como cursada!'
        category = 'success'

    except ValueError as e:

        raise e

        messages = 'No fue posible completar la operacion!'
        category = 'error'

    flash(messages, category)
    return redirect(url_for('users.subjects_finished'))


@auth_view.route('/delete/subject/<int:id>')
def delete_subjects(id):

    dato = db.query(Courses).filter(Courses.user_id == current_user.id).\
        filter(Courses.id == id).one()

    try:
        dato.state = 0
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
@auth_view.route('/assing-teacher', methods=['POST'])
def assing_teacher():

    form = AssignForm()

    if form.validate_on_submit():

        # name = form.profe.data
        id_teacher = request.form['profe']
        id_subject = form.id.data

        try:

            update = db.query(Courses).\
                filter(Courses.user_id == current_user.id)\
                .filter(Courses.id == id_subject)

            new_teacher = update.one()
            new_teacher.Teachers_id = id_teacher
            db.commit()

            messages = 'La operacion se realizo con exito!'
            category = 'success'

        except ValueError as e:
            raise e

            messages = 'Ha ocurrido un error!'
            category = 'error'

        flash(messages, category)

    return redirect(url_for('users.subjects'))


# this function is to register new teacher for the current user
@auth_view.route('/register-Teachers', methods=['POST'])
def register_profesor():

    form = ProfeForm()

    if form.validate_on_submit():

        name = form.full_name.data

        check = db.query(Teachers).\
            filter(Teachers.user_id == current_user.id).\
            filter(Teachers.full_name == name).first()

        if not check:

            if form.subjects.data is not None:

                user = Teachers(full_name=name,
                                course=[form.subjects.data],
                                email=form.email.data,
                                phone_number=form.phone.data,
                                user_id=current_user.id)

            else:
                user = Teachers(full_name=name,
                                email=form.email.data,
                                phone_number=form.phone.data,
                                user_id=current_user.id)

            try:
                db.add(user)
                db.commit()

                messages = 'Registro guardado con exito!'
                category = 'success'

            except ValueError as e:
                messages = 'Ha ocurrido un error desconocido!'
                category = 'error'

                raise e

        else:

            messages = '{} ya esta registrado!'.format(name)
            category = 'error'

    flash(messages, category)
    return redirect(url_for('users.teachers'))


@auth_view.route('/delete/teachers/<int:id>')
def delete_teachers(id):

    dato = db.query(Teachers).filter(Teachers.user_id == current_user.id).\
        filter(Teachers.id == id).one()

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

        name = form.name.data
        materia = form.materia.data
        asignada_en = form.asignada_en.data
        dia_entrega = form.dia_entrega.data
        comentario = form.nota.data

        try:

            task = Tasks(
                name=name,
                user_id=current_user.id,
                course=materia,
                assigned_in=asignada_en,
                delivery_day=dia_entrega,
                comment=comentario
            )

            msg = 'Saludos {} recuenrda que tuenes una tarea pendiente'.format(
                current_user.first_name)

            delay = datetime.utcnow() + timedelta(second=30)

            notifications.apply_async(
                (name,
                 msg,
                 asignada_en,
                 current_user.id),
                eta=delay
            )

            db.add(task)
            db.commit()

            messages = 'Tasks guardada con exito!'
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
            event = Events(
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


# function to register studies plan
@auth_view.route('/register-study-plan', methods=['POST'])
def register_study_plan():

    form = PlanForm()

    if form.validate_on_submit():

        try:
            name = form.name.data
            start_date = form.start_date.data

            plan = StudyPlan(name, start_date, current_user.id)

            db.add(plan)
            db.commit()

            messages = 'Plan de estudio creado exitosamente'
            category = 'success'

        except ValueError as e:

            messages = 'No fue posible crear el plan de estudios'
            category = 'error'
            raise e

        finally:
            flash(messages, category)

    return redirect(url_for('users.plan_de_estudio'))


@auth_view.route('/register-study-plan-goals', methods=['POST'])
def register_study_plan_goals():

    form = PlanGoalsForm()

    if form.validate_on_submit():

        try:
            title = form.title.data
            deadline = form.deadline.data
            study_plan = request.form['study_plan']
            comment = form.comment.data

            user = StudyPlanGoals(
                title=title,
                deadline=deadline,
                comment=comment,
                plan_id=study_plan
            )

            db.add(user)
            db.commit()

            messages = "Objetivo guardado exitosamente!"
            category = "success"

        except Exception as e:

            messages = "Ha ocurrido un error desconocido!"
            category = "error"

            raise e

        finally:

            flash(messages, category)

    return redirect(url_for('users.plan_de_estudio'))


# this function is to delete records in any antity
@auth_view.route('/delete/tasks/<int:id>')
def delete_tasks(id):

    task = db.query(Tasks).filter(Tasks.user_id == current_user.id).\
        filter(Tasks.id == id).one()

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


@auth_view.route('/update-subjects', methods=['POST'])
def update_subjects():

    form = SubjectsForm()

    name = form.name.data
    id = request.form['id']
    teacher_id = request.form['profe']

    try:

        data = db.query(Courses).filter(Courses.user_id == current_user.id).\
            filter(Courses.id == id)

        new_data = data.one()

        new_data.name = name

        if teacher_id != '__None':

            teacher = db.query(Teachers).\
                filter(Teachers.user_id == current_user.id).\
                filter(Teachers.id == teacher_id).one()

            new_data.Teachers = teacher

        db.commit()

        messages = 'Registro actualizado con exito!'
        category = 'success'

    except ValueError as e:
        messages = 'No fue posible editar el registro!'
        category = 'error'

        raise e

    flash(messages, category)
    return redirect(url_for('users.subjects'))


@auth_view.route('/add_qualification', methods=['POST'])
def add_qualification():

    form = QualificationForm()

    if form.validate_on_submit():

        id = form.id.data

        try:
            qualification = db.query(Courses).filter(Courses.id == id)

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


@auth_view.route('/update-teacher', methods=['POST'])
def update_teacher():

    form = ProfeForm()

    if form.validate_on_submit():

        id = form.id.data
        name = form.full_name.data
        email = form.email.data
        phone = form.phone.data

        try:
            engine.execute("""
                    UPDATE teacher SET \
                    full_name=%s,
                    email=%s,
                    phone_number=%s
                    WHERE id=%s""",
                           (name, email, phone, id))

            messages = 'Registro actualizado con exito!'
            category = 'success'

        except ValueError as e:

            messages = 'No fue posible editar el registro!'
            category = 'error'
            raise e

    flash(messages, category)
    return redirect(url_for('users.teachers'))


# this function edit any entity selected in the previus function
@auth_view.route('/edit/task/<int:id>')
def edit_tasks(id):

    try:
        task = db.query(Tasks).filter(Tasks.user_id == current_user.id).\
            filter(Tasks.id == id)

        task.id = id
        db.commit()

        flash('Registro modificado con exito!', category='success')

    except ValueError as e:

        flash('No fue posible modificar los datos!', category='danger')
        raise e

    return redirect(url_for('users.tasks'))


# endpoint rest to send events to the client
@auth_view.route('/calendar-events')
@login_required
def calendar_events():

    try:
        result = engine.execute("""
            SELECT id, title, color, UNIX_TIMESTAMP(start_date)*1000 as start,\
            UNIX_TIMESTAMP(end_date)*1000 as end FROM event
        """)

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


@auth_view.route('/search')
@login_required
def search():

    try:
        result = engine.execute("""
            SELECT id, name, table_name, user_id FROM course
            WHERE user_id = {0} UNION \
            SELECT id, first_name, table_name, last_name FROM user
            WHERE NOT id = {0} UNION \
            SELECT id, title, table_name, user_id FROM event
            WHERE user_id = {0} UNION \
            SELECT id, name, table_name, user_id FROM task
            WHERE user_id = {0} UNION \
            SELECT id, full_name, table_name, user_id FROM teacher
            WHERE user_id = {0} UNION \
            SELECT id, name, table_name, user_id FROM study_plan \
            WHERE user_id = {0} UNION \
            SELECT plan_id, title, deadline, finished_in FROM (study_plan_goals
            INNER JOIN study_plan ON \
            study_plan_goals.plan_id = study_plan.id ) \
            WHERE study_plan.user_id = {0}
            """.format(current_user.id))

        resp = jsonify({
            'success': 1,
            'result': [dict(row) for row in result]
        })

        resp.status_code = 200

        return resp

    except Exception as e:
        raise e
        return jsonify({'result': 'error'})
