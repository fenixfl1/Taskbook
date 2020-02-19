from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.default import *

engne = create_engine(
    SQLALCHEMY_DATABASE_URI, convert_unicode=True)

db = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engne))

Base = declarative_base()
Base.query = db.query_property()


def init_db():

    from . import models
    Base.metadata.create_all(bind=engne)