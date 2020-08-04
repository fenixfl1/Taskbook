# from app.database.queries import Queries
from flask_security import current_user
from flask import Markup
from app.database.models import Tasks, Courses, Teachers, \
    StudyPlan, StudyPlanGoals, Events
from app.database import db
from app.extentions import avatars, db_session
import hashlib
from datetime import datetime


def tasks(id, **kwargs):

    get_tasks = db.query(Tasks).\
        filter(Tasks.user_id == current_user.id).\
        filter(Tasks.state == 1)

    f = get_tasks
    progress = 0.0

    if 'this' in kwargs:
        if kwargs.get('this') == 1:
            if 'done' in kwargs:
                if kwargs.get('done') == 1:
                    f = get_tasks.filter(Tasks.course_id == id). \
                        filter(Tasks.done == 1).count()
                elif kwargs.get('done') == 0:
                    f = get_tasks.filter(Tasks.course_id == id). \
                        filter(Tasks.done == 0).count()
                else:
                    f = get_tasks.filter(Tasks.course_id == id).count()

                return f

            if 'progress' in kwargs:
                if kwargs.get('progress') == 1:
                    done = get_tasks.filter(Tasks.done == 1). \
                        filter(Tasks.course_id == id).count()
                    total = get_tasks.filter(Tasks.course_id == id).count()

                    try:
                        progress = (done * 100) / total
                    except ZeroDivisionError as e:
                        raise e
                    finally:
                        return progress

                else:
                    return ValueError("Value error")

        if kwargs.get('this') == 0:
            if 'done' in kwargs:
                if kwargs.get('done') == 1:
                    return get_tasks.filter(Tasks.done == 1).count()
                if kwargs.get('done') == 0:
                    return get_tasks.filter(Tasks.done == 0).count()
                else:
                    return get_tasks.count()

            if 'progress' in kwargs:

                if kwargs.get('progress') == 1:
                    done = get_tasks.filter(Tasks.done == 1).count()
                    total = get_tasks.count()

                    try:
                        progress = (done * 100) / total
                    except ZeroDivisionError as e:
                        raise e
                    finally:
                        return progress

                else:
                    return ValueError("Value error")
    else:
        return ValueError("Value error")

    return get_tasks.count()


def courses(value, **kwargs):

    filtro = db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.state == 1)

    progress = 0

    if 'finished' in kwargs:

        if kwargs.get('finished') == 0:
            return filtro.filter(Courses.finished == 0).count()

        if kwargs.get('finished') == 1:
            return filtro.filter(Courses.finished == 1).count()

        else:
            return filtro.count()

    if 'progress' in kwargs:

        if kwargs.get('progress') == 1:
            total = filtro.count()
            finished = filtro.filter(Courses.finished == 1).count()

            try:
                progress = (finished * 100) / total
            except ZeroDivisionError as e:
                raise e
            finally:
                return progress
        else:
            return 0


def teachers(id, n=1):

    filtro = db.query(Teachers).\
        filter(Teachers.user_id == current_user.id).\
        filter(Teachers.state == n)

    return filtro


def study_plan(value, **kwargs):

    get_plan = db.query(StudyPlan).\
        filter(StudyPlan.user_id == current_user.id).\
        filter(StudyPlan.state == 1)

    progress = 0

    if 'done' in kwargs:
        if kwargs.get('done') == 1:
            return get_plan.filter(StudyPlan.done == 1).count()
        elif kwargs.get('done') == 0:
            return get_plan.filter(StudyPlan.done == 0).count()
        else:
            return get_plan.count()

    if 'progress' in kwargs:
        if kwargs.get('progress') == 1:
            done = get_plan.filter(StudyPlan.done == 1).count()
            total = get_plan.count()

            try:
                progress = (done * 100) / total
            except ZeroDivisionError as e:
                raise e
            finally:
                return progress

        else:
            return ValueError('Error in the key word')

    return get_plan.count()


