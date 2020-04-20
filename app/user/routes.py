from . import user_view
from flask import render_template, request
from flask_security import login_required, current_user
from sqlalchemy.orm import contains_eager
from datetime import datetime, date
from app.database import db
from app.auth.forms import LoadForm, EventForm, TaskForm, \
    SubjectsForm, ProfeForm, AssingForm, PlanForm
from app.database.models import Eventos, Tarea, PlanEstudio, DetalleTarea, \
    Materias, Profesor
from app.database.queries import Queries


# this is the index mfunction
@user_view.route('/index')
@login_required
def index():

    event = Queries.queries(Eventos, current_user, order_by="name")
    task = Queries.queries(Tarea, current_user, order_by="name")
    plan = Queries.queries(PlanEstudio, current_user, order_by="name")
    subject = Queries.queries(Materias, current_user, order_by="name")

    count_event = Queries.contador(Eventos, current_user, 1)
    count_plan = Queries.contador(PlanEstudio, current_user, 1)
    count_subjects = Queries.contador(Materias, current_user, 1)
    count_task = Queries.contador(Tarea, current_user, 1)

    _task = db.query(Tarea, DetalleTarea).\
        filter(Tarea.user_id == current_user.id).\
        filter(DetalleTarea.dia_endrega).first()

    return render_template(
        'user/index.html.j2',
        title='Index -',
        event_user=event,
        task_user=task,
        next_task=_task,
        num_task=count_task,
        num_event=count_event,
        num_plan=count_plan,
        num_subject=count_subjects,
        stady_plan=plan,
        subject_user=subject,
        year=datetime.now()
    )


# this function yo see the profile of the current user
@user_view.route('/profile/<string:user>/')
@login_required
def profile(user):

    form = LoadForm(request.form)

    return render_template(
        'user/profile.html.j2',
        title='perfil -',
        user=user,
        upload_form=form,
        year=datetime.now()
    )


# this function is to see and create the subjects
@user_view.route('/subjects/')
@login_required
def subjects():

    subjects = db.query(Materias).filter(Materias.user_id == current_user.id).\
        filter(Materias.estado == 1)

    count = Queries.contador(Materias, current_user, 1)

    count_complet = Queries.contador(Materias, current_user, 0)

    teacher = db.query(Profesor).filter(
        Profesor.user_id == current_user.id).count()

    sform = SubjectsForm()
    pform = ProfeForm()

    return render_template(
        'user/subjects.html.j2',
        title='Subjects -',
        subject_form=sform,
        subjects_user=subjects,
        profe_form=pform,
        num_subjects=count,
        num_completed=count_complet,
        num_teacher=teacher,
        year=datetime.now()
    )


@user_view.route('/subjects/edit/<id>')
@login_required
def edit_subjects(id):

    form = SubjectsForm()

    count = Queries.contador(Materias, current_user, 1)
    data = db.query(Materias).filter(Materias.user_id == current_user.id).\
        filter(Materias.id == id).one()

    return render_template(
        'user/edit/edit_subjects.html.j2',
        title='Edit subject -',
        num_subjects=count,
        subject_form=form,
        edit_data=data,
        year=datetime.now()
    )


@user_view.route('/subjects/finished')
@login_required
def subjects_finished():

    form = SubjectsForm()

    try:
        subjects = db.query(Materias).filter(Materias.user_id == current_user.id).\
            filter(Materias.estado == 0)

    except ValueError as e:
        raise e

    teacher = Queries.contador(Materias, current_user, 1)

    count = Queries.contador(Materias, current_user, 1)

    completed = Queries.contador(Materias, current_user, 0)

    return render_template(
        'user/subjects_finished.html.j2',
        title='Subjects finished -',
        subject_form=form,
        subjects_user=subjects,
        num_completed=completed,
        num_teacher=teacher,
        num_subjects=count,
        year=datetime.now()
    )


@user_view.route('/subjects/assing-teachers/<id>')
@login_required
def assing_teachers(id):

    form = AssingForm()
    pform = ProfeForm()

    data = db.query(Materias).filter(Materias.user_id == current_user.id).\
        filter(Materias.id == id).one()

    teacher = db.query(Profesor).filter(
        Profesor.user_id == current_user.id).count()

    subjects = Queries.contador(Materias, current_user, 1)

    return render_template(
        'user/assing_teacher.html.j2',
        title='Assing teacher -',
        profe_form=pform,
        form=form,
        edit_data=data,
        num_teacher=teacher,
        num_subjects=subjects,
        year=datetime.now()
    )


