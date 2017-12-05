# -*- coding: utf-8 -*-
"""
数据库初始化
"""
from db import Base, eng

Base.metadata.create_all(eng)  # 建立表
print("done!")