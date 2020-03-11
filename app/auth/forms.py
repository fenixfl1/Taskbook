from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, FileField, StringField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField, TimeField

weekdays = [('Sun','Sunday'),
            ('Mon', 'Monday'),
            ('Tus', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday')]

class LoadForm(FlaskForm):

    picture = FileField(id='file', _name='file')

    submit = SubmitField('', id='publish')
    
    
class TaskForm(FlaskForm):
    
    name = StringField(
        'Task', validators=[DataRequired()])
    
    materia = StringField(
        'Asignatura', validators=[DataRequired(), Length(max=80)])
    
    asignada_en = DateField(
        'Fecha de asignacion', validators=[DataRequired()])
    
    dia_entrega = DateField(
        'Fecha de entrega', validators=[DataRequired()])
    
    nota = TextAreaField(
        'Comment', validators=[Length(max=150)])
    
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
