from . import user_view
from flask import render_template, request
from flask_security import login_required, current_user
from flask_socketio import emit
from sqlalchemy.orm import contains_eager
from datetime import datetime, date
from app.extentions import sql, socket
from app.database import db
from app.auth.forms import LoadForm, EventForm, TaskForm, \
    SubjectsForm, ProfeForm, AssignForm, PlanForm, \
    QualificationForm, GaleryCourseForm
from app.database.models import Events, Tasks, StudyPlan, \
    Courses, Teachers
from app.database.queries import Queries


sqla = sql.session


@socket.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socket.on('connect', namespace='/hello')
def connect_handler():
    if current_user.is_authenticated:
        emit('my response',
             {'message': '{0} has joined'.format(current_user.name)},
             broadcast=True)
    else:
        return 0

# this is the index mfunction


@user_view.route('/index')
@login_required
def index():

    event = Queries.queries(Events, current_user)
    task = Queries.queries(Tasks, current_user)
    plan = Queries.queries(StudyPlan, current_user)
    subject = Queries.queries(Courses, current_user)

    _task = db.query(Tasks).\
        filter(Tasks.user_id == current_user.id).\
        filter(Tasks.delivery_day).first()

    return render_template(
        'user/react/test.html.j2',
        title='Index -',
        event_user=event,
        task_user=task,
        next_task=_task,
        stady_plan=plan,
        subject_user=subject,
        async_mode=socket.async_mode,
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
@user_view.route('/courses/')
@login_required
def subjects():

    page = 1
    pages = 1

    if 'page' in request.args:
        page = int(request.args.get('page'))

    subjects = sqla.query(Courses).filter(Courses.user_id == current_user.id).\
        filter(Courses.finished == 0).\
        filter(Courses.state == 1).paginate(page, 8, 0)

    pages = subjects.total / 8

    if pages is not int:

        total_pages = round(pages) + 1

    else:
        total_pages = pages - 1

    sform = SubjectsForm()
    pform = ProfeForm()
    aform = AssignForm()
    galery = GaleryCourseForm()

    return render_template(
        'user/courses.html.j2',
        title='Courses -',
        subject_form=sform,
        subjects_user=subjects,
        profe_form=pform,
        assig_form=aform,
        galery_form=galery,
        current_page=page,
        total_pages=total_pages,
        year=datetime.now()
    )


@user_view.route('/courses/finished')
@login_required
def subjects_finished():

    form = SubjectsForm()
    formQ = QualificationForm()

    try:
        subjects = db.query(Courses).\
            filter(Courses.user_id == current_user.id).\
            filter(Courses.state == 1).\
            filter(Courses.finished == 1).all()

    except ValueError as e:
        raise e

    return render_template(
        'user/courses_finished.html.j2',
        title='Finished courses -',
        subject_form=form,
        qualif_form=formQ,
        subjects_user=subjects,
        year=datetime.now()
    )


# this function is to see the details of the subjects
@user_view.route('/courses/teachers')
@login_required
def teachers():

    form = ProfeForm()

    teacher = db.query(Teachers).filter(
        Teachers.user_id == current_user.id).all()

    return render_template(
        'user/teachers.html.j2',
        title="Teachers -",
        profe_form=form,
        teachers=teacher,
        year=datetime.now()
    )


# this function is to create and see the schedule
@user_view.route('/schedule')
@login_required
def horario():

    subjects = Queries.queries(Courses, current_user)

    return render_template(
        'user/schedule.html.j2',
        title='Schedule -',
        subjects_user=subjects,
        year=datetime.now()
    )


# this function is to see and creat task
@user_view.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():

    form = TaskForm()

    task = Queries.queries(Tasks, current_user)

    return render_template(
        'user/task.html.j2',
        title='Tasks -',
        task_user=task,
        task_form=form,
        year=datetime.now()
    )


@user_view.route('/tasks/finished')
@login_required
def task_finished():

    task = db.query(Tasks).filter(Tasks.user_id == current_user.id).\
        filter(Tasks.state == 1).filter(Tasks.done == 1)

    form = TaskForm()

    return render_template(
        'user/task_finished.html.j2',
        title='Finished tasks -',
        task_form=form,
        task_user=task,
        year=datetime.now()
    )


@user_view.route('/tasks/edit/<id>')
@login_required
def edit_tasks(id):

    form = TaskForm()

    datos = db.query(Tasks).filter(Tasks.user_id == current_user.id).\
        filter(Tasks.id == id).one()

    return render_template(
        'user/edit/edit_tasks.html.j2',
        title='Edit tasks -',
        task_form=form,
        edit_data=datos,
        year=datetime.now()
    )


# this function is to see the details of the tasks
@user_view.route('/tasks/details/<int:id>/', methods=['GET'])
@login_required
def details_task(id):

    form = TaskForm()

    details = db.query(Tasks).filter(Tasks.id == id).\
        options(contains_eager(Tasks.user)).one()

    return render_template(
        'user/details_task.html.j2',
        title='details -',
        details=details,
        task_form=form,
        hoy=date.today()
    )


# this function is to see and create stuies plan
@user_view.route('/studies-plan')
@login_required
def plan_de_estudio():

    plan_form = PlanForm()

    plan = Queries.queries(StudyPlan, current_user)

    return render_template(
        'user/stady_plan.html.j2',
        title='Studies plan -',
        stady_plan=plan,
        plan_form=plan_form,
        year=datetime.now()
    )


# this function is to see and creat events
@user_view.route('/events')
@login_required
def eventos():

    form = EventForm(request.form)

    event = Queries.queries(Events, current_user)
    num_event = Queries.contador(Events, current_user, 1)

    return render_template(
        'user/events.html.j2',
        title='Events -',
        event_user=event,
        num_event=num_event,
        event_form=form,
        year=datetime.now()
    )
