from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, FileField, StringField, \
    TextAreaField, BooleanField, SelectField, RadioField
from wtforms.fields.html5 import EmailField, URLField, \
    DateTimeLocalField, DateField
from wtforms_alchemy import PhoneNumberField
from wtforms_alchemy.fields import QuerySelectField
from app.database.models import Courses, Teachers, StudyPlan
from app.database import db
from flask_security import current_user


def subject_query():
    return db.query(Courses).filter(Courses.user_id == current_user.id).\
        filter(Courses.state == 1).filter(Courses.finished == 0).\
        order_by(Courses.name)


def profesor_query():
    return db.query(Teachers).filter(Teachers.user_id == current_user.id)\
        .order_by(Teachers.full_name)


def study_plan_query():
    return db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id).\
        filter(StudyPlan.state == 1).order_by(StudyPlan.name)


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

    asignada_en = DateTimeLocalField(
        'Fecha de asignacion', validators=[DataRequired()])

    dia_entrega = DateTimeLocalField(
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

    start_date = DateTimeLocalField(
        'Inicio', validators=[DataRequired()])

    end_date = DateTimeLocalField(
        'Fin', validators=[DataRequired()])

    nota = TextAreaField(
        'Comentario', validators=[Length(max=150)])


class PlanForm(Default):

    name = StringField(
        'Nombre', validators=[DataRequired(), Length(max=80)]
    )

    start_date = DateField(
        'Fecha de inicio', validators=[DataRequired()]
    )


class PlanGoalsForm(Default):

    title = StringField(
        'Titulo', validators=[DataRequired(), Length(max=150)]
    )

    study_plan = QuerySelectField(
        'Plan de estudios', query_factory=study_plan_query,
        allow_blank=True, validators=[DataRequired()]
    )

    deadline = DateField(
        'Fecha limite', validators=[DataRequired()]
    )

    comment = TextAreaField(
        'Comentario', validators=[Length(max=255)]
    )


galery = [('img_1', 'image 1'), ('img_2', 'image 2'),
          ('img_3', 'image 3'), ('mgg_4', 'image 4')]


class GaleryCourseForm(Default):

    image = RadioField("image", choices=galery)
