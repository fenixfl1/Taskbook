from . import user_view
from flask import render_template
from flask_security import login_required, current_user
from sqlalchemy.orm import *
from datetime import datetime
from app.database import db
from app.database.models import DetalleEvento, Eventos


@user_view.route('/index')
@login_required
def index():

    return render_template(
        'user/index.html',
        title='Inicio',
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

    return 'Tareas'


@user_view.route('/plan de estudio')
@login_required
def plan_de_estudio():

    return 'plan de estudio'


@user_view.route('/eventos')
@login_required
def eventos():

    event_user = db.query(Eventos).filter(
        Eventos.user_id == current_user.id).options(contains_eager(
            Eventos.user)).all()

    # Numero total de eventos
    num_event = db.query(Eventos).filter(
        Eventos.user_id == current_user.id).count()

    detail_evento = db.query(DetalleEvento).join(DetalleEvento.evento).\
        filter(DetalleEvento.evento_id == Eventos.id).filter(
            Eventos.user_id == current_user.id).filter(
            DetalleEvento.estado == True).options(contains_eager(
                DetalleEvento.evento)).all()

    return render_template(
        'user/events.html',
        title='Events',
        detail_evento=detail_evento,
        event_user=event_user,
        num_event=num_event,
        year=datetime.now().year
    )
