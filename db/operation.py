# -*- coding: utf-8 -*-
"""
DB ORM Operation
"""
from functools import wraps, partial
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError
from logger import storagelog
from .basic import db_session


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            storagelog.error('DB operation error，here are details:{}'.format(e))
            db_session.rollback()
    return session_commit


class DBOperation():
    
    @classmethod
    @db_commit_decorator
    def add(cls, data):
        db_session.add(data)
        db_session.begin_nested()
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def add_all(cls, datas):
        try:
            db_session.add_all(datas)
            db_session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add(data)
