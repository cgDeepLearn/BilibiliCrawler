# -*- coding: utf-8 -*-
"""
Bili爬取主程序入口
"""
import sys
import csv
import os
from queue import Queue
from biliapi import BiliUserVideo
from db import Session
from utils import Producer, Consumer, Timer, Producer2
from config import BASE_DIR


def crawl2db(getsession, start, end):
    """多线程只使用一个连接会存在一些问题,建立一个session池每个线程一个session"""
    Q = Queue()
    sentinal = (None, None)  # 结束任务标记
    mythreads = []
    pthread = Producer2(Q, start=start, end=end,
                       func=lambda x: (x,), sleepsec=0.1)
    # mythreads.append(pthread)
    consumer_num = 4  # 4个消费者线程
    sessions = [getsession() for _ in range(consumer_num)]
    for i in range(consumer_num):
        db_session = sessions[i]  # 每个线程一个session
        cthread = Consumer(Q, session=db_session,
                           func=BiliUserVideo.store_user_video, sleepsec=0.01)
        mythreads.append(cthread)
    with Timer() as t:
        pthread.start()
        for thread in mythreads:
            thread.start()
        pthread.join()  # 生产者线程阻塞
        for _ in range(consumer_num):
            Q.put(sentinal)  # put结束标记
        for thread in mythreads:
            thread.join()
    for session in sessions:
        session.close()

    # db_session.close()
    print('runtime - (%i_%i) - : %s' % (start, end, t.elapsed))
    print('======= All Done! =======')


def crawl2csv(filenames, start, end):
    """sleep sec 可以用random生成在一个范围的正态分布更好些"""
    Q = Queue()
    sentinal = (None, None)  # 结束任务标记
    userfile, videofile = filenames
    with open(userfile, 'w', encoding='utf8', newline='') as userwriter,\
            open(videofile, 'w', encoding='utf8', newline='') as videowriter:
        usercsvwriter = csv.writer(userwriter)
        videocsvwriter = csv.writer(videowriter)
        mythreads = []
        pthread = Producer2(Q, start=start, end=end,
                           func=lambda x: (x,), sleepsec=0.1)
        # mythreads.append(pthread)
        consumer_num = 4  # 4个消费者线程
        for _ in range(consumer_num):
            mycsvwriter = (usercsvwriter, videocsvwriter)
            cthread = Consumer(Q, csvwriter=mycsvwriter,
                               func=BiliUserVideo.store_user_video, sleepsec=0.01)
            mythreads.append(cthread)
        with Timer() as t:
            pthread.start()
            for thread in mythreads:
                thread.start()
            pthread.join()
            for _ in range(consumer_num):
                Q.put(sentinal)
            for thread in mythreads:
                thread.join()

        print('runtime - (%i_%i) - : %s s' % (start, end, t.elapsed))
        print('======= All Done! =======')


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

        userfilepath = os.path.join(
            BASE_DIR, 'data/userinfo_%s_%s.csv' % (start, end))
        videofilepath = os.path.join(
            BASE_DIR, 'data/videoinfo_%s_%s.csv' % (start, end))
        filepaths = (userfilepath, videofilepath)
        crawl2csv(filepaths, int(start), int(end))
    elif mode == 'db':
        crawl2db(Session, int(start), int(end))
    else:
        print("wrong mode keyword, run by choosing (db or file)")
