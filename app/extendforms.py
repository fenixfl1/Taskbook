from flask_security.forms import RegisterForm
from wtforms_alchemy import PhoneNumberField, CountryField
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


genders = [(None, ''), (u'M', u'Masculino'),
           (u'F', u'Femenino'), (u'NB', u'No binario')]


class ExtendRegisterForm(RegisterForm):

    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    phone_number = PhoneNumberField('Telefono', validators=[DataRequired()])
    country = CountryField('País', validators=[DataRequired()])
    aceptar = BooleanField('', validators=[DataRequired()])
    univercity = StringField('Univercity', validators=[DataRequired()])
    gender = SelectField('Genero', choices=genders,
                         validators=[DataRequired()])