def study_plan_goals(id, **kwargs):

    get_goals = db.query(StudyPlanGoals).\
        join(StudyPlan, StudyPlanGoals.plan_id == StudyPlan.id).\
        filter(StudyPlanGoals.state == 1).\
        filter(StudyPlan.id == id).\
        filter(StudyPlan.state == 1).\
        filter(StudyPlan.user_id == current_user.id)

    progress = 0

    if 'done' in kwargs:
        if kwargs.get('done') == 1:
            return get_goals.filter(StudyPlanGoals.done == 1).count()
        elif kwargs.get('done') == 0:
            return get_goals.filter(StudyPlanGoals.done == 0).count()
        else:
            return get_goals.count()

    if 'progress' in kwargs:
        if kwargs.get('progress') == 1:
            done = get_goals.filter(StudyPlanGoals.done == 1).count()
            total = get_goals.count()

            try:
                progress = (done * 100) / total
            except ZeroDivisionError as e:
                raise e
            finally:
                return progress

    return get_goals.count()


def list_courses(value):
    return db.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.state == 1).\
        filter(Courses.finished == 0).all()


def paginate_courses(state, finished):

    filter = db_session.query(Courses).\
        filter(Courses.user_id == current_user.id).\
        filter(Courses.state == state).\
        filter(Courses.finished == finished).\
        paginate(1, 8, 0)

    return filter

def avatar(value, **kwargs):

    classes = ''
    size = '50'

    if kwargs['size']:
        size = kwargs['size']
    if kwargs['class']:
        classes = kwargs['class']

    email_hash = hashlib.md5(current_user.email.lower().
                             encode('utf-8')).hexdigest()

    url_avatar = avatars.gravatar(email_hash, size=size)

    return Markup(
        '<img src="{}" class="{}" title="{} {}">'.
        format(url_avatar, str(classes),
               current_user.first_name.capitalize(),
               current_user.last_name.capitalize())
    )


def generate_avatar(value, **kwargs):

    title = ''
    classes = ''
    size = '50'

    if 'title' in kwargs:
        title = kwargs.get('title')
    if 'size' in kwargs:
        size = kwargs['size']
    if 'class' in kwargs:
        classes = kwargs['class']

    email_hash = hashlib.md5(value.lower().encode('utf-8')).hexdigest()

    url_avatar = avatars.gravatar(email_hash, size=size)

    return Markup(
        '<img src="{}" class="{}" title="{}">'.
        format(url_avatar, str(classes), str(title))
    )
    

def the_next(value, **kwargs):
    
    course = db.query(Courses). \
        filter(Courses.user_id == current_user.id). \
        filter(Courses.state == 1). \
        order_by(Courses.name)
    
    next_task = db.query(Tasks). \
        filter(Tasks.user_id == current_user.id). \
        filter(Tasks.state == 1). \
        order_by(Tasks.delivery_day)
    
    next_plan = db.query(StudyPlan). \
        filter(StudyPlan.user_id == current_user.id). \
        filter(StudyPlan.state == 1). \
        order_by(StudyPlan.start_date)
        
    next_goals = db.query(StudyPlanGoals).\
        join(StudyPlan, StudyPlanGoals.plan_id == StudyPlan.id).\
        filter(StudyPlanGoals.state == 1).\
        filter(StudyPlan.state == 1).\
        filter(StudyPlan.user_id == current_user.id)
        
    if 'task' in kwargs:
        if kwargs.get('task', True):
            next = next_task.first()
    
    elif 'stuty_plan' in kwargs:
        if kwargs.get('stuty_plan', True):
            next = next_plan.first()
            
    elif 'study_plan_goals' in kwargs:
        if kwargs.get('study_plan_goals', True):
            next = next_goals.first()
            
    else:
        next = course.first()
        
    if 'data' in kwargs:
        if kwargs.get('data') == 'name':
            return next.name
        
        elif kwargs.get('data') == 'id':
            return next.id
        
        elif kwargs.get('data') == 'title':
            return next.title
        
    return next

class Filter():

    def __init__(self, app):

        app.jinja_env.filters['tasks'] = tasks
        app.jinja_env.filters['courses'] = courses
        app.jinja_env.filters['teacher'] = teachers
        app.jinja_env.filters['plan'] = study_plan
        app.jinja_env.filters['list_courses'] = list_courses
        app.jinja_env.filters['default'] = avatar
        app.jinja_env.filters['generate_avatar'] = generate_avatar
        app.jinja_env.filters['paginate_courses'] = paginate_courses
        app.jinja_env.filters['study_plan_goals'] = study_plan_goals
        app.jinja_env.filters['next'] = the_next
