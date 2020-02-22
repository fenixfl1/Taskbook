from . import user_view
from flask import render_template
from flask_security import login_required, current_user
from sqlalchemy.orm import *
from datetime import datetime
from app.database import db
from app.database.models import Eventos, Tarea, PlanEstudio


# Perform query of any entity for current_user
def queries(entity):

    return db.query(entity).filter(entity.user_id == current_user.id).\
        options(contains_eager(entity.user)).all()


# number of records in an entity
def contador(entity):

    return db.query(Eventos).filter(
        Eventos.user_id == current_user.id).count()


# get the time in text formt
def literal_time(entity):

    date_str = str(entity[0].detalle[0].dia)

    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    date = datetime.strftime(date_object, '%a %d de %b')

    return date


# get the next activity to perform
def get_most_recent(result):

    date = []

    # num_activity = contador(result)

    for i in range(2):

        date.append(result[i].detalle[i].dia)

        print(date)

    return max(date)


@user_view.route('/inicio')
@login_required
def index():

    event = queries(Eventos)

    task = queries(Tarea)

    plan = queries(PlanEstudio)

    fecha = literal_time(event)

    return render_template(
        'user/index.html',
        title='Inicio',
        event_user=event,
        task_user=task,
        fecha=fecha,
        stady_plan=plan,
        year=datetime.now().year
    )


@user_view.route('/calendario')
@login_required
def calendario():

    return 'Calendario'


@user_view.route('/horario')
@login_required
def horario():

    return 'Horario'


@user_view.route('/tareas')
@login_required
def tareas():

    task = queries(Tarea)

    num_task = contador(Tarea)

    return render_template(
        'user/task.html',
        title='Tareas',
        task_user=task,
        num_task=num_task,
        year=datetime.now().year
    )


@user_view.route('/plan de estudio')
@login_required
def plan_de_estudio():

    plan = queries(PlanEstudio)

    num_plan = contador(PlanEstudio)

    return render_template(
        'user/stady_plan.html',
        title='plan de estudio',
        stady_plan=plan,
        num_plan=num_plan,
        year=datetime.now().year
    )


@user_view.route('/eventos')
@login_required
def eventos():

    event = queries(Eventos)

    num_event = contador(Eventos)

    return render_template(
        'user/events.html',
        title='Events',
        event_user=event,
        num_event=num_event,
        year=datetime.now().year
    )
