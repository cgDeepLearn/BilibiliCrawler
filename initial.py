# -*- coding: utf-8 -*-
"""
数据库初始化
"""
import os
import sys
from db import Base, eng
from config import BASE_DIR

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("run with 1 arg : db or file to choose the mode while initializing")
        exit(-1)
    mode = sys.argv[1]
    if mode == 'file':
        data_dir = os.path.join(BASE_DIR, 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
    elif mode == 'db':
        # Base.metadata.drop_all(eng)  # 删除表
        Base.metadata.create_all(eng)  # 建立表
        print("done!")
    else:
        print("wrong mode, run by use arg db or file!")