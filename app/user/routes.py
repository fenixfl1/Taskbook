from . import user_view
from flask import render_template, request
from flask_security import login_required, current_user
from sqlalchemy.orm import contains_eager
from datetime import datetime
from app.database import db
from app.auth.forms import LoadForm, EventForm
from app.database.models import Eventos, Tarea, PlanEstudio, DetalleEvento


# Perform query of any entity for current_user
def queries(entity):

    try:
        return db.query(entity).filter(entity.user_id == current_user.id).\
            options(contains_eager(entity.user)).all()
            
    except:
        pass


# number of records in an entity
def contador(entity):

    try:
        return db.query(Eventos).filter(
            Eventos.user_id == current_user.id).count()
        
    except:
        pass


# get the time in text formt
def literal_time(entity):
    
    try:

        date_str = str(entity[0].detalle[0].dia)

        date_object = datetime.strptime(date_str, '%Y-%m-%d')

        date = datetime.strftime(date_object, '%a %d de %b')

    
        return date
    
    except:
        pass


# get the next activities to perform
def get_most_recent(result):

    date = []

    # num_activity = contador(result)

    for i in range(2):

        date.append(result[i].detalle[i].dia)

        print(date)

    return max(date)


@user_view.route('/index')
@login_required
def index():
        
    event = queries(Eventos)

    task = queries(Tarea)

    plan = queries(PlanEstudio)

    fecha = literal_time(event)

    return render_template(
        'user/index.html',
        title='Index',
        event_user=event,
        task_user=task,
        fecha=fecha,
        stady_plan=plan,
        year=datetime.now().year
    )
    
    
@user_view.route('/profile/<user>/')
@login_required
def profile(user):
    
    form = LoadForm(request.form)
    
    return render_template(
        'user/profile.html',
        title='perfil',
        user=user,
        upload_form=form,
        year=datetime.now().year
    )


@user_view.route('/schedule')
@login_required
def horario():

    return render_template(
        'user/schedule.html',
        title='Schedule',
        year=datetime.now().year
    )


@user_view.route('/tasks')
@login_required
def tareas():

    task = queries(Tarea)

    num_task = contador(Tarea)

    return render_template(
        'user/task.html',
        title='Tasks',
        task_user=task,
        num_task=num_task,
        year=datetime.now().year
    )


@user_view.route('/studies-plan')
@login_required
def plan_de_estudio():

    plan = queries(PlanEstudio)

    num_plan = contador(PlanEstudio)

    return render_template(
        'user/stady_plan.html',
        title='Studies plan',
        stady_plan=plan,
        num_plan=num_plan,
        year=datetime.now().year
    )


@user_view.route('/events')
@login_required
def eventos():
    
    form = EventForm(request.form)

    event = queries(Eventos)

    num_event = contador(Eventos)

    return render_template(
        'user/events.html',
        title='Events',
        event_user=event,
        num_event=num_event,
        event_form=form,
        year=datetime.now().year
    )
