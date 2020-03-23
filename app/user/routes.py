from . import user_view
from flask import render_template, request
from flask_restful import Resource
from flask_security import login_required, current_user
from sqlalchemy.orm import contains_eager
from datetime import datetime, date
from app.database import db
from app.auth.forms import LoadForm, EventForm, TaskForm, ProfeForm, SubjectsForm, ProfeForm, \
    AssingForm
from app.database.models import Eventos, Tarea, PlanEstudio, DetalleEvento, DetalleTarea, \
    Materias, Profesor
from app.database.queries import Queries
import requests


# this is the index mfunction
@user_view.route('/index')
@login_required
def index():
        
    event = Queries.queries(Eventos, current_user, order_by="name")

    task = Queries.queries(Tarea, current_user, order_by="date1")

    plan = Queries.queries(PlanEstudio, current_user, order_by="name")
    
    count_task = Queries.contador(Tarea, current_user)

    fecha = Queries.literal_time(task)

    return render_template(
        'user/index.html.j2',
        title='Index -',
        event_user=event,
        task_user=task,
        fecha=fecha,
        num_task=count_task,
        stady_plan=plan,
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
    
    subjects = Queries.queries(Materias, current_user)
    count = Queries.contador(Materias, current_user)
    
    sform = SubjectsForm()
    pform = ProfeForm()
    aform = AssingForm()
    
    return render_template(
        'user/subjects.html.j2',
        title='Subjects -',
        subject_form=sform,
        subjects_user=subjects,
        profe_form=pform,
        num_subjects=count,
        form=aform,
        year=datetime.now()
    )


# this function is to see the details of the subjects 
@user_view.route('/subjects/teachers')
@login_required
def teachers():
    
    form = ProfeForm()
    count = Queries.contador(Materias, current_user)
    
    return render_template(
        'user/teachers.html.j2',
        title="teachers -",
        profe_form=form,
        num_subjects=count,
        year=datetime.now()
    )


# this function is to create and see the schedule
@user_view.route('/schedule')
@login_required
def horario():
    
    subjects = Queries.queries(Materias, current_user)
    count = Queries.contador(Materias, current_user)

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
        
    num_task = Queries.contador(Tarea, current_user)
       
    for i in range(num_task):
        
        index = task[i].id
    
        num = db.query(DetalleTarea).filter(DetalleTarea.tarea_id ==\
             index and index.user_id == current_user.id).\
                 filter(DetalleEvento.estado==True).count()
        
        num_details.append(num)
    
    return render_template(
        'user/task.html.j2',
        title='Tasks -',
        task_user=task,
        num_task=num_task,
        num_details=num_details,
        task_form=form,
        year=datetime.now()
    )
    
 
# this function is to see the details of the tasks   
@user_view.route('/tasks/details/<int:id>/', methods=['GET'])
@login_required
def details_task(id):
    
    form = TaskForm()
    
    num_task = Queries.contador(Tarea, current_user)
    
    details = db.query(Tarea).filter(Tarea.id==id).\
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

    plan = Queries.queries(PlanEstudio, current_user)

    num_plan = Queries.contador(PlanEstudio, current_user)

    return render_template(
        'user/stady_plan.html.j2',
        title='Studies plan -',
        stady_plan=plan,
        num_plan=num_plan,
        year=datetime.now()
    )


# this function is to see and creat events
@user_view.route('/events')
@login_required
def eventos():
    
    form = EventForm(request.form)

    event = Queries.queries(Eventos, current_user)

    num_event = Queries.contador(Eventos, current_user)

    return render_template(
        'user/events.html.j2',
        title='Events -',
        event_user=event,
        num_event=num_event,
        event_form=form,
        year=datetime.now()
    )
    
@user_view.route('/test')
def test():
    
    r = requests.get('https://google.com')
    
    return r.json()
