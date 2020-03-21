from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, FileField, StringField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField, TimeField, EmailField
from wtforms_alchemy import PhoneNumberField
from wtforms_alchemy.fields import QuerySelectField
from app.database.models import Materias, Profesor
from app.database import db
from flask_security import current_user


def subject_query():
    return db.query(Materias).filter(Materias.user_id == current_user.id).\
        order_by(Materias.name)
        
def profesor_query():
    return db.query(Profesor).filter(Profesor.id, Profesor.name).order_by(Profesor.name)


weekdays = [(1, 'Sunday'),
            (2, 'Monday'),
            (3, 'Tuesday'),
            (4, 'Wednesday'),
            (5, 'Thursday'),
            (6, 'Friday'),
            (7, 'Saturday')]


class LoadForm(FlaskForm):

    picture = FileField(id='file', _name='file')

    submit = SubmitField(id='publish')
    
class AssingForm(FlaskForm):
    
    subjects = QuerySelectField(
        'Asignatura', validators=[DataRequired()], query_factory=subject_query,
        allow_blank=True
    )
    
    profe = QuerySelectField(
        'Profesores', validators=[DataRequired()], query_factory=profesor_query,
        allow_blank=True
    )
    
    submit = SubmitField()


class SubjectsForm(FlaskForm):

    name = StringField(
        'Nombre', validators=[DataRequired()]
    )

    submit = SubmitField()


class ProfeForm(FlaskForm):

    subjects = QuerySelectField(
        'Asignaturas', validators=[DataRequired()], query_factory=subject_query,
        allow_blank=True
    )

    name = StringField(
        'Nombre del Profesor', validators=[DataRequired(), Length(max=80)]
    )

    last_name = StringField(
        'Apellido', validators=[Length(max=80)]
    )

    email = EmailField(
        'Email',  validators=[Length(max=80)]
    )

    phone = PhoneNumberField(
        'Telefono'
    )

    submit = SubmitField()


class TaskForm(FlaskForm):

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


class EventForm(FlaskForm):

    name = StringField(
        'Nombre', validators=[DataRequired(), Length(max=80)])

    lugar = StringField(
        'Lugar', validators=[DataRequired(), Length(max=100)])

    dia = SelectField('Dia', choices=weekdays,
                      validators=[DataRequired()])

    hora_inicio = TimeField(
        'Hora de Inicio', validators=[DataRequired()])

    hora_fin = TimeField(
        'Finaliza en', validators=[DataRequired()])

    nota = StringField('Nota')

    submit = SubmitField('')
