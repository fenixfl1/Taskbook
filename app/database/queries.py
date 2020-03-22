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
            except:
                pass
            
        if 'order_by' in kwargs and kwargs['order_by'] == 'date1':
            
            try:
                return db.query(entity).filter(entity.user_id == user.id).\
                    order_by(entity.detalle.dia_endrega).one().options(contains_eager(entity.user))
            except:
                pass
            
        if 'order_by' in kwargs and kwargs['order_by'] == 'date2':
            
            try:
                return db.query(entity).filter(entity.user_id == user.id).\
                    options(contains_eager(entity.user)).older_by(entity.detalle.hora_fin)
            except:
                pass
        
        else:

            try:
                return db.query(entity).filter(entity.user_id == user.id).\
                    options(contains_eager(entity.user))
            except:
                pass

    @staticmethod
    def contador(entity, user):

        try:
            return db.query(entity).filter(entity.user_id == user.id).count()

        except:
            pass

    # get the time in text formt
    @staticmethod
    def literal_time(entity):

        try:

            date_str = str(entity[0].detalle[0].dia)

            date_object = datetime.strptime(date_str, '%Y-%m-%d')

            date = datetime.strftime(date_object, '%a %d de %b')

            return date

        except:
            pass

    # get the next activities to perform
    @staticmethod
    def get_most_recent(result):

        date = []

        # num_activity = contador(result)

        for i in range(2):

            date.append(result[i].detalle[i].dia)

            print(date)

        return max(date)

    @staticmethod
    def get_query(entity, user):

        return db.query(entity).filter(entity.user_id == user.id)
