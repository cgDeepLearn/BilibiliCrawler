# -*- coding: utf-8 -*-
"""sqlalchemy basic"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import get_db_args

def get_engine():
    kwargs = get_db_args()
    connect_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(kwargs['user'], kwargs['password'], kwargs['host'], kwargs['port'], kwargs['dbname'])
    engine = create_engine(connect_str, encoding='utf-8')
    return engine

eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
# db_session = Session()

__all__ = ['eng', 'Base', 'Session']