from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, FileField, StringField, \
    TextAreaField, BooleanField, SelectField
from wtforms.fields.html5 import DateField, TimeField, \
    EmailField, URLField, DateTimeField
from wtforms_alchemy import PhoneNumberField
from wtforms_alchemy.fields import QuerySelectField
from app.database.models import Courses, Teachers
from app.database import db
from flask_security import current_user


def subject_query():
    return db.query(Courses).filter(Courses.user_id == current_user.id).\
        filter(Courses.state == True).filter(Courses.finished == False).\
        order_by(Courses.id)


def profesor_query():
    return db.query(Teachers).filter(Teachers.user_id == current_user.id)\
        .order_by(Teachers.full_name)


lista_calificacion = [('A', 'A - Muy bien: 90-100%'),
                      ('B', 'B - Bien: 80-89%'),
                      ('C', 'C - Suficiente: 70-79%'),
                      ('D', 'D - Deficiente: 60-69%'),
                      ('F', 'F - Muy deficiente: 0-50%')]

class Default(FlaskForm):

    id = StringField()
    submit = SubmitField()


class LoadForm(Default):

    picture = FileField(id='file', _name='file')


class AssignForm(Default):

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

    profe = QuerySelectField(
        'Profesores', query_factory=profesor_query,
        allow_blank=True
    )

    calificacion = SelectField('Calificación',
                               choices=lista_calificacion
                               )

    estado = BooleanField('Marcar como cursada')


class QualificationForm(Default):

    name = StringField(
        'Nombre', validators=[DataRequired()]
    )

    calificacion = SelectField(
        'Calificación',
        validators=[DataRequired()],
        choices=lista_calificacion
    )


class ProfeForm(Default):

    subjects = QuerySelectField(
        'Asignaturas', query_factory=subject_query,
        allow_blank=True
    )

    full_name = StringField(
        'Nombre del Profesor', validators=[DataRequired(), Length(max=80)]
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