# this function is to see the details of the subjects
@user_view.route('/subjects/teachers')
@login_required
def teachers():

    form = ProfeForm()
    count = Queries.contador(Materias, current_user, 1)

    num_teacher = Queries.contador(Profesor, current_user, 1)

    teacher = db.query(Profesor).filter(
        Profesor.user_id == current_user.id).all()

    count_complet = Queries.contador(Materias, current_user, 0)

    return render_template(
        'user/teachers.html.j2',
        title="teachers -",
        profe_form=form,
        teachers=teacher,
        num_subjects=count,
        num_completed=count_complet,
        num_teacher=num_teacher,
        year=datetime.now()
    )


@user_view.route('/subjects/teachers/edit/<id>')
@login_required
def edit_teachers(id):

    form = ProfeForm()

    num_teacher = Queries.contador(Materias, current_user, 1)
    data = db.query(Profesor).filter(Profesor.user_id == current_user.id).\
        filter(Profesor.id == id).one()

    return render_template(
        'user/edit/edit_teacher.html.j2',
        title='Edit teacher -',
        num_teacher=num_teacher,
        edit_data=data,
        profe_form=form,
        year=datetime.now()
    )


# this function is to create and see the schedule
@user_view.route('/schedule')
@login_required
def horario():

    subjects = Queries.queries(Materias, current_user, order_by='name')
    count = Queries.contador(Materias, current_user, 1)

    return render_template(
        'user/schedule.html.j2',
        title='Schedule -',
        subjects_user=subjects,
        num_subjects=count,
        year=datetime.now()
    )


# this function is to see and creat task
@user_view.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks(order_by='id'):

    num_details = []

    form = TaskForm()

    task = Queries.queries(Tarea, current_user, order_by=order_by)

    num_task = Queries.contador(Tarea, current_user, 1)

    return render_template(
        'user/task.html.j2',
        title='Tasks -',
        task_user=task,
        num_task=num_task,
        num_details=num_details,
        task_form=form,
        year=datetime.now()
    )


@user_view.route('/tasks/edit/<id>')
def edit_tasks(id):

    form = TaskForm()

    datos = db.query(Tarea).filter(Tarea.user_id == current_user.id).\
        filter(Tarea.id == id).one()

    return render_template(
        'user/edit/edit_tasks.html.j2',
        title='Edit tasks -',
        task_form=form,
        edit_data=datos,
        year=datetime.now()
    )


@user_view.route('/tasks/compleds')
def task_completed():

    form = TaskForm()

    # task = Queries.queries(Tarea, current_user)
    num_task = Queries.contador(Tarea, current_user, 1)

    return render_template(
        'user/task_completed.html',
        title='Tasks completed -',
        num_task=num_task,
        task_form=form,
        year=datetime.now()
    )


# this function is to see the details of the tasks
@user_view.route('/tasks/details/<int:id>/', methods=['GET'])
@login_required
def details_task(id):

    form = TaskForm()

    num_task = Queries.contador(Tarea, current_user, 1)

    details = db.query(Tarea).filter(Tarea.id == id).\
        options(contains_eager(Tarea.user)).one()

    return render_template(
        'user/details_task.html.j2',
        title='details -',
        details=details,
        task_form=form,
        num_task=num_task,
        hoy=date.today()
    )


# this function is to see and create stuies plan
@user_view.route('/studies-plan')
@login_required
def plan_de_estudio():

    plan_form = PlanForm()

    plan = Queries.queries(PlanEstudio, current_user)

    num_plan = Queries.contador(PlanEstudio, current_user, 1)

    return render_template(
        'user/stady_plan.html.j2',
        title='Studies plan -',
        stady_plan=plan,
        num_plan=num_plan,
        plan_form=plan_form,
        year=datetime.now()
    )


# this function is to see and creat events
@user_view.route('/events')
@login_required
def eventos():

    form = EventForm(request.form)

    event = Queries.queries(Eventos, current_user)
    num_event = Queries.contador(Eventos, current_user, 1)

    return render_template(
        'user/events.html.j2',
        title='Events -',
        event_user=event,
        num_event=num_event,
        event_form=form,
        year=datetime.now()
    )
