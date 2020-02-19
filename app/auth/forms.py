from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, FileField, StringField
from wtforms.fields.html5 import DateField, TimeField


class LoadForm(FlaskForm):

    picture = FileField(id='file', _name='file')

    submit = SubmitField('', id='publish')


class EventForm(FlaskForm):

    name = StringField(
        'Nombre', validators=[DataRequired(), Length(max=80)])

    lugar = StringField(
        'Lugar', validators=[DataRequired(), Length(max=100)])

    dia = DateField(
        'Dia', validators=[DataRequired()])

    hora_inicio = TimeField(
        'Hora de Inicio', validators=[DataRequired()])

    hora_fin = TimeField(
        'Finaliza en', validators=[DataRequired()])

    nota = StringField('Nota')

    submit = SubmitField('')
