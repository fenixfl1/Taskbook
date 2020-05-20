from sqlalchemy.orm import contains_eager
from datetime import datetime
from . import db


class Queries():
    """
    class for perform all query in the database 
    """

    @staticmethod
    def queries(entity, user, **kwargs):
        """
        event = Queries.queries(entity, user)
        """

        if 'order_by' in kwargs and kwargs['order_by'] == 'name':

            try:
                return db.query(entity).filter(entity.user_id == user.id).\
                    options(contains_eager(entity.user)).older_by(entity.name)
            except ValueError as e:
                raise e

        if 'order_by' in kwargs and kwargs['order_by'] == 'date1':

            try:
                return db.query(entity).filter(entity.user_id == user.id).first()
            except ValueError as e:
                raise e

        if 'order_by' in kwargs and kwargs['order_by'] == 'date2':

            try:
                return db.query(entity).filter(entity.user_id == user.id).\
                    options(contains_eager(entity.user))
            except ValueError as e:
                raise e

        else:

            try:
                return db.query(entity).filter(entity.user_id == user.id).\
                    options(contains_eager(entity.user))
            except ValueError as e:
                raise e

    @staticmethod
    def contador(entity, user, n):
        """
            this function is to count the number of rows in any table.
            :entity reference to the table to want count.
            :user the current user
            :n is the state of the column state
        """

        try:
            return db.query(entity).filter(entity.user_id == user.id).\
                filter(entity.state == n).count()

        except ValueError as e:
            raise e

    # get the time in text formt
    @staticmethod
    def literal_time(entity):

        try:

            date_str = str(entity[0].detalle[0].dia)

            date_object = datetime.strptime(date_str, '%Y-%m-%d')

            date = datetime.strftime(date_object, '%a %d de %b')

            return date

        except ValueError as e:
            raise e

    # get the next activities to perform
    @staticmethod
    def get_most_recent(result, num, entity, user):

        date = []

        for i in range(num):

            date.append(result[i].detalle[0].dia_endrega)

        m = max(date)

        r = db.query(entity).filter(entity.user_id == user.id).\
            options(contains_eager(entity.user)).first()

        return r

    @staticmethod
    def get_query(entity, user):

        return db.query(entity).filter(entity.user_id == user.id)
