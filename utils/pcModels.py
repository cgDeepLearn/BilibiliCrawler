# -*- coding: utf-8 -*-
"""
producer-consumer Model
生产者-消费者模型
"""


import time
import random
from threading import Thread
from db import BiliUserInfo, BiliVideoInfo, BiliVideoList


class Producer(Thread):
    """生产者"""
    def __init__(self, queue, start, end, func, sleepsec=0.3, cthread_num=10):
        """queue：队列
        start,end:生产起止编号
        sleepsec: 休息间隔
        func: 生产者函数
        cthread_num: 消费者线程终止标记个数
        """

        super(Producer, self).__init__()
        self._queue = queue
        self._range = (start, end)
        self._sleepsec = random.uniform(sleepsec, sleepsec * 2)
        self._cthread_num = cthread_num
        self._func = func 
    
    def run(self):
        for index in range(*self._range):
            plist = self._func(index)
            if plist:
                for pitem in plist:
                    self._queue.put((index, pitem))
                    print('[+] produce %s_%s' % (index, pitem))

                    time.sleep(self._sleepsec)
        time.sleep(10)
        for _ in range(self._cthread_num):
            self._queue.put((self._range[1], None))  # 结束任务标记


class Consumer(Thread):
    """消费者"""
    def __init__(self, queue, session=None, csvwriter=None, func=None, sleepsec=0.01):
        super(Consumer, self).__init__()
        self._queue = queue
        self._func = func
        self._session = session
        self._csvwriter = csvwriter
        self._sleepsec = random.uniform(sleepsec, sleepsec * 2)
    
    def run(self):
        while 1:
            if self._queue.empty():
                time.sleep(0.1)
            else:
                index, data = self._queue.get()
                if data is None:  # 任务结束标记
                    break
                self._func(index, data, session=self._session, csvwriter=self._csvwriter)
                
                # info = self._func(data)

                print('[-] consumed %s_%s\n' % (index, data))