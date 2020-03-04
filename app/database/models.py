from sqlalchemy import Integer, String, ForeignKey,\
    Column, DateTime, Boolean, Time, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from flask_security import RoleMixin, UserMixin
from sqlalchemy_utils import CountryType
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from sqlalchemy_utils.types.url import URLType
import hashlib
from . import Base

from sqlalchemy_utils.types.weekdays import WeekDaysType
from sqlalchemy_utils.types.weekdays import WeekDaysType

class RolesUsers(Base):

    __tablename__ = 'roles_users'

    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    role_id = Column('role_id', Integer, ForeignKey('role.id')) 


class Role(Base, RoleMixin):

    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    description = Column(String(255), nullable=False)

    def __repr__(self):

        return '{}'.format(self.name)


class User(Base, UserMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(PhoneNumberType(), nullable=False)
    country = Column(CountryType(), nullable=False)
    gender = Column(String(3), nullable=False)
    last_login_at = Column(DateTime(timezone=True))
    current_login_at = Column(DateTime(timezone=True))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    confirmed_at = Column(DateTime(timezone=True))
    picture = relationship(
        'ProfilePicture', uselist=False, back_populates='user')
    profe = relationship('Profesor', back_populates='user')
    evento = relationship('Eventos', back_populates='user')
    plan = relationship('PlanEstudio', back_populates='user')
    tarea = relationship('Tarea', back_populates='user')
    active = Column(Boolean(), default=True)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('user', lazy='dynamic'))

    def __repr__(self):

        return self.first_name

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_phone(phone):
        return User.query.filter_by(phone_number=phone).first()

    @property
    def object_id(self):

        key = '<p>{0}</p>'.format(self.id)
        _key = bytes(key, 'utf-8')

        return int(hashlib.sha1(_key).hexdigest(), 16)

    @staticmethod
    def get_by_id(id):
        """
            Obtiene el id de un usurio
        """

        return User.query.get(id)

    def get_security_payload(self):

        return {
            'id': self.id,
            'first_name': self.first_name,
            'email': self.email,
            'country': self.country,
            'current_login_ip': self.current_login_ip
        }


class ProfilePicture(Base):

    __tablename__ = 'profile_picture'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='picture')
    picture_url = Column(URLType)
    name = Column(String(100), nullable=False)
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.name)


class Profesor(Base):

    __tablename__ = 'profesor'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='profe')
    materia = relationship('Materias', back_populates='profe')
    name = Column(String(80), nullable=False)
    last_name = Column(String(80))
    email = Column(String(100))
    phone_number = Column(String(22))

    def __repr__(self):

        return '{0} {1}'.format(self.name, self.last_name)


class Materias(Base):

    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True)
    profe_id = Column(Integer, ForeignKey('profesor.id'))
    profe = relationship('Profesor', back_populates='materia')
    tareas = relationship('DetalleTarea', back_populates='materia')
    horario = relationship('HorarioClases', back_populates='materia')
    name = Column(String(80), nullable=False)
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.name)


class HorarioClases(Base):

    __tablename__ = 'horario_clases'

    id = Column(Integer, primary_key=True)
    materia_id = Column(Integer, ForeignKey('materias.id'))
    materia = relationship('Materias', back_populates='horario')
    dia = Column(String(3), nullable=False)
    hora_inicio = Column(Time(), nullable=False)
    hora_fin = Column(Time(), nullable=False)
    aula = Column(String(5), nullable=False)
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.hora_inicio)


class Tarea(Base):

    __tablename__ = 'tarea'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='tarea')
    materia_id = Column(Integer, ForeignKey('materias.id'))
    detalle = relationship('DetalleTarea', back_populates='tarea')
    name = Column(String(80), nullable=False)
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.name)


class DetalleTarea(Base):

    __tablename__ = 'detalle_tarea'

    id = Column(Integer, primary_key=True)
    tarea_id = Column(Integer, ForeignKey('tarea.id'))
    tarea = relationship('Tarea', back_populates='detalle')
    materia_id = Column(Integer, ForeignKey('materias.id'))
    materia = relationship('Materias', back_populates='tareas')
    asignada_en = Column(DateTime(), default=func.now())
    dia = Column(Date(), nullable=False)
    hora_inicio = Column(Time(), nullable=False)
    hora_fin = Column(Time(), nullable=False)
    realizada_en = Column(DateTime())
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{0} - {1}'.format(self.dia, self.hora_inicio)


class Eventos(Base):

    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='evento')
    detalle = relationship('DetalleEvento', back_populates='evento')
    name = Column(String(150), nullable=False)
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.name)

    @staticmethod
    def get_by_id(id):

        return User.query.get(id)


class DetalleEvento(Base):

    __tablename__ = 'detalle_evento'

    id = Column(Integer, primary_key=True)
    evento_id = Column(Integer, ForeignKey('evento.id'))
    evento = relationship('Eventos', back_populates='detalle')
    creada_en = Column(DateTime(), default=func.now())
    lugar = Column(String(100), nullable=False)
    dia = Column(String(3), nullable=False)
    hora_inicio = Column(Time(), nullable=False)
    hora_fin = Column(Time(), nullable=False)
    comentario = Column(String(100))
    realizada_en = Column(DateTime())
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.lugar)


class PlanEstudio(Base):

    __tablename__ = 'plan_estudio'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='plan')
    detalle = relationship('DetallePlan', back_populates='plan')
    name = Column(String(100), nullable=False)
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.name)


class DetallePlan(Base):

    __tablename__ = 'detalle_plan'

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plan_estudio.id'))
    plan = relationship('PlanEstudio', back_populates='detalle')
    creada_en = Column(DateTime(), default=func.now())
    dia = Column(String(3), nullable=False)
    hora_inicio = Column(Time(), nullable=False)
    hora_fin = Column(Time(), nullable=False)
    objetivo = Column(String(255))
    realizada_en = Column(DateTime())
    estado = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.plan)
    