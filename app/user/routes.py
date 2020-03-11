from . import user_view
from flask import render_template, request
from flask_security import login_required, current_user
from sqlalchemy.orm import contains_eager
from datetime import datetime
from app.database import db
from app.auth.forms import LoadForm, EventForm, TaskForm
from app.database.models import Eventos, Tarea, PlanEstudio, DetalleEvento, DetalleTarea
from app.database.queries import Queries


@user_view.route('/index')
@login_required
def index():
        
    event = Queries.queries(Eventos, current_user)

    task = Queries.queries(Tarea, current_user)

    plan = Queries.queries(PlanEstudio, current_user)

    fecha = Queries.literal_time(event)

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
def tasks():
    
    num_details = []

    task = Queries.queries(Tarea, current_user)
    
    form = TaskForm()

    num_task = Queries.contador(Tarea, current_user)
    
    for i in range(num_task):
        
        index = task[i].id
    
        num = db.query(DetalleTarea).filter(DetalleTarea.tarea_id ==\
             index and index.user_id == current_user.id).count()
        
        num_details.append(num)
    
    return render_template(
        'user/task.html',
        title='Tasks',
        task_user=task,
        num_task=num_task,
        num_details=num_details,
        task_form=form,
        year=datetime.now().year
    )


@user_view.route('/studies-plan')
@login_required
def plan_de_estudio():

    plan = Queries.queries(PlanEstudio, current_user)

    num_plan = Queries.contador(PlanEstudio, current_user)

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

    event = Queries.queries(Eventos, current_user)

    num_event = Queries.contador(Eventos, current_user)

    return render_template(
        'user/events.html',
        title='Events',
        event_user=event,
        num_event=num_event,
        event_form=form,
        year=datetime.now().year
    )
