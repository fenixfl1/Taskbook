from sqlalchemy import Integer, String, ForeignKey,\
    Column, DateTime, Boolean, Time, CHAR, TEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from flask_security import UserMixin, RoleMixin
from sqlalchemy_utils import CountryType
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from sqlalchemy_utils.types.url import URLType
from . import Base


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
    course = relationship('Courses', back_populates='user')
    teacher = relationship('Teachers', back_populates='user')
    event = relationship('Events', back_populates='user')
    plan = relationship('StudyPlan', back_populates='user')
    task = relationship('Tasks', back_populates='user')
    notify = relationship('Notify', back_populates='user')
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

    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(first_name=name).first()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)


class Teachers(Base):

    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='teacher')
    course = relationship('Courses', back_populates='teacher')
    full_name = Column(String(80), nullable=False, unique=True)
    email = Column(String(100))
    phone_number = Column(String(22))
    table_name = Column(String(10), default='teachers')
    state = Column(Boolean(), default=True)

    def __repr__(self):

        return '{0}'.format(self.full_name)


class Courses(Base):

    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='course')
    task = relationship('Tasks', back_populates='course')
    class_schedule = relationship('ClassSchedule', back_populates='course')
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship('Teachers', back_populates='course')
    name = Column(String(80), nullable=False)
    finished = Column(Boolean(), default=False)
    qualification = Column(CHAR(1), default=None)
    table_name = Column(String(10), default='courses')
    state = Column(Boolean(), default=True)

    def __init__(self, name, user_id, **kwargs):

        self.name = name
        self.user_id = user_id
        self.teacher = kwargs.get('teacher')
        self.finished = kwargs.get('finished')
        self.qualification = kwargs.get('qualification')

    def __repr__(self):
        return '{}'.format(self.name)

    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(name=name).first()


class ClassSchedule(Base):

    __tablename__ = 'class_schedule'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE'))
    course = relationship('Courses', back_populates='class_schedule')
    day = Column(CHAR(1), nullable=False)
    start_date = Column(Time(), nullable=False)
    end_date = Column(Time(), nullable=False)
    classroom = Column(String(5), nullable=False)
    state = Column(Boolean(), default=True)

    def __repr__(self):
        return '{0} - {1}'.format(self.start_date, self.end_date)


class Tasks(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='task')
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE'))
    course = relationship('Courses', back_populates='task')
    name = Column(String(80), nullable=False)
    assigned_in = Column(DateTime(timezone=True), default=func.now())
    delivery_day = Column(DateTime(), nullable=False)
    finished_in = Column(DateTime())
    comment = Column(String(150))
    table_name = Column(String(10), default='tasks')
    done = Column(Boolean(), default=False)
    state = Column(Boolean(), default=True)

    def __repr__(self):
        return "{}".format(self.name)


class Events(Base):

    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='event')
    date_created = Column(DateTime(), default=func.now())
    title = Column(String(150), nullable=False)
    location = Column(String(100), nullable=False)
    url = Column(URLType)
    start_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime(), nullable=False)
    comment = Column(String(100))
    table_name = Column(String(10), default='events')
    finished_in = Column(DateTime())
    state = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.title)

    @staticmethod
    def get_by_id(id):

        return User.query.get(id)

    @staticmethod
    def update_color(color):
        pass


class StudyPlan(Base):

    __tablename__ = 'study_plan'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='plan')
    detail = relationship('StudyPlanDetail', back_populates='plan')
    name = Column(String(100), nullable=False)
    table_name = Column(String(10), default='study-plan')
    state = Column(Boolean(), default=True)

    def __repr__(self):

        return '{}'.format(self.name)


class StudyPlanDetail(Base):

    __tablename__ = 'study_plan_detail'

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey(
        'study_plan.id', ondelete='CASCADE'))
    plan = relationship('StudyPlan', back_populates='detail')
    date_created = Column(DateTime(), default=func.now())
    title = Column(String(255), nullable=False)
    url = Column(URLType)
    day = Column(Integer(), nullable=False)
    start_time = Column(Time(), nullable=False)
    end_time = Column(Time(), nullable=False)
    objective = Column(String(255))
    table_name = Column(String(15), default='study_plan_detail')
    finished_in = Column(DateTime())
    done = Column(Boolean(), default=True)
    state = Column(Boolean(), default=True)

    def __repr__(self):
        return '{0}'.format(self.title)


class Notify(Base):

    __tablename__ = 'notify'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='notify')
    title = Column(String(250), nullable=False)
    msg = Column(TEXT(), nullable=False)
    notify_time = Column(DateTime(), nullable=False)
    published_at = Column(DateTime(), default=func.now())
    readed = Column(Boolean(), default=False)
    state = Column(Boolean(), default=True)

    def __init__(self, user_id, title, msg, notify_time):

        self.user_id = user_id
        self.title = title
        self.msg = msg
        self.notify_time = notify_time

    def __repr__(self):
        return '{}'.format(self.title)
