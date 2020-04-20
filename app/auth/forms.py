from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, FileField, StringField, \
    TextAreaField, BooleanField
from wtforms.fields.html5 import DateField, TimeField, \
    EmailField, URLField, DateTimeField
from wtforms_alchemy import PhoneNumberField
from wtforms_alchemy.fields import QuerySelectField
from app.database.models import Materias, Profesor
from app.database import db
from flask_security import current_user


def subject_query():
    return db.query(Materias).filter(Materias.user_id == current_user.id).\
        filter(Materias.estado == True).order_by(Materias.id)


def profesor_query():
    return db.query(Profesor).filter(Profesor.user_id == current_user.id)\
        .order_by(Profesor.name)


weekdays = [(1, 'Sunday'),
            (2, 'Monday'),
            (3, 'Tuesday'),
            (4, 'Wednesday'),
            (5, 'Thursday'),
            (6, 'Friday'),
            (7, 'Saturday')]


class Default(FlaskForm):

    submit = SubmitField()


class LoadForm(Default):

    picture = FileField(id='file', _name='file')


class AssingForm(Default):

    subjects = StringField(
        'Asignatura', validators=[DataRequired()]
    )

    profe = QuerySelectField(
        'Profesores', validators=[DataRequired()],
        query_factory=profesor_query,
        allow_blank=True
    )


class SubjectsForm(Default):

    name = StringField(
        'Nombre', validators=[DataRequired()]
    )

    estado = BooleanField('Marcar como cursada',)


class ProfeForm(Default):

    subjects = QuerySelectField(
        'Asignaturas', query_factory=subject_query,
        allow_blank=True
    )

    name = StringField(
        'Nombre del Profesor', validators=[DataRequired(), Length(max=80)]
    )

    last_name = StringField(
        'Apellido', validators=[Length(max=80)]
    )

    email = EmailField(
        'Email', validators=[Length(max=80)]
    )

    phone = PhoneNumberField(
        'Telefono'
    )


class TaskForm(Default):

    name = StringField(
        'Tarea', validators=[DataRequired()])

    materia = QuerySelectField(
        query_factory=subject_query, allow_blank=True
    )

    asignada_en = DateField(
        'Fecha de asignacion', validators=[DataRequired()])

    dia_entrega = DateField(
        'Fecha de entrega', validators=[DataRequired()])

    nota = TextAreaField(
        'Comentario', validators=[Length(max=150)])

    submit = SubmitField('')


class EventForm(Default):

    name = StringField(
        'Nombre', validators=[DataRequired(), Length(max=80)])

    lugar = StringField(
        'Lugar', validators=[DataRequired(), Length(max=100)])

    url = URLField('Url')

    start_date = DateTimeField(
        'Inicio', validators=[DataRequired()])

    end_date = DateTimeField(
        'Fin', validators=[DataRequired()])

    nota = TextAreaField(
        'Comentario', validators=[Length(max=150)])


class PlanForm(Default):

    name = StringField(
        'Nombre', validators=[DataRequired(), Length(max=80)]
    )

    start = TimeField(
        'Desde', validators=[DataRequired()]
    )

    end = TimeField(
        'Hasta', validators=[DataRequired()]
    )

    objetivo = TextAreaField(
        'Objetivo', validators=[Length(max=255)]
    )
