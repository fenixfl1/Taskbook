from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Courses


class CoursesSchema(SQLAlchemyAutoSchema):

    class Meta():
        model = Courses
        include_fk = False
