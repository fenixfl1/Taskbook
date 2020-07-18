from . import user_view
from flask import render_template, request
from flask_security import login_required, current_user
from sqlalchemy.orm import contains_eager
from datetime import datetime, date
from app import db_session
from app.database import db
from app.auth.forms import LoadForm, EventForm, TaskForm, \
    SubjectsForm, ProfeForm, AssignForm, PlanForm, \
    QualificationForm, PlanGoalsForm
from app.database.models import Events, Tasks, StudyPlan, \
    Courses, Teachers, StudyPlanGoals
from app.database.queries import Queries


@user_view.context_processor
def context_processor():

    task_form = TaskForm()
    course_form = SubjectsForm()
    event_form = EventForm()
    plan_form = PlanForm()
    plan_goal_form = PlanGoalsForm()
    profe_form = ProfeForm()
    assign_form = AssignForm()
    q_form = QualificationForm()
    load_form = LoadForm()
    year = datetime.now()
    hoy = date.today()

    return dict(
        task_form=task_form,
        course_form=course_form,
        event_form=event_form,
        plan_form=plan_form,
        plan_goal_form=plan_goal_form,
        profe_form=profe_form,
        assign_form=assign_form,
        q_form=q_form,
        load_form=load_form,
        year=year,
        hoy=hoy
    )


# this function yo see the profile of the current user
@user_view.route('/users/<int:id>/<string:user>/')
@login_required
def profile(id, user):

    return render_template(
        'user/profile.html.j2',
        title='perfil -',
        user=user,
        id=id
    )


# this function is to see and create the subjects
@user_view.route('/index')
@login_required
def subjects():

    page = 1
    pages = 1

    if 'page' in request.args:
        page = int(request.args.get('page'))

    courses = db_session.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.finished == 0).\
        filter(Courses.state == 1).paginate(page, 8, 0)

    list_courses = db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.finished == 0).\
        filter(Courses.state == 1)

    pages = courses.total / 8

    if pages is not int:
        total_pages = round(pages) + 1
    else:
        total_pages = pages - 1

    return render_template(
        'user/all_courses.html.j2',
        title='Courses -',
        subjects_user=courses,
        list_courses=list_courses,
        current_page=page,
        total_pages=total_pages
    )


@user_view.route('/courses/<int:id>/')
@login_required
def courses(id):

    courses = db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.id == id).first()

    task = db.query(Tasks).\
        filter(Tasks.user_id == current_user.id).\
        filter(Tasks.state == 1).\
        filter(Tasks.done == 0)

    return render_template(
        'user/courses.html.j2',
        title='Course of {}'.format(courses.name),
        course=courses,
        assignments=task
    )


@user_view.route('/courses/finished')
@login_required
def subjects_finished():

    try:
        courses = db.query(Courses).\
            filter(Courses.user_id == current_user.id).\
            filter(Courses.state == 1).\
            filter(Courses.finished == 1).all()

    except ValueError as e:
        raise e

    return render_template(
        'user/courses_finished.html.j2',
        title='Finished courses -',
        subjects_user=courses
    )


# this function is to see the details of the subjects
@user_view.route('/courses/teachers')
@login_required
def teachers():

    teacher = db.query(Teachers).filter(
        Teachers.user_id == current_user.id).all()

    return render_template(
        'user/teachers.html.j2',
        title="Teachers -",
        teachers=teacher
    )


# this function is to create and see the schedule
@user_view.route('/schedule')
@login_required
def horario():

    courses = Queries.queries(Courses, current_user)

    return render_template(
        'user/schedule.html.j2',
        title='Schedule -',
        subjects_user=courses
    )


# this function is to see and creat task
@user_view.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():

    task = Queries.queries(Tasks, current_user)

    return render_template(
        'user/task.html.j2',
        title='Tasks -',
        task_user=task
    )


@user_view.route('/tasks/finished')
@login_required
def task_finished():

    task = db.query(Tasks).filter(Tasks.user_id == current_user.id).\
        filter(Tasks.state == 1).filter(Tasks.done == 1)

    return render_template(
        'user/task_finished.html.j2',
        title='Finished tasks -',
        task_user=task
    )


@user_view.route('/tasks/edit/<int:id>')
@login_required
def edit_tasks(id):

    datos = db.query(Tasks).filter(Tasks.user_id == current_user.id).\
        filter(Tasks.id == id).one()

    return render_template(
        'user/edit/edit_tasks.html.j2',
        title='Edit tasks -',
        edit_data=datos
    )


# this function is to see the details of the tasks
@user_view.route('/tasks/details/<int:id>/', methods=['GET'])
@login_required
def details_task(id):

    details = db.query(Tasks).filter(Tasks.id == id).\
        options(contains_eager(Tasks.user)).one()

    return render_template(
        'user/details_task.html.j2',
        title='details -',
        details=details
    )


# this function is to see and create stuies plan
@user_view.route('/studies-plan')
@login_required
def plan_de_estudio():

    plan = db.query(StudyPlan).\
        filter(StudyPlan.user_id == current_user.id). \
        filter(StudyPlan.state == 1).\
        options(contains_eager(StudyPlan.user))

    return render_template(
        'user/stady_plan.html.j2',
        title='Studies plan -',
        stady_plan=plan
    )


# this functionis to watch all golas of one study plan
@user_view.route('/studies-plan/<int:id>')
@login_required
def study_plan_golas(id):

    goals = db.query(StudyPlanGoals).\
        join(StudyPlan, StudyPlanGoals.plan_id == StudyPlan.id).\
        filter(StudyPlanGoals.state == 1).\
        filter(StudyPlanGoals.done == 0).\
        filter(StudyPlan.id == id).\
        filter(StudyPlan.state == 1).\
        filter(StudyPlan.user_id == current_user.id)

    return render_template(
        'user/stady_plan_goals.html.j2',
        title='Studies plan goals -',
        goals=goals,
        plan_id=id
    )


# this function is to see and creat events
@user_view.route('/events')
@login_required
def eventos():

    event = Queries.queries(Events, current_user)
    num_event = Queries.contador(Events, current_user, 1)

    return render_template(
        'user/events.html.j2',
        title='Events -',
        event_user=event,
        num_event=num_event
    )
