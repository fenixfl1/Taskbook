from sqlalchemy.orm import contains_eager
from datetime import datetime
from . import db


class Queries():
    """
    class for perform all query in the database 
    """

    @staticmethod
    def queries(entity, user):
        """
        event = Queries.queries(entity, user)
        """

        try:
            return db.query(entity).filter(entity.user_id == user.id).\
                options(contains_eager(entity.user)).all()
                
        except:
            pass
        
    @staticmethod
    def contador(entity, user):

        try:
            return db.query(entity).filter(
                entity.user_id == user.id).count()
            
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