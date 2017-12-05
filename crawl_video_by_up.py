# -*- coding: utf-8 -*-
"""
BiliVideo爬取主程序入口,从userinfo入手，
如果user有video则生成aid list发送到Producer
"""
import sys
import csv
import os
from queue import Queue
from biliapi import BiliUser, BiliVideo
from db import Session
from utils import Producer, Consumer, Timer
from config import BASE_DIR


def crawl2db(getsession, start, end):
    """多线程只使用一个连接会存在一些问题,建立一个session池每个线程一个session
    视频访问速率有很严格的限制，请调大sleepsec"""
    Q = Queue()
    mythreads = []
    pthread = Producer(Q, start=start, end=end, func=BiliUser.getVideoList, sleepsec=0.5)
    mythreads.append(pthread)
    consumer_num = 4 # 4个消费者线程
    sessions = [getsession() for _ in range(consumer_num)]
    for i in range(consumer_num):
        db_session = sessions[i] # 每个线程一个session
        cthread = Consumer(Q, session=db_session, func=BiliVideo.store_video, sleepsec=0.5)
        mythreads.append(cthread)
    with Timer() as t:
        for thread in mythreads:
            thread.start()
        for thread in mythreads:
            thread.join()
    for session in sessions:
        session.close()
        
    # db_session.close()
    print('runtime: %s' % t.elapsed)
    print('======= All Done! ======')


def crawl2csv(filename, start, end):
    """sleep sec 可以用random生成在一个范围的正态分布更好些
    start, end: up主mid范围"""
    Q = Queue()
    
    with open(filename, 'w', encoding='utf8', newline='') as fwriter:
        mycsvwriter = csv.writer(fwriter)
        mythreads = []
        pthread = Producer(Q, start=start, end=end, func=BiliUser.getVideoList, sleepsec=0.15)
        mythreads.append(pthread)
        consumer_num = 4 # 4个消费者线程
        for _ in range(consumer_num):
            cthread = Consumer(Q, csvwriter=mycsvwriter, func=BiliVideo.store_video, sleepsec=0.01)
            mythreads.append(cthread)
        with Timer() as t:
            for thread in mythreads:
                thread.start()
            for thread in mythreads:
                thread.join()
        
        print('runtime: %s' % t.elapsed)
        print('======= All Done! ======')


if __name__ == '__main__':
    """运行参数:
    1: mode(db/file)---选择存储方式(db是postgresql数据库存储可修改db.basic和config.conf配置换成mysql等其他的数据库)
    选择db方式时若是初次运行，请运行python inital.py 是drop数据库和create表操作
    2：start crawl初始id
    3 :end crawl结束id"""
    if len(sys.argv) < 4:
        print("need more args...")
    else:
        mode = sys.argv[1]
        start, end = sys.argv[2], sys.argv[3]

    if mode == 'file':
        filepath = os.path.join(BASE_DIR, 'data/videoinfo_byup_%s_%s.csv' % (start, end))
        crawl2csv(filepath, int(start), int(end))
    elif mode == 'db':
        crawl2db(Session, int(start), int(end))
    else:
        print("wrong mode keyword, run by choosing (db or file)")
        
