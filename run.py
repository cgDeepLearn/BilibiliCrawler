# -*- coding: utf-8 -*-
"""
Bili爬取主程序入口
"""
from queue import Queue
from biliapi import BiliUser, BiliVideo
from db import DBOperation
from utils import Producer, Consumer, Timer

def crawl():
    Q = Queue()
    mythreads = []
    pthread = Producer(Q, start=1, end=10, func=lambda x: (x,), sleepsec=0.1)
    mythreads.append(pthread)
    consumer_num = 4 # 4个消费者线程
    for _ in range(consumer_num):
        cthread = Consumer(Q, func=BiliUser.store_user, sleepsec=0.1)
        mythreads.append(cthread)
    with Timer() as t:
        for thread in mythreads:
            thread.start()
        for thread in mythreads:
            thread.join()
    print('runtime: %s' % t.elapsed)
    print('======= All Done! =====')
        



if __name__ == '__main__':
    crawl()