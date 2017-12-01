# -*- coding: utf-8 -*-
"""
数据库初始化
"""
from db import Base, eng

Base.metadata.drop_all(eng)
Base.metadata.create_all(eng)
print("done!")