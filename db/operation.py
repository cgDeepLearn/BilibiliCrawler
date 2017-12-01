# -*- coding: utf-8 -*-
"""
DB ORM Operation
"""
from functools import wraps, partial
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from psycopg2 import IntegrityError as pgIntegrityError
from sqlalchemy.exc import InvalidRequestError
from logger import storagelog
from .basic import Session


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            storagelog.error('DB operation error，here are details:{}'.format(e))
            args[2].rollback()  # db_session--->args[2]
    return session_commit


class DBOperation():
    
    @classmethod
    @db_commit_decorator
    def add(cls, data, db_session):
        # db_session = Session()
        db_session.add(data)
        
        db_session.commit()
        # db_session.close()

    @classmethod
    @db_commit_decorator
    def add_all(cls, datas, db_session):
        #db_session = Session()
        try:
            db_session.add_all(datas)
            db_session.commit()
            
        except (SqlalchemyIntegrityError, pgIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add(data, db_session)
